"""Candidate persistence layer for the bounty-hunt workflow.

A Candidate is one bounty-eligible unit: a C4/Sherlock/Cantina contest, or
an Immunefi program. The kind discriminator separates source-only contests
(GitHub repo at a commit) from deployed-kind programs (on-chain addresses).

Storage:
  * eval/candidates.jsonl — append-only, canonical source of truth
  * eval/candidates.db    — derived sqlite for queries; rebuildable

Lifecycle (triage_status):
  new          → just ingested, not yet scored
  stage1       → Opus-ranked, in the queue
  stage2-done  → full audit completed, findings in audits/<run-dir>/
  submitted    → at least one finding submitted to a platform
  skipped      → manually marked as not worth pursuing
  expired      → contest closed, no submission
"""

from __future__ import annotations

import json
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from harness.corpus import REPO_ROOT

CANDIDATES_JSONL = REPO_ROOT / "eval" / "candidates.jsonl"
CANDIDATES_DB = REPO_ROOT / "eval" / "candidates.db"

Platform = Literal["c4", "sherlock", "cantina", "immunefi"]
Kind = Literal["source-only", "deployed"]
TriageStatus = Literal[
    "new", "stage1", "stage2-done", "submitted", "skipped", "expired"
]


@dataclass
class Candidate:
    """One bounty-eligible unit."""

    id: str                          # platform-stable, e.g. "c4-2026-05-aave-v4"
    platform: Platform
    kind: Kind
    title: str
    sourced_at: str                  # ISO 8601

    # Optional metadata
    payout_max_usd: int | None = None
    closes_at: str | None = None     # ISO 8601, for time-boxed contests

    # source-only kind
    repo_url: str | None = None
    commit: str | None = None
    scope_paths: list[str] = field(default_factory=list)
    out_of_scope_paths: list[str] = field(default_factory=list)
    local_path: str | None = None    # cloned location after sweep fetches it

    # deployed kind
    chain_id: int | None = None
    addresses: list[str] = field(default_factory=list)

    # Free-form context: README excerpts, docs links, prior audit reports
    notes: str = ""

    # Triage state (mutates over time across sweep runs)
    triage_status: TriageStatus = "new"
    triage_score: float | None = None
    triage_rationale: str | None = None
    triage_top_suspects: list[dict] = field(default_factory=list)
    triage_skip_reasons: list[str] = field(default_factory=list)
    last_triaged_at: str | None = None

    # Cross-refs
    audit_run_dirs: list[str] = field(default_factory=list)
    submission_ids: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# jsonl persistence (canonical source of truth)
# ---------------------------------------------------------------------------


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_all() -> list[Candidate]:
    """Load every candidate from jsonl. Last-write-wins on duplicate id."""
    if not CANDIDATES_JSONL.exists():
        return []
    by_id: dict[str, Candidate] = {}
    with CANDIDATES_JSONL.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            c = Candidate(**d)
            by_id[c.id] = c
    return list(by_id.values())


def append(candidates: list[Candidate]) -> None:
    """Append candidates to the jsonl log (no dedup at write time)."""
    CANDIDATES_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with CANDIDATES_JSONL.open("a") as f:
        for c in candidates:
            f.write(json.dumps(asdict(c)) + "\n")


def upsert(candidate: Candidate) -> None:
    """Append a fresh row representing the latest state of one candidate."""
    append([candidate])


def get(candidate_id: str) -> Candidate | None:
    for c in load_all():
        if c.id == candidate_id:
            return c
    return None


def diff_against_log(fresh: list[Candidate]) -> tuple[list[Candidate], list[Candidate]]:
    """Compare a fresh list against the jsonl. Return (new, status_changed)."""
    existing = {c.id: c for c in load_all()}
    new: list[Candidate] = []
    changed: list[Candidate] = []
    for c in fresh:
        prior = existing.get(c.id)
        if prior is None:
            new.append(c)
        elif (prior.closes_at != c.closes_at) or (prior.payout_max_usd != c.payout_max_usd):
            changed.append(c)
    return new, changed


# ---------------------------------------------------------------------------
# sqlite mirror (rebuildable from jsonl)
# ---------------------------------------------------------------------------


DDL = """
CREATE TABLE IF NOT EXISTS candidates (
    id              TEXT PRIMARY KEY,
    platform        TEXT NOT NULL,
    kind            TEXT NOT NULL,
    title           TEXT NOT NULL,
    sourced_at      TEXT NOT NULL,
    payout_max_usd  INTEGER,
    closes_at       TEXT,
    repo_url        TEXT,
    commit_sha      TEXT,
    scope_paths     TEXT,
    chain_id        INTEGER,
    addresses       TEXT,
    triage_status   TEXT NOT NULL,
    triage_score    REAL,
    triage_rationale TEXT,
    last_triaged_at TEXT,
    notes           TEXT,
    raw_json        TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_candidates_platform ON candidates(platform);
CREATE INDEX IF NOT EXISTS idx_candidates_triage_status ON candidates(triage_status);
CREATE INDEX IF NOT EXISTS idx_candidates_triage_score ON candidates(triage_score DESC);
CREATE INDEX IF NOT EXISTS idx_candidates_closes_at ON candidates(closes_at);
"""


@contextmanager
def connect(path: Path | None = None) -> Iterator[sqlite3.Connection]:
    p = path or CANDIDATES_DB
    p.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(p)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def reindex() -> int:
    """Drop + recreate the sqlite mirror from the on-disk jsonl."""
    if CANDIDATES_DB.exists():
        CANDIDATES_DB.unlink()
    with connect() as conn:
        conn.executescript(DDL)
        n = 0
        for c in load_all():
            d = asdict(c)
            conn.execute(
                """
                INSERT OR REPLACE INTO candidates
                  (id, platform, kind, title, sourced_at, payout_max_usd,
                   closes_at, repo_url, commit_sha, scope_paths,
                   chain_id, addresses, triage_status, triage_score,
                   triage_rationale, last_triaged_at, notes, raw_json)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    c.id, c.platform, c.kind, c.title, c.sourced_at,
                    c.payout_max_usd, c.closes_at, c.repo_url, c.commit,
                    json.dumps(c.scope_paths), c.chain_id,
                    json.dumps(c.addresses), c.triage_status, c.triage_score,
                    c.triage_rationale, c.last_triaged_at, c.notes,
                    json.dumps(d),
                ),
            )
            n += 1
        return n


def query_queue(
    *,
    platform: Platform | None = None,
    status: TriageStatus | None = None,
    min_score: float | None = None,
    limit: int = 50,
) -> list[Candidate]:
    """Return candidates ordered by triage_score DESC, filtered."""
    if not CANDIDATES_DB.exists():
        reindex()
    where = []
    params: list = []
    if platform:
        where.append("platform = ?")
        params.append(platform)
    if status:
        where.append("triage_status = ?")
        params.append(status)
    if min_score is not None:
        where.append("triage_score >= ?")
        params.append(min_score)
    sql = "SELECT raw_json FROM candidates"
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY triage_score DESC NULLS LAST, sourced_at DESC LIMIT ?"
    params.append(limit)
    with connect() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [Candidate(**json.loads(r["raw_json"])) for r in rows]
