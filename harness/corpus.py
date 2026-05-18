"""Corpus storage: sqlite schema, ingest from markdown, retrieval helpers.

Single source of truth: the markdown files in ``corpus/`` are canonical.
The sqlite DB is a derived index, rebuildable from scratch via ``reindex()``.
That invariant means we can freely drop and recreate the DB; we never have
to migrate sqlite schemas in-place.
"""

from __future__ import annotations

import os
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import frontmatter

from harness.schema import CorpusEntryFrontmatter

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = REPO_ROOT / "corpus.db"
DEFAULT_CORPUS_DIR = REPO_ROOT / "corpus"


def db_path() -> Path:
    return Path(os.environ.get("W3S_DB_PATH") or DEFAULT_DB_PATH)


def corpus_dir() -> Path:
    return Path(os.environ.get("W3S_CORPUS_DIR") or DEFAULT_CORPUS_DIR)


DDL = [
    """
    CREATE TABLE IF NOT EXISTS corpus_entries (
        id              TEXT PRIMARY KEY,
        source          TEXT NOT NULL,
        source_url      TEXT,
        title           TEXT NOT NULL,
        body            TEXT NOT NULL,
        ingested_at     TEXT NOT NULL,
        published_at    TEXT,
        severity        TEXT,
        file_path       TEXT NOT NULL,
        raw_frontmatter TEXT NOT NULL
    );
    """,
    "CREATE INDEX IF NOT EXISTS idx_entries_source   ON corpus_entries(source);",
    "CREATE INDEX IF NOT EXISTS idx_entries_severity ON corpus_entries(severity);",
    """
    CREATE TABLE IF NOT EXISTS corpus_vuln_classes (
        entry_id   TEXT NOT NULL REFERENCES corpus_entries(id) ON DELETE CASCADE,
        vuln_class TEXT NOT NULL,
        PRIMARY KEY (entry_id, vuln_class)
    );
    """,
    "CREATE INDEX IF NOT EXISTS idx_vuln_class ON corpus_vuln_classes(vuln_class);",
    """
    CREATE TABLE IF NOT EXISTS corpus_protocol_categories (
        entry_id TEXT NOT NULL REFERENCES corpus_entries(id) ON DELETE CASCADE,
        category TEXT NOT NULL,
        PRIMARY KEY (entry_id, category)
    );
    """,
    "CREATE INDEX IF NOT EXISTS idx_protocol_category ON corpus_protocol_categories(category);",
    """
    CREATE TABLE IF NOT EXISTS corpus_tags (
        entry_id TEXT NOT NULL REFERENCES corpus_entries(id) ON DELETE CASCADE,
        tag      TEXT NOT NULL,
        PRIMARY KEY (entry_id, tag)
    );
    """,
    "CREATE INDEX IF NOT EXISTS idx_tag ON corpus_tags(tag);",
    """
    CREATE TABLE IF NOT EXISTS corpus_related_swc (
        entry_id TEXT NOT NULL REFERENCES corpus_entries(id) ON DELETE CASCADE,
        swc_id   TEXT NOT NULL,
        PRIMARY KEY (entry_id, swc_id)
    );
    """,
    """
    CREATE VIRTUAL TABLE IF NOT EXISTS corpus_fts USING fts5(
        entry_id UNINDEXED,
        title,
        body,
        tokenize = 'porter unicode61'
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS corpus_embeddings (
        entry_id    TEXT NOT NULL REFERENCES corpus_entries(id) ON DELETE CASCADE,
        model       TEXT NOT NULL,
        chunk_index INTEGER NOT NULL,
        embedding   BLOB NOT NULL,
        PRIMARY KEY (entry_id, model, chunk_index)
    );
    """,
]


