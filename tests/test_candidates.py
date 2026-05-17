"""Tests for harness.candidates — Candidate persistence + diff."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from harness import candidates as cs
from harness.candidates import Candidate


@pytest.fixture
def isolated_store(tmp_path, monkeypatch):
    """Point CANDIDATES_JSONL + CANDIDATES_DB at tmp_path."""
    jsonl = tmp_path / "candidates.jsonl"
    db = tmp_path / "candidates.db"
    monkeypatch.setattr(cs, "CANDIDATES_JSONL", jsonl)
    monkeypatch.setattr(cs, "CANDIDATES_DB", db)
    return tmp_path


def _make(id_="c4-test", platform="c4", **kw):
    return Candidate(
        id=id_,
        platform=platform,
        kind=kw.get("kind", "source-only"),
        title=kw.get("title", "test contest"),
        sourced_at=kw.get("sourced_at", "2026-05-18T00:00:00+00:00"),
        payout_max_usd=kw.get("payout_max_usd"),
        repo_url=kw.get("repo_url"),
        scope_paths=kw.get("scope_paths", []),
    )


def test_append_and_load_roundtrip(isolated_store):
    c1 = _make("c4-a")
    c2 = _make("c4-b")
    cs.append([c1, c2])
    loaded = cs.load_all()
    assert {c.id for c in loaded} == {"c4-a", "c4-b"}


def test_upsert_overwrites_last_write_wins(isolated_store):
    c1 = _make("c4-a", title="first")
    cs.upsert(c1)
    c2 = _make("c4-a", title="second")
    cs.upsert(c2)
    loaded = cs.load_all()
    assert len(loaded) == 1
    assert loaded[0].title == "second"


def test_diff_against_log_identifies_new_and_changed(isolated_store):
    cs.append([_make("c4-a", payout_max_usd=100_000)])
    fresh = [
        _make("c4-a", payout_max_usd=150_000),   # changed payout
        _make("c4-b"),                            # new
    ]
    new, changed = cs.diff_against_log(fresh)
    assert [c.id for c in new] == ["c4-b"]
    assert [c.id for c in changed] == ["c4-a"]


def test_reindex_rebuilds_sqlite_from_jsonl(isolated_store):
    cs.append([_make("c4-a"), _make("c4-b")])
    n = cs.reindex()
    assert n == 2
    assert isolated_store.joinpath("candidates.db").exists()


def test_query_queue_orders_by_score_desc(isolated_store):
    c_hi = _make("c4-hi"); c_hi.triage_score = 9; c_hi.triage_status = "stage1"
    c_md = _make("c4-md"); c_md.triage_score = 5; c_md.triage_status = "stage1"
    c_lo = _make("c4-lo"); c_lo.triage_score = 2; c_lo.triage_status = "stage1"
    cs.append([c_lo, c_md, c_hi])
    cs.reindex()
    out = cs.query_queue(limit=10)
    assert [c.id for c in out] == ["c4-hi", "c4-md", "c4-lo"]


def test_query_queue_respects_min_score(isolated_store):
    c_hi = _make("c4-hi"); c_hi.triage_score = 9
    c_lo = _make("c4-lo"); c_lo.triage_score = 2
    cs.append([c_lo, c_hi])
    cs.reindex()
    out = cs.query_queue(min_score=5, limit=10)
    assert [c.id for c in out] == ["c4-hi"]
