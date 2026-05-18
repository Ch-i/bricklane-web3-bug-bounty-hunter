"""Tests for cmd_autoscrutinize — end-to-end orchestration of suggest + scrutinize."""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

import pytest

from harness import tui
from harness.candidates import Candidate
from harness.suggest import Suggestion


def _iso(offset_hours: float = 0) -> str:
    return (datetime.now(timezone.utc) + timedelta(hours=offset_hours)).isoformat()


def _cand(local_path: str | None = "/tmp/repos/aave-v4") -> Candidate:
    return Candidate(
        id="c4-aave",
        platform="code4rena",
        kind="source",
        title="Aave V4",
        sourced_at=_iso(-1),
        triage_score=8.0,
        local_path=local_path,
        scope_paths=["src/core"],
        closes_at=_iso(168),
    )


def _args(**kw) -> argparse.Namespace:
    ns = argparse.Namespace(
        top=1, platform=None, min_stage1=None, out=None,
        model="opus", max_functions=None, materialize_min_severity="High",
        single_model=False, no_audit_pocs=False,
        skip_audit=False, skip_deep_dive=False, skip_cross_fn=False,
        skip_materialize=False, skip_filter=False,
        dry_run_first=False, dry_run=False,
    )
    for k, v in kw.items():
        setattr(ns, k, v)
    return ns


def test_autoscrutinize_picks_top_then_calls_scrutinize(monkeypatch):
    cand = _cand()
    sug = Suggestion(candidate=cand, score=0.5, components={}, reasoning="x")
    captured = {}

    def fake_scrutinize(target, **kw):
        captured["target"] = target
        captured.update(kw)
        return Path("/tmp/r.md")

    with patch("harness.suggest.suggest_top_n", return_value=[sug]):
        with patch("harness.scrutinize.scrutinize", side_effect=fake_scrutinize):
            rc = tui.cmd_autoscrutinize(_args())
    assert rc == 0
    assert captured["target"] == "/tmp/repos/aave-v4"
    assert captured["scope"] == "src/core"


def test_autoscrutinize_no_candidates_returns_1(capsys):
    with patch("harness.suggest.suggest_top_n", return_value=[]):
        rc = tui.cmd_autoscrutinize(_args())
    assert rc == 1
    captured = capsys.readouterr()
    assert "No candidates" in captured.out


def test_autoscrutinize_missing_local_path_returns_1(capsys):
    cand = _cand(local_path=None)
    sug = Suggestion(candidate=cand, score=0.5, components={}, reasoning="x")
    with patch("harness.suggest.suggest_top_n", return_value=[sug]):
        rc = tui.cmd_autoscrutinize(_args())
    assert rc == 1
    captured = capsys.readouterr()
    assert "no local_path" in captured.out


def test_autoscrutinize_dry_run_exits_after_preview():
    cand = _cand()
    sug = Suggestion(candidate=cand, score=0.5, components={}, reasoning="x")
    called_real = {"hit": False}

    def fake_scrutinize(target, **kw):
        if kw.get("dry_run"):
            return None
        called_real["hit"] = True
        return Path("/tmp/r.md")

    with patch("harness.suggest.suggest_top_n", return_value=[sug]):
        with patch("harness.scrutinize.scrutinize", side_effect=fake_scrutinize):
            rc = tui.cmd_autoscrutinize(_args(dry_run=True))
    assert rc == 0
    # Real scrutinize must NOT have been called when dry_run=True
    assert called_real["hit"] is False


def test_autoscrutinize_dry_run_first_runs_both():
    """With --dry-run-first, the preview runs THEN the real scrutinize runs."""
    cand = _cand()
    sug = Suggestion(candidate=cand, score=0.5, components={}, reasoning="x")
    call_log = []

    def fake_scrutinize(target, **kw):
        call_log.append("dry" if kw.get("dry_run") else "real")
        return None if kw.get("dry_run") else Path("/tmp/r.md")

    with patch("harness.suggest.suggest_top_n", return_value=[sug]):
        with patch("harness.scrutinize.scrutinize", side_effect=fake_scrutinize):
            rc = tui.cmd_autoscrutinize(_args(dry_run_first=True))
    assert rc == 0
    assert call_log == ["dry", "real"]


def test_autoscrutinize_passes_phase_skips_through():
    cand = _cand()
    sug = Suggestion(candidate=cand, score=0.5, components={}, reasoning="x")
    captured = {}

    def fake_scrutinize(target, **kw):
        captured.update(kw)
        return Path("/tmp/r.md")

    with patch("harness.suggest.suggest_top_n", return_value=[sug]):
        with patch("harness.scrutinize.scrutinize", side_effect=fake_scrutinize):
            tui.cmd_autoscrutinize(_args(
                skip_audit=True, skip_materialize=True, single_model=True,
            ))
    assert captured["skip_audit"] is True
    assert captured["skip_materialize"] is True
    assert captured["audit_multimodel"] is False  # --single-model inverts the flag