@contextmanager
def connect(path: Path | None = None) -> Iterator[sqlite3.Connection]:
    p = path or db_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    # 30s busy timeout — if a concurrent writer (e.g. background synthesizer
    # reindex) holds the write lock, retry rather than fail immediately.
    conn = sqlite3.connect(p, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    # WAL mode lets readers proceed while a writer is mid-transaction —
    # crucial for tests + analysis tools running alongside crawlers.
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db(path: Path | None = None) -> None:
    """Create all tables (idempotent)."""
    with connect(path) as conn:
        for stmt in DDL:
            conn.executescript(stmt)


# ---------------------------------------------------------------------------
# Ingest: markdown file -> CorpusEntryFrontmatter -> sqlite rows
# ---------------------------------------------------------------------------


@dataclass
class IngestResult:
    inserted: int
    updated: int
    skipped: int
    errors: list[tuple[Path, str]]


def parse_entry(path: Path) -> tuple[CorpusEntryFrontmatter, str]:
    """Return (frontmatter, body) for a single markdown file."""
    post = frontmatter.load(path)
    fm = CorpusEntryFrontmatter.model_validate(post.metadata)
    return fm, post.content


def upsert_entry(
    conn: sqlite3.Connection,
    fm: CorpusEntryFrontmatter,
    body: str,
    file_path: Path,
) -> Literal_Upsert:
    rel_path = str(file_path.resolve().relative_to(REPO_ROOT))
    raw_yaml = _dump_yaml(fm)

    existing = conn.execute(
        "SELECT id FROM corpus_entries WHERE id = ?", (fm.id,)
    ).fetchone()

    if existing is None:
        conn.execute(
            """
            INSERT INTO corpus_entries
              (id, source, source_url, title, body, ingested_at, published_at,
               severity, file_path, raw_frontmatter)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                fm.id,
                fm.source,
                fm.source_url,
                fm.title,
                body,
                fm.ingested_at.isoformat(),
                fm.published_at.isoformat() if fm.published_at else None,
                fm.severity,
                rel_path,
                raw_yaml,
            ),
        )
        result = "inserted"
    else:
        conn.execute(
            """
            UPDATE corpus_entries SET
              source          = ?,
              source_url      = ?,
              title           = ?,
              body            = ?,
              ingested_at     = ?,
              published_at    = ?,
              severity        = ?,
              file_path       = ?,
              raw_frontmatter = ?
            WHERE id = ?
            """,
            (
                fm.source,
                fm.source_url,
                fm.title,
                body,
                fm.ingested_at.isoformat(),
                fm.published_at.isoformat() if fm.published_at else None,
                fm.severity,
                rel_path,
                raw_yaml,
                fm.id,
            ),
        )
        result = "updated"

    # Replace child rows wholesale — simpler than diffing.
    for table, col, values in [
        ("corpus_vuln_classes", "vuln_class", fm.vuln_class),
        ("corpus_protocol_categories", "category", fm.protocol_category),
        ("corpus_tags", "tag", fm.tags),
        ("corpus_related_swc", "swc_id", fm.related_swc),
    ]:
        conn.execute(f"DELETE FROM {table} WHERE entry_id = ?", (fm.id,))
        conn.executemany(
            f"INSERT INTO {table} (entry_id, {col}) VALUES (?, ?)",
            [(fm.id, v) for v in values],
        )

    # FTS5 mirror — replace existing row for this entry.
    conn.execute("DELETE FROM corpus_fts WHERE entry_id = ?", (fm.id,))
    conn.execute(
        "INSERT INTO corpus_fts (entry_id, title, body) VALUES (?, ?, ?)",
        (fm.id, fm.title, body),
    )

    return result  # type: ignore[return-value]


# Type alias used only for return annotation above; placed after the function
# for readability.
from typing import Literal as _Literal  # noqa: E402

Literal_Upsert = _Literal["inserted", "updated"]


def reindex(
    corpus_root: Path | None = None,
    db: Path | None = None,
) -> IngestResult:
    """Drop + recreate the sqlite index from the on-disk markdown corpus.

    Atomic: builds the new index in a temp file and renames over the
    canonical path only on success. If killed mid-build, the existing
    DB is preserved — no more "killed during reindex left me with an
    empty corpus".

    Embeddings are NOT rebuilt here — embed via ``scripts/ingest_md.py --embed``.
    """
    root = corpus_root or corpus_dir()
    p = db or db_path()

    # Build into a sibling temp file
    tmp = p.with_suffix(p.suffix + ".reindex.tmp")
    if tmp.exists():
        tmp.unlink()

    result = IngestResult(inserted=0, updated=0, skipped=0, errors=[])
    try:
        init_db(tmp)
        with connect(tmp) as conn:
            for path in sorted(root.rglob("*.md")):
                if path.name.startswith("_"):
                    result.skipped += 1
                    continue
                try:
                    fm, body = parse_entry(path)
                    action = upsert_entry(conn, fm, body, path)
                    if action == "inserted":
                        result.inserted += 1
                    else:
                        result.updated += 1
                except Exception as e:  # noqa: BLE001
                    result.errors.append((path, str(e)))
        # Success — atomically replace the live DB with the temp one
        # (os.replace is atomic on POSIX even when target exists)
        import os as _os
        _os.replace(tmp, p)
    except BaseException:
        # On any failure (including KeyboardInterrupt), leave the existing DB
        # intact and remove the temp.
        try:
            tmp.unlink()
        except OSError:
            pass
        raise
    return result


# ---------------------------------------------------------------------------
# Query helpers — backbone of the MCP server tools
# ---------------------------------------------------------------------------


@dataclass
class CorpusHit:
    id: str
    title: str
    source: str
    severity: str | None
    snippet: str
    score: float


def search(
    query: str,
    *,
    vuln_class: list[str] | None = None,
    severity: list[str] | None = None,
    source: list[str] | None = None,
    exclude_ids: list[str] | None = None,
    top_k: int = 10,
    db: Path | None = None,
) -> list[CorpusHit]:
    """FTS5 BM25 search with optional structured filters.

    ``exclude_ids`` is critical for eval runs: it filters out the corpus
    entries that match a historical exploit's post-mortem so the harness
    can't trivially solve eval cases by reading the answer.
    """
    # FTS5 MATCH expects a query. Escape user-supplied terms minimally.
    fts_query = _fts_escape(query)

    filters_sql = []
    params: list = [fts_query]

    if vuln_class:
        placeholders = ",".join("?" * len(vuln_class))
        filters_sql.append(
            f"e.id IN (SELECT entry_id FROM corpus_vuln_classes WHERE vuln_class IN ({placeholders}))"
        )
        params.extend(vuln_class)
    if severity:
        placeholders = ",".join("?" * len(severity))
        filters_sql.append(f"e.severity IN ({placeholders})")
        params.extend(severity)
    if source:
        placeholders = ",".join("?" * len(source))
        filters_sql.append(f"e.source IN ({placeholders})")
        params.extend(source)
    if exclude_ids:
        placeholders = ",".join("?" * len(exclude_ids))
        filters_sql.append(f"e.id NOT IN ({placeholders})")
        params.extend(exclude_ids)

    where = "WHERE " + " AND ".join(filters_sql) if filters_sql else ""
    sql = f"""
        SELECT
          e.id, e.title, e.source, e.severity,
          snippet(corpus_fts, 2, '<mark>', '</mark>', '...', 16) AS snip,
          bm25(corpus_fts) AS score
        FROM corpus_fts
        JOIN corpus_entries e ON e.id = corpus_fts.entry_id
        WHERE corpus_fts MATCH ?
        {('AND ' + ' AND '.join(filters_sql)) if filters_sql else ''}
        ORDER BY score
        LIMIT ?
    """
    params.append(top_k)

    with connect(db) as conn:
        rows = conn.execute(sql, params).fetchall()

    return [
        CorpusHit(
            id=r["id"],
            title=r["title"],
            source=r["source"],
            severity=r["severity"],
            snippet=r["snip"],
            score=float(r["score"]),
        )
        for r in rows
    ]


def get_entry(entry_id: str, db: Path | None = None) -> dict | None:
    """Return full markdown body + structured frontmatter for a single entry."""
    with connect(db) as conn:
        row = conn.execute(
            "SELECT * FROM corpus_entries WHERE id = ?", (entry_id,)
        ).fetchone()
        if not row:
            return None
        d = dict(row)
        d["vuln_class"] = [
            r["vuln_class"]
            for r in conn.execute(
                "SELECT vuln_class FROM corpus_vuln_classes WHERE entry_id = ?",
                (entry_id,),
            )
        ]
        d["protocol_category"] = [
            r["category"]
            for r in conn.execute(
                "SELECT category FROM corpus_protocol_categories WHERE entry_id = ?",
                (entry_id,),
            )
        ]
        d["tags"] = [
            r["tag"]
            for r in conn.execute(
                "SELECT tag FROM corpus_tags WHERE entry_id = ?", (entry_id,)
            )
        ]
        d["related_swc"] = [
            r["swc_id"]
            for r in conn.execute(
                "SELECT swc_id FROM corpus_related_swc WHERE entry_id = ?", (entry_id,)
            )
        ]
        return d


def list_synthesis_notes(
    category: str | None = None, db: Path | None = None
) -> list[dict]:
    with connect(db) as conn:
        if category:
            rows = conn.execute(
                """
                SELECT e.id, e.title, e.ingested_at, e.severity
                FROM corpus_entries e
                JOIN corpus_protocol_categories c ON c.entry_id = e.id
                WHERE e.source = 'synthesis' AND c.category = ?
                ORDER BY e.ingested_at DESC
                """,
                (category,),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT id, title, ingested_at, severity
                FROM corpus_entries
                WHERE source = 'synthesis'
                ORDER BY ingested_at DESC
                """
            ).fetchall()
    return [dict(r) for r in rows]


def stats(db: Path | None = None) -> dict:
    with connect(db) as conn:
        total = conn.execute("SELECT COUNT(*) AS n FROM corpus_entries").fetchone()["n"]
        by_source = {
            r["source"]: r["n"]
            for r in conn.execute(
                "SELECT source, COUNT(*) AS n FROM corpus_entries GROUP BY source"
            )
        }
        by_severity = {
            (r["severity"] or "unspecified"): r["n"]
            for r in conn.execute(
                "SELECT severity, COUNT(*) AS n FROM corpus_entries GROUP BY severity"
            )
        }
        top_vuln_classes = [
            {"vuln_class": r["vuln_class"], "count": r["n"]}
            for r in conn.execute(
                """
                SELECT vuln_class, COUNT(*) AS n
                FROM corpus_vuln_classes
                GROUP BY vuln_class
                ORDER BY n DESC
                LIMIT 25
                """
            )
        ]
    return {
        "total": total,
        "by_source": by_source,
        "by_severity": by_severity,
        "top_vuln_classes": top_vuln_classes,
    }


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------


def _fts_escape(q: str) -> str:
    # Wrap each whitespace-separated token in double quotes so FTS5 treats it
    # as a literal phrase. This is permissive (any token matches) but safe.
    tokens = [t for t in q.split() if t]
    return " OR ".join(f'"{t.replace(chr(34), "")}"' for t in tokens) or '""'


def _dump_yaml(fm: CorpusEntryFrontmatter) -> str:
    import yaml

    data = fm.model_dump(mode="json", exclude_none=True)
    # Ensure datetimes are strings, not yaml's native timestamp form, for round-tripping
    return yaml.safe_dump(data, sort_keys=True, allow_unicode=True)
