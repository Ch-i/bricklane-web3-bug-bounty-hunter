"""Tests for harness/digest.py — time-windowed activity report."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

import pytest

from harness import digest
from harness.candidates import Candidate


def _iso(offset_hours: float = 0) -> str:
    return (datetime.now(timezone.utc) + timedelta(hours=offset_hours)).isoformat()


def _cand(*, id: str, sourced_hours_ago: float = 12, triaged_hours_ago: float | None = None) -> Candidate:
    return Candidate(
        id=id,
        platform="code4rena",
        kind="source",
        title=f"Test {id}",
        sourced_at=_iso(-sourced_hours_ago),
        triage_score=8.0,
        last_triaged_at=_iso(-triaged_hours_ago) if triaged_hours_ago is not None else None,
    )


def test_new_candidates_within_window():
    cands = [
        _cand(id="recent", sourced_hours_ago=6),     # in 24h window
        _cand(id="too-old", sourced_hours_ago=48),   # outside
        _cand(id="re-triaged", sourced_hours_ago=72, triaged_hours_ago=3),  # was triaged in window
    ]
    with patch("harness.candidates.load_all", return_value=cands):
        fresh = digest._new_candidates(digest._since(24))
    ids = {c["id"] for c in fresh}
    assert "recent" in ids
    assert "too-old" not in ids
    assert "re-triaged" in ids


def test_new_candidates_flags_new_vs_triaged():
    cands = [
        _cand(id="newish", sourced_hours_ago=2),
        _cand(id="re-rank", sourced_hours_ago=72, triaged_hours_ago=3),
    ]
    with patch("harness.candidates.load_all", return_value=cands):
        fresh = digest._new_candidates(digest._since(24))
    by_id = {c["id"]: c for c in fresh}
    assert by_id["newish"]["is_new"] is True
    assert by_id["newish"]["was_triaged"] is False
    assert by_id["re-rank"]["is_new"] is False
    assert by_id["re-rank"]["was_triaged"] is True


def test_recent_audit_runs_finds_scrutinize_and_audit_dirs(tmp_path, monkeypatch):
    audits = tmp_path / "audits"
    audits.mkdir()
    # An audit dir (has prep.json) — recent
    a1 = audits / "vulnerable-sol-20260518"
    a1.mkdir()
    (a1 / "prep.json").write_text("{}")
    (a1 / "findings.json").write_text(json.dumps([
        {"title": "X", "severity": "High", "poc_status": "reproduced"},
        {"title": "Y", "severity": "Low", "poc_status": "not-attempted"},
    ]))
    # A scrutinize dir
    s1 = audits / "scrutinize-foo-20260518"
    s1.mkdir()
    (s1 / "scrutinize-report.md").write_text("# report")
    # A deep-dive dir
    d1 = audits / "deep-dive-bar-20260518"
    d1.mkdir()
    (d1 / "deep-dive-report.md").write_text("# dd")
    # A non-audit dir — should be ignored
    other = audits / "not-an-audit"
    other.mkdir()
    (other / "something.txt").write_text("")

    monkeypatch.setattr(digest, "REPO_ROOT", tmp_path)
    out = digest._recent_audit_runs(digest._since(1))
    names = {r["name"] for r in out}
    assert "vulnerable-sol-20260518" in names
    assert "scrutinize-foo-20260518" in names
    assert "deep-dive-bar-20260518" in names
    assert "not-an-audit" not in names

    # Verify metadata extraction
    by_name = {r["name"]: r for r in out}
    assert by_name["vulnerable-sol-20260518"]["kind"] == "audit"
    assert by_name["vulnerable-sol-20260518"]["n_findings"] == 2
    assert by_name["vulnerable-sol-20260518"]["has_pocs"] is True
    assert by_name["scrutinize-foo-20260518"]["kind"] == "scrutinize"
    assert by_name["scrutinize-foo-20260518"]["has_master_report"] is True
    assert by_name["deep-dive-bar-20260518"]["kind"] == "deep-dive"


def test_recent_audit_runs_excludes_old_dirs(tmp_path, monkeypatch):
    import os
    audits = tmp_path / "audits"
    audits.mkdir()
    old = audits / "scrutinize-old"
    old.mkdir()
    (old / "scrutinize-report.md").write_text("# x")
    # Set the dir mtime to a week ago
    week_ago = datetime.now().timestamp() - 7 * 24 * 3600
    os.utime(old, (week_ago, week_ago))

    monkeypatch.setattr(digest, "REPO_ROOT", tmp_path)
    out = digest._recent_audit_runs(digest._since(1))
    assert all(r["name"] != "scrutinize-old" for r in out)


def test_new_submissions_filters_by_window(tmp_path, monkeypatch):
    subs_dir = tmp_path / "submissions"
    subs_dir.mkdir()
    log_path = subs_dir / "submissions.jsonl"
    rows = [
        {"platform": "c4", "title": "Old sub", "severity": "High",
         "outcome": "submitted", "submitted_at": _iso(-72)},  # outside
        {"platform": "sherlock", "title": "Fresh sub", "severity": "Critical",
         "outcome": "validated", "submitted_at": _iso(-3)},   # inside
    ]
    log_path.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    monkeypatch.setattr(digest, "REPO_ROOT", tmp_path)
    out = digest._new_submissions(digest._since(24))
    assert len(out) == 1
    assert out[0]["title"] == "Fresh sub"


def test_new_corpus_entries_finds_synthesis_notes(tmp_path, monkeypatch):
    synth_dir = tmp_path / "corpus" / "synthesis"
    synth_dir.mkdir(parents=True)
    (synth_dir / "fresh-topic.md").write_text(
        'title: "Fresh topic synthesis"\n\n# body line 1\n# body line 2\n'
    )
    monkeypatch.setattr(digest, "REPO_ROOT", tmp_path)
    out = digest._new_corpus_entries(digest._since(24))
    titles = [n["title"] for n in out["synthesis_notes"]]
    assert "Fresh topic synthesis" in titles


def test_generate_digest_assembles_all_sections(tmp_path, monkeypatch):
    """Smoke test: generate_digest returns a dict with all expected keys."""
    monkeypatch.setattr(digest, "REPO_ROOT", tmp_path)
    with patch("harness.candidates.load_all", return_value=[]):
        d = digest.generate_digest(hours=24)
    assert "window_hours" in d
    assert "since" in d
    assert "now" in d
    assert d["candidates"] == []
    assert d["audit_runs"] == []
    assert d["submissions"] == []
    assert "corpus" in d


def test_render_digest_handles_empty_digest(capsys, tmp_path, monkeypatch):
    """Empty digest should print a helpful "nothing happened" hint."""
    monkeypatch.setattr(digest, "REPO_ROOT", tmp_path)
    with patch("harness.candidates.load_all", return_value=[]):
        d = digest.generate_digest(hours=24)
    digest.render_digest(d)
    captured = capsys.readouterr()
    assert "No activity in the last" in captured.out


def test_render_digest_emits_next_steps_when_unranked_cands_exist(capsys):
    """If user has fresh unranked candidates, Next steps should mention Stage 1."""
    d = {
        "window_hours": 24,
        "since": _iso(-24),
        "now": _iso(),
        "candidates": [{
            "id": f"c4-x{i}", "platform": "code4rena", "title": "fresh",
            "payout_max_usd": None, "triage_score": None, "triage_status": "new",
            "is_new": True, "was_triaged": False, "local_path": None,
        } for i in range(8)],
        "audit_runs": [],
        "submissions": [],
        "corpus": {"synthesis_notes": [], "ingested_count": 0, "by_source": {}},
    }
    digest.render_digest(d)
    captured = capsys.readouterr()
    assert "Next steps" in captured.out
    assert "have no Stage-1 rank" in captured.out
    assert "w3s sweep" in captured.out


def test_render_digest_emits_next_steps_for_unwrapped_deep_dives(capsys):
    """A deep-dive run without master report → suggest scrutinize."""
    d = {
        "window_hours": 24,
        "since": _iso(-24),
        "now": _iso(),
        "candidates": [],
        "audit_runs": [{
            "name": "deep-dive-x", "kind": "deep-dive",
            "mtime": _iso(-2), "n_findings": 10,
            "has_pocs": False, "has_master_report": False,
        }],
        "submissions": [],
        "corpus": {"synthesis_notes": [], "ingested_count": 0, "by_source": {}},
    }
    digest.render_digest(d)
    captured = capsys.readouterr()
    assert "Next steps" in captured.out
    assert "lack a master scrutinize report" in captured.out
    assert "w3s scrutinize" in captured.out


def test_render_digest_emits_next_steps_for_unsubmitted_scrutinize(capsys):
    """A scrutinize run without submissions → suggest reviewing + submitting."""
    d = {
        "window_hours": 24,
        "since": _iso(-24),
        "now": _iso(),
        "candidates": [],
        "audit_runs": [{
            "name": "scrutinize-x", "kind": "scrutinize",
            "mtime": _iso(-2), "n_findings": 5,
            "has_pocs": True, "has_master_report": True,
        }],
        "submissions": [],
        "corpus": {"synthesis_notes": [], "ingested_count": 0, "by_source": {}},
    }
    digest.render_digest(d)
    captured = capsys.readouterr()
    assert "0 submissions filed" in captured.out
    assert "w3s submit" in captured.out


def test_render_digest_emits_candidate_table(capsys):
    """Candidate table should include the candidate id + payout."""
    d = {
        "window_hours": 24,
        "since": _iso(-24),
        "now": _iso(),
        "candidates": [{
            "id": "c4-mytarget",
            "platform": "code4rena",
            "title": "MyTarget Audit",
            "payout_max_usd": 100_000,
            "triage_score": 8.5,
            "triage_status": "new",
            "is_new": True,
            "was_triaged": True,
            "local_path": "/x",
        }],
        "audit_runs": [],
        "submissions": [],
        "corpus": {"synthesis_notes": [], "ingested_count": 0, "by_source": {}},
    }
    digest.render_digest(d)
    captured = capsys.readouterr()
    assert "c4-mytarget" in captured.out
    assert "$100,000" in captured.out
    assert "1 new ingested" in captured.out
