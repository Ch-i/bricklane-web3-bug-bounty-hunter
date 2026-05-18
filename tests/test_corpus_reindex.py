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
