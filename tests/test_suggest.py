"""Tests for harness/suggest.py — composite scoring + ranking."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest

from harness import suggest
from harness.candidates import Candidate


def _now(offset_hours: float = 0) -> str:
    return (datetime.now(timezone.utc) + timedelta(hours=offset_hours)).isoformat()


def _cand(
    *,
    id: str = "c4-test",
    platform: str = "code4rena",
    triage_score: float | None = 8.0,
    payout_max_usd: int | None = 50_000,
    closes_at: str | None = None,
    audit_run_dirs: list | None = None,
    triage_status: str = "new",
) -> Candidate:
    return Candidate(
        id=id,
        platform=platform,
        kind="source",
        title=f"Test {id}",
        sourced_at=_now(-24),
        triage_score=triage_score,
        payout_max_usd=payout_max_usd,
        closes_at=closes_at or _now(168),  # 7d
        audit_run_dirs=audit_run_dirs or [],
        triage_status=triage_status,
    )


def test_payout_factor_monotonic():
    """Larger payouts must produce larger factors."""
    f_1k = suggest._payout_factor(1_000)
    f_100k = suggest._payout_factor(100_000)
    f_1m = suggest._payout_factor(1_000_000)
    f_10m = suggest._payout_factor(10_000_000)
    assert f_1k < f_100k < f_1m <= f_10m
    assert 0 <= f_10m <= 1.0


def test_payout_factor_unknown_is_moderate():
    assert 0.2 <= suggest._payout_factor(None) <= 0.5
    assert 0.2 <= suggest._payout_factor(0) <= 0.5


def test_urgency_factor_sweet_spot_at_5d():
    """5 days out should be the highest urgency factor."""
    u_5d, _ = suggest._urgency_factor(_now(120))   # 5d
    u_3w, _ = suggest._urgency_factor(_now(504))   # 21d
    u_6h, _ = suggest._urgency_factor(_now(6))     # 6h
    u_closed, _ = suggest._urgency_factor(_now(-24))  # past

    assert u_5d > u_3w
    assert u_5d > u_6h
    assert u_closed == 0.0


def test_urgency_factor_handles_missing_or_garbage():
    assert suggest._urgency_factor(None)[0] == 0.5
    assert suggest._urgency_factor("not-a-date")[0] == 0.5


def test_score_candidate_higher_stage1_wins_when_others_equal():
    c_lo = _cand(id="c-lo", triage_score=3.0)
    c_hi = _cand(id="c-hi", triage_score=9.0)
    assert suggest.score_candidate(c_hi).score > suggest.score_candidate(c_lo).score


def test_score_candidate_already_audited_penalized():
    c_fresh = _cand(id="c-fresh", audit_run_dirs=[])
    c_done = _cand(id="c-done", audit_run_dirs=["/some/audit/path"])
    assert suggest.score_candidate(c_fresh).score > suggest.score_candidate(c_done).score


def test_score_candidate_skip_status_heavily_penalized():
    c_new = _cand(id="c-new", triage_status="new")
    c_skip = _cand(id="c-skip", triage_status="skip")
    s_new = suggest.score_candidate(c_new).score
    s_skip = suggest.score_candidate(c_skip).score
    assert s_skip < s_new * 0.5  # skip penalty is 0.2x


def test_score_candidate_platform_priors_applied():
    """Code4rena should outrank Immunefi when all else equal."""
    c_c4 = _cand(id="c-c4", platform="code4rena")
    c_im = _cand(id="c-im", platform="immunefi")
    assert suggest.score_candidate(c_c4).score > suggest.score_candidate(c_im).score


def test_suggest_top_n_filters_audited_by_default():
    fresh = _cand(id="fresh", audit_run_dirs=[])
    audited = _cand(id="audited", audit_run_dirs=["/x"])
    with patch("harness.candidates.load_all", return_value=[fresh, audited]):
        out = suggest.suggest_top_n(10)
    ids = [s.candidate.id for s in out]
    assert "fresh" in ids
    assert "audited" not in ids


def test_suggest_top_n_include_audited_overrides():
    audited = _cand(id="audited", audit_run_dirs=["/x"])
    with patch("harness.candidates.load_all", return_value=[audited]):
        out = suggest.suggest_top_n(10, include_audited=True)
    assert len(out) == 1
    assert out[0].candidate.id == "audited"


def test_suggest_top_n_filters_closed_by_default():
    open_c = _cand(id="open", closes_at=_now(72))  # 3d
    closed = _cand(id="closed", closes_at=_now(-24))  # already past
    with patch("harness.candidates.load_all", return_value=[open_c, closed]):
        out = suggest.suggest_top_n(10)
    ids = [s.candidate.id for s in out]
    assert "open" in ids
    assert "closed" not in ids


def test_suggest_top_n_sorts_by_composite_descending():
    cands = [
        _cand(id="a", triage_score=2.0, payout_max_usd=1_000),
        _cand(id="b", triage_score=9.0, payout_max_usd=500_000),
        _cand(id="c", triage_score=5.0, payout_max_usd=50_000),
    ]
    with patch("harness.candidates.load_all", return_value=cands):
        out = suggest.suggest_top_n(10)
    # b should rank #1 (high stage1 + high payout); a should be last.
    ids = [s.candidate.id for s in out]
    assert ids[0] == "b"
    assert ids[-1] == "a"


def test_suggest_top_n_respects_min_stage1():
    cands = [
        _cand(id="weak", triage_score=2.0),
        _cand(id="strong", triage_score=9.0),
    ]
    with patch("harness.candidates.load_all", return_value=cands):
        out = suggest.suggest_top_n(10, min_stage1=5.0)
    assert [s.candidate.id for s in out] == ["strong"]


def test_suggest_top_n_filters_platform():
    cands = [
        _cand(id="c4", platform="code4rena"),
        _cand(id="sh", platform="sherlock"),
    ]
    with patch("harness.candidates.load_all", return_value=cands):
        out = suggest.suggest_top_n(10, platform="code4rena")
    assert [s.candidate.id for s in out] == ["c4"]


def test_suggest_reasoning_is_concise():
    c = _cand(id="x", triage_score=7.5, payout_max_usd=100_000, closes_at=_now(72))
    s = suggest.score_candidate(c)
    # Reasoning should be a short single-line, factor-tagged string
    assert "stage1=7.5" in s.reasoning
    assert "payout=$100,000" in s.reasoning
    assert "platform=code4rena" in s.reasoning
