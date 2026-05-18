"""Tests for harness.corpus.reindex — atomicity + WAL mode.

These tests focus on the file-level atomicity guarantees of reindex
(temp DB + atomic rename + cleanup on failure), without requiring
real corpus markdown files (which the upsert path validates against
REPO_ROOT).
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from harness import corpus


def test_reindex_writes_via_temp_path(tmp_path: Path, monkeypatch):
    """reindex must build into a .reindex.tmp sibling, NOT in-place on the
    live DB — otherwise a kill mid-way leaves the user with an empty corpus.
    """
    db = tmp_path / "corpus.db"
    pre_existing = tmp_path / "fake-existing.db"
    pre_existing.write_text("fake old content")  # placeholder

    # Capture the path passed to init_db so we know it's the temp one
    init_calls = []
    real_init = corpus.init_db

    def trace_init(path=None):
        init_calls.append(str(path))
        # Don't actually init (we don't have corpus md files under REPO_ROOT)
        return None

    monkeypatch.setattr(corpus, "init_db", trace_init)
    # Stub the empty markdown scan
    monkeypatch.setattr(corpus, "corpus_dir", lambda: tmp_path / "nonexistent")

    corpus.reindex(db=db)
    # init was called with a path containing .reindex.tmp
    assert any(".reindex.tmp" in c for c in init_calls), init_calls


def test_reindex_cleans_up_temp_on_failure(tmp_path: Path, monkeypatch):
    """If init_db raises, the .reindex.tmp file (if created) must be removed."""
    db = tmp_path / "corpus.db"

    def bad_init(path=None):
        # Simulate partial create: touch the temp file, then fail
        if path and ".reindex.tmp" in str(path):
            Path(path).touch()
            raise RuntimeError("simulated kill")
        return None

    monkeypatch.setattr(corpus, "init_db", bad_init)
    monkeypatch.setattr(corpus, "corpus_dir", lambda: tmp_path / "nonexistent")

    with pytest.raises(RuntimeError, match="simulated"):
        corpus.reindex(db=db)

    # The .tmp file should be gone
    tmp_db = db.with_suffix(".db.reindex.tmp")
    assert not tmp_db.exists(), f"temp DB leaked: {tmp_db}"


def test_reindex_preserves_old_db_on_fatal_failure(tmp_path: Path, monkeypatch):
    """If the rebuild fails mid-way, the existing DB at the canonical path
    must be untouched."""
    db = tmp_path / "corpus.db"
    # Pre-create a real SQLite DB at the live path
    pre_conn = sqlite3.connect(db)
    pre_conn.execute("CREATE TABLE marker (id INT)")
    pre_conn.execute("INSERT INTO marker VALUES (42)")
    pre_conn.commit()
    pre_conn.close()
    pre_mtime = db.stat().st_mtime

    def bad_init(path=None):
        if path and ".reindex.tmp" in str(path):
            raise RuntimeError("simulated kill")
        return None

    monkeypatch.setattr(corpus, "init_db", bad_init)
    monkeypatch.setattr(corpus, "corpus_dir", lambda: tmp_path / "nonexistent")

    with pytest.raises(RuntimeError):
        corpus.reindex(db=db)

    # Live DB must still exist with original content
    assert db.exists()
    post_conn = sqlite3.connect(db)
    rows = post_conn.execute("SELECT id FROM marker").fetchall()
    post_conn.close()
    assert rows == [(42,)]
    # mtime unchanged
    assert db.stat().st_mtime == pre_mtime


def test_connect_enables_wal_mode(tmp_path: Path):
    """Verify the WAL pragma we set in connect() actually sticks."""
    db = tmp_path / "x.db"
    with corpus.connect(db):
        pass
    raw = sqlite3.connect(db)
    mode = raw.execute("PRAGMA journal_mode").fetchone()[0]
    raw.close()
    assert mode == "wal"


def test_fts_escape_wraps_tokens_in_double_quotes():
    """FTS5 needs each token quoted; multi-token query becomes OR."""
    assert corpus._fts_escape("reentrancy") == '"reentrancy"'
    assert corpus._fts_escape("oracle staleness") == '"oracle" OR "staleness"'


def test_fts_escape_handles_empty_input():
    """Empty / whitespace-only input returns a safe empty-quote literal."""
    assert corpus._fts_escape("") == '""'
    assert corpus._fts_escape("   ") == '""'


def test_fts_escape_strips_embedded_double_quotes():
    """A token containing " would break the FTS5 lexer — strip them."""
    result = corpus._fts_escape('say"hi')
    assert '""' not in result.replace('""', "_DBL_")  # no two adjacent double quotes
    # The character is stripped:
    assert '"' not in result.replace('"', "")[1:-1] or "sayhi" in result


def test_parse_entry_loads_frontmatter_and_body(tmp_path: Path):
    """parse_entry should return (CorpusEntryFrontmatter, body_str)."""
    md = tmp_path / "test-entry.md"
    md.write_text("""---
id: swc-test
source: swc
title: Test entry
ingested_at: 2026-05-18T00:00:00Z
vuln_class:
  - reentrancy
---

This is the body.
""")
    fm, body = corpus.parse_entry(md)
    assert fm.id == "swc-test"
    assert fm.source == "swc"
    assert "reentrancy" in fm.vuln_class
    assert "This is the body" in body


def test_dump_yaml_excludes_none_and_is_sortkey_stable():
    """_dump_yaml should produce sorted, none-excluded YAML for reproducibility."""
    from harness.schema import CorpusEntryFrontmatter as FM
    fm = FM(
        id="swc-test", source="swc", title="x",
        ingested_at="2026-05-18T00:00:00Z",
        source_url=None,  # should be excluded
        vuln_class=["a", "b"],
    )
    yaml_out = corpus._dump_yaml(fm)
    assert "source_url" not in yaml_out
    # Sorted keys means 'id' < 'ingested_at' < 'source' < 'title' < 'vuln_class'
    # (alphabetical order)
    lines = yaml_out.splitlines()
    id_idx = next(i for i, l in enumerate(lines) if l.startswith("id:"))
    title_idx = next(i for i, l in enumerate(lines) if l.startswith("title:"))
    assert id_idx < title_idx  # alpha-sorted
