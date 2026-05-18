"""Tests for harness.submissions — template rendering + log roundtrip."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from harness import submissions as sub
from harness.schema import Finding, FindingLocation


def _make_finding(**overrides):
    base = dict(
        title="Reentrancy in withdraw()",
        severity="High",
        location=[FindingLocation(file="src/Vault.sol", line_start=42, line_end=58)],
        description="External call precedes balance update; classic CEI violation.",
        impact="Attacker drains the vault in a single tx.",
        recommendation="Move state mutation before the external call; add nonReentrant.",
        citations=["swc-107", "synthesis-reentrancy-variants-..."],
        novel=False,
        confidence="high",
        discovered_by="claude",
        proof_of_concept="(prose PoC)",
    )
    base.update(overrides)
    return Finding.model_validate(base)


def test_render_c4_includes_severity_letter_and_location():
    f = _make_finding()
    out = sub.render_c4(f, "c4-test", Path("/tmp"))
    assert "[H] Reentrancy" in out
    assert "Lines of code" in out
    assert "src/Vault.sol#L42-L58" in out
    assert "swc-107" in out


def test_render_sherlock_has_summary_and_recommendation():
    f = _make_finding()
    out = sub.render_sherlock(f, "sherlock-test", Path("/tmp"))
    assert "## Summary" in out
    assert "## Recommendation" in out
    assert "**Severity:** High" in out


def test_render_immunefi_has_brief_and_impact():
    f = _make_finding()
    out = sub.render_immunefi(f, "immunefi-test", Path("/tmp"))
    assert "## Brief / Intro" in out
    assert "## Impact Details" in out


def test_render_c4_surfaces_filter_verdict():
    """When filter_info is passed, the rendered template should include the
    verdict + rationale so the submitter (and judge) see what the filter
    agent already evaluated."""
    f = _make_finding()
    filter_info = {"verdict": "ACCEPT", "rationale": "Funds at risk on real path; PoC reproduced."}
    out = sub.render_c4(f, "c4-test", Path("/tmp"), filter_info=filter_info)
    assert "Internal review" in out
    assert "ACCEPT" in out
    assert "Funds at risk on real path" in out


def test_render_sherlock_surfaces_filter_verdict():
    f = _make_finding()
    out = sub.render_sherlock(
        f, "sherlock-test", Path("/tmp"),
        filter_info={"verdict": "DOWNGRADE", "rationale": "view-only impact"},
    )
    assert "DOWNGRADE" in out
    assert "view-only impact" in out


def test_render_with_no_filter_info_unchanged():
    """Passing filter_info=None or missing should not break the template."""
    f = _make_finding()
    out_no = sub.render_c4(f, "c4-test", Path("/tmp"), filter_info=None)
    out_omit = sub.render_c4(f, "c4-test", Path("/tmp"))
    # The Internal-review block should not appear when no filter info
    assert "Internal review" not in out_no
    assert "Internal review" not in out_omit
    # Both forms should produce equivalent output
    assert out_no == out_omit


def test_cmd_submissions_filters(tmp_path, monkeypatch, capsys):
    """cmd_submissions should filter by candidate/outcome/platform and aggregate stats."""
    from harness import tui
    import argparse

    log_path = tmp_path / "submissions.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    rows = [
        {"id": "c1--bug1--c4", "candidate_id": "c1", "finding_title": "bug1",
         "finding_severity": "High", "run_dir": "x", "platform": "c4",
         "template_path": "x.md", "outcome": "accepted", "payout_usd": 5000,
         "created_at": "2026-05-10T12:00:00+00:00"},
        {"id": "c2--bug2--sherlock", "candidate_id": "c2", "finding_title": "bug2",
         "finding_severity": "Medium", "run_dir": "y", "platform": "sherlock",
         "template_path": "y.md", "outcome": "rejected", "payout_usd": None,
         "created_at": "2026-05-12T12:00:00+00:00"},
    ]
    log_path.write_text("\n".join(__import__("json").dumps(r) for r in rows) + "\n")

    monkeypatch.setattr(sub, "SUBMISSIONS_LOG", log_path)

    # No filter — should show both
    args = argparse.Namespace(candidate_id=None, outcome=None, platform=None, limit=30)
    tui.cmd_submissions(args)
    out = capsys.readouterr().out
    assert "bug1" in out
    assert "bug2" in out
    assert "$5,000" in out
    assert "accepted=1" in out
    assert "rejected=1" in out

    # Filter by outcome
    args = argparse.Namespace(candidate_id=None, outcome="accepted", platform=None, limit=30)
    tui.cmd_submissions(args)
    out = capsys.readouterr().out
    assert "bug1" in out
    assert "bug2" not in out


def test_cmd_submissions_empty_log(tmp_path, monkeypatch, capsys):
    from harness import tui
    import argparse

    log_path = tmp_path / "empty.jsonl"
    log_path.write_text("")
    monkeypatch.setattr(sub, "SUBMISSIONS_LOG", log_path)

    args = argparse.Namespace(candidate_id=None, outcome=None, platform=None, limit=30)
    rc = tui.cmd_submissions(args)
    assert rc == 0
    out = capsys.readouterr().out
    assert "No submissions match" in out


def test_export_run_passes_filter_info_to_renderer(tmp_path, monkeypatch):
    """End-to-end: scrutinize wrote filter info into findings.json; export
    should pass it through to the renderers."""
    run_dir = tmp_path / "audits" / "scrutinize-test"
    run_dir.mkdir(parents=True)
    finding_dict = {
        "title": "Reentrancy in withdraw",
        "severity": "High",
        "location": [{"file": "x.sol", "line_start": 1}],
        "description": "d", "impact": "i", "recommendation": "r",
        "citations": ["swc-107"], "novel": False,
        "confidence": "high", "discovered_by": "claude",
        # Filter info as written by scrutinize:
        "filter": {"verdict": "ACCEPT", "rationale": "real funds at risk"},
    }
    (run_dir / "findings.json").write_text(json.dumps([finding_dict]))
    monkeypatch.setattr(sub, "SUBMISSIONS_DIR", tmp_path / "subs")
    monkeypatch.setattr(sub, "SUBMISSIONS_LOG", tmp_path / "subs" / "submissions.jsonl")

    sub.export_run(run_dir, candidate_id="test-cand", platforms=["c4"], min_severity="Medium")

    out_files = list((tmp_path / "subs").rglob("*.md"))
    assert len(out_files) == 1
    body = out_files[0].read_text()
    assert "ACCEPT" in body
    assert "real funds at risk" in body


def test_export_run_writes_files_and_log(tmp_path, monkeypatch):
    # Stage a run dir with findings.json
    run_dir = tmp_path / "audits" / "test-run"
    run_dir.mkdir(parents=True)
    findings = [
        _make_finding(severity="Critical", title="Critical bug A"),
        _make_finding(severity="Low", title="Low bug B"),
    ]
    (run_dir / "findings.json").write_text(
        json.dumps([f.model_dump() for f in findings])
    )

    monkeypatch.setattr(sub, "SUBMISSIONS_DIR", tmp_path / "submissions")
    monkeypatch.setattr(sub, "SUBMISSIONS_LOG", tmp_path / "submissions" / "submissions.jsonl")

    records = sub.export_run(
        run_dir,
        candidate_id="c4-test",
        platforms=["c4", "sherlock"],
        min_severity="Medium",
    )
    # min_severity=Medium filters out the Low; 1 finding × 2 platforms = 2 records
    assert len(records) == 2
    assert {r.platform for r in records} == {"c4", "sherlock"}
    assert sub.SUBMISSIONS_LOG.exists()
    for r in records:
        assert Path(sub.REPO_ROOT / r.template_path if not r.template_path.startswith("/") else r.template_path)


def test_export_run_only_reproduced_filter(tmp_path, monkeypatch):
    run_dir = tmp_path / "audits" / "test-run"
    run_dir.mkdir(parents=True)
    findings = [
        _make_finding(severity="High", title="reproduced bug", poc_status="reproduced"),
        _make_finding(severity="High", title="unconfirmed bug", poc_status="unconfirmed"),
    ]
    (run_dir / "findings.json").write_text(
        json.dumps([f.model_dump() for f in findings])
    )

    monkeypatch.setattr(sub, "SUBMISSIONS_DIR", tmp_path / "submissions")
    monkeypatch.setattr(sub, "SUBMISSIONS_LOG", tmp_path / "submissions" / "submissions.jsonl")

    records = sub.export_run(
        run_dir,
        candidate_id="c4-test",
        platforms=["c4"],
        only_reproduced=True,
    )
    assert len(records) == 1
    assert records[0].finding_title == "reproduced bug"
