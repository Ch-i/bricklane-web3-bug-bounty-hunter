"""Tests for harness/scrutinize.py — focus on the master report assembly.

Scrutinize itself orchestrates real subprocess-level work (claude/codex/forge)
that can't be unit tested in isolation, so we test:
  1. _master_report aggregates correctly from realistic inputs
  2. CLI flag wiring routes to scrutinize.scrutinize() with the right kwargs
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from harness import scrutinize


def test_master_report_with_all_phases(tmp_path: Path):
    scrutinize_dir = tmp_path / "scrutinize-run"
    scrutinize_dir.mkdir()
    target = tmp_path / "src" / "Vault.sol"
    target.parent.mkdir()
    target.write_text("// dummy")

    # Phase 1 fixture: audit run with findings + report
    audit_dir = scrutinize_dir / "audit"
    audit_dir.mkdir()
    (audit_dir / "report.md").write_text("# audit report")
    (audit_dir / "findings.json").write_text(json.dumps([
        {"title": "stale oracle", "severity": "High", "poc_status": "reproduced"},
        {"title": "missing access control", "severity": "Critical", "poc_status": "compile-failed"},
        {"title": "unchecked return", "severity": "Medium", "poc_status": "not-attempted"},
    ]))

    # Phase 2 fixture: deep-dive run
    dd_dir = scrutinize_dir / "deep-dive"
    dd_dir.mkdir()
    (dd_dir / "deep-dive-report.md").write_text("# dd")
    (dd_dir / "per-function.jsonl").write_text("\n".join([
        json.dumps({"function_id": "src/Vault.sol::deposit",
                    "candidate_vulnerabilities": [
                        {"title": "v1", "severity": "High"},
                        {"title": "v2", "severity": "Medium"},
                    ]}),
        json.dumps({"function_id": "src/Vault.sol::withdraw",
                    "candidate_vulnerabilities": [{"title": "v3", "severity": "Critical"}]}),
    ]))
    (dd_dir / "cross-function.jsonl").write_text(json.dumps({
        "vulnerabilities": [{"title": "cross-v1"}, {"title": "cross-v2"}],
    }))

    # Phase 3 fixture: materialized PoCs
    mat_path = scrutinize_dir / "materialized.json"
    mat_path.write_text(json.dumps([
        {"title": "v1", "severity": "High", "poc_status": "reproduced",
         "poc_artifacts": {"test_path": "test/__web3sentinel_pocs__/V1.t.sol"}},
        {"title": "v3", "severity": "Critical", "poc_status": "compile-failed"},
    ]))

    # Phase 4 fixture: filter verdicts
    filter_path = scrutinize_dir / "filter-verdicts.json"
    filter_path.write_text(json.dumps([
        {"title": "stale oracle", "severity": "High",
         "filter": {"verdict": "ACCEPT", "rationale": "real funds at risk"}},
        {"title": "missing access control", "severity": "Critical",
         "filter": {"verdict": "ACCEPT", "rationale": "anyone can drain"}},
        {"title": "unchecked return", "severity": "Medium",
         "filter": {"verdict": "DOWNGRADE", "rationale": "view-only impact"}},
    ]))

    out = scrutinize._master_report(
        target=target,
        scrutinize_dir=scrutinize_dir,
        audit_run_dir=audit_dir,
        deep_dive_run_dir=dd_dir,
        filter_results_path=filter_path,
        materialized_path=mat_path,
        elapsed_s=125,
    )

    assert out.exists()
    body = out.read_text()
    # Header + timing
    assert "# Scrutinize report" in body
    assert "Vault.sol" in body
    assert "Total wall time: 125s" in body

    # Phase summaries
    assert "## 1. Multi-model audit" in body
    assert "Findings: 3" in body
    assert "High=1" in body
    assert "Critical=1" in body
    assert "Medium=1" in body

    assert "## 2. Deep-dive" in body
    assert "Functions analyzed: 2" in body
    assert "Candidate vulnerabilities (per-fn): 3" in body
    assert "Cross-function vulnerabilities: 2" in body

    assert "## 3. Materialized PoCs" in body
    assert "Materialized: 2" in body
    assert "reproduced=1" in body
    assert "compile-failed=1" in body
    # Reproduced should be highlighted
    assert "✓ Reproduced candidates" in body
    assert "V1.t.sol" in body

    assert "## 4. Filter verdicts" in body
    assert "ACCEPT=2" in body
    assert "DOWNGRADE=1" in body
    assert "Submission-ready" in body
    assert "stale oracle" in body
    assert "real funds at risk" in body


def test_master_report_handles_missing_phases(tmp_path: Path):
    target = tmp_path / "Empty.sol"
    target.write_text("// dummy")
    out = scrutinize._master_report(
        target=target,
        scrutinize_dir=tmp_path,
        audit_run_dir=None,
        deep_dive_run_dir=None,
        filter_results_path=None,
        materialized_path=None,
        elapsed_s=5,
    )
    body = out.read_text()
    # Every section should still be present and self-label "skipped"
    assert "## 1. Multi-model audit" in body
    assert "## 2. Deep-dive" in body
    assert "## 3. Materialized PoCs" in body
    assert "## 4. Filter verdicts" in body
    assert body.count("_(skipped") >= 3


def test_master_report_tolerates_empty_findings_files(tmp_path: Path):
    """Run dirs exist but findings.json is missing or empty — should not crash."""
    target = tmp_path / "x.sol"
    target.write_text("//")
    audit_dir = tmp_path / "a"
    audit_dir.mkdir()
    (audit_dir / "report.md").write_text("# audit")
    # No findings.json

    dd_dir = tmp_path / "dd"
    dd_dir.mkdir()
    (dd_dir / "deep-dive-report.md").write_text("# dd")
    # No per-function.jsonl

    mat = tmp_path / "mat.json"
    mat.write_text(json.dumps([]))

    out = scrutinize._master_report(
        target=target,
        scrutinize_dir=tmp_path,
        audit_run_dir=audit_dir,
        deep_dive_run_dir=dd_dir,
        filter_results_path=None,
        materialized_path=mat,
        elapsed_s=10,
    )
    body = out.read_text()
    # Should produce the doc even with malformed/empty inputs
    assert "# Scrutinize report" in body
    # Empty materialized = no severity threshold met
    assert "no candidates met the materialization severity threshold" in body


def test_cli_flag_routing(tmp_path: Path, monkeypatch):
    """`w3s scrutinize <target> --skip-audit --single-model` should reach scrutinize()."""
    captured: dict = {}

    def fake_scrutinize(target, **kwargs):
        captured["target"] = target
        captured.update(kwargs)
        return tmp_path / "fake-report.md"

    monkeypatch.setattr(scrutinize, "scrutinize", fake_scrutinize)

    scrutinize.main([
        "/path/to/target.sol",
        "--skip-audit",
        "--single-model",
        "--no-audit-pocs",
        "--max-functions", "5",
        "--materialize-min-severity", "Medium",
        "--model", "sonnet",
    ])

    assert captured["target"] == "/path/to/target.sol"
    assert captured["skip_audit"] is True
    assert captured["audit_multimodel"] is False
    assert captured["audit_with_pocs"] is False
    assert captured["deep_dive_max_functions"] == 5
    assert captured["materialize_min_severity"] == "Medium"
    assert captured["model"] == "sonnet"
    # Phases not explicitly skipped should default to False
    assert captured["skip_deep_dive"] is False
    assert captured["skip_filter"] is False


def test_cli_defaults_to_full_pipeline():
    """`w3s scrutinize <target>` with no flags should enable every phase."""
    captured: dict = {}

    def fake_scrutinize(target, **kwargs):
        captured.update(kwargs)
        return Path("/tmp/x.md")

    with patch.object(scrutinize, "scrutinize", fake_scrutinize):
        scrutinize.main(["/path/to/x.sol"])

    assert captured["skip_audit"] is False
    assert captured["skip_deep_dive"] is False
    assert captured["skip_cross_fn"] is False
    assert captured["skip_materialize"] is False
    assert captured["skip_filter"] is False
    assert captured["audit_multimodel"] is True
    assert captured["audit_with_pocs"] is True
