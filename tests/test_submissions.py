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
