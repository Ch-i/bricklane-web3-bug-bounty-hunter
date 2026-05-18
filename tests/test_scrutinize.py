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


def test_state_save_and_load_roundtrip(tmp_path: Path):
    """State writes are incremental — calling _save_state twice should merge keys."""
    scrutinize._save_state(tmp_path, {"audit_run_dir": "/tmp/audit-x"})
    scrutinize._save_state(tmp_path, {"deep_dive_run_dir": "/tmp/dd-y"})
    state = scrutinize._load_state(tmp_path)
    assert state["audit_run_dir"] == "/tmp/audit-x"
    assert state["deep_dive_run_dir"] == "/tmp/dd-y"
    assert "last_updated" in state


def test_state_load_missing_file_returns_empty(tmp_path: Path):
    assert scrutinize._load_state(tmp_path) == {}


def test_state_load_corrupt_file_returns_empty(tmp_path: Path):
    (tmp_path / "state.json").write_text("not valid json {{{")
    assert scrutinize._load_state(tmp_path) == {}


def test_resume_skips_completed_audit_phase(tmp_path: Path, monkeypatch):
    """If state.json points at an existing audit run dir with findings.json,
    Orchestrator should NOT be invoked again."""
    # Build a fake prior-completed scrutinize dir
    scrutinize_dir = tmp_path / "scrutinize-Foo-20260518"
    scrutinize_dir.mkdir()
    audit_dir = tmp_path / "audit-prior"
    audit_dir.mkdir()
    (audit_dir / "findings.json").write_text("[]")
    (audit_dir / "report.md").write_text("# old report")
    scrutinize._save_state(scrutinize_dir, {"audit_run_dir": str(audit_dir)})

    target = tmp_path / "Foo.sol"
    target.write_text("contract F { function f() external {} }")

    orch_calls = []
    monkeypatch.setattr(
        scrutinize, "Orchestrator",
        lambda *a, **kw: (orch_calls.append(1), (_ for _ in ()).throw(AssertionError("audit re-ran")))[0],
    )
    # Also patch the other phases so we don't spend
    monkeypatch.setattr(
        scrutinize.deep_dive, "run_deep_dive",
        lambda *a, **kw: tmp_path / "fake-dd-report.md",
    )
    monkeypatch.setattr(
        scrutinize.deep_dive_poc, "materialize_for_run",
        lambda *a, **kw: tmp_path / "fake-mat.json",
    )
    # Pre-create the fake deep-dive output so its run_dir resolves
    fake_dd_dir = tmp_path / "deep-dive"
    fake_dd_dir.mkdir()
    (fake_dd_dir / "deep-dive-report.md").write_text("# dd report")
    (fake_dd_dir / "per-function.jsonl").write_text("")
    monkeypatch.setattr(
        scrutinize.deep_dive, "run_deep_dive",
        lambda *a, **kw: fake_dd_dir / "deep-dive-report.md",
    )
    (tmp_path / "fake-mat.json").write_text("[]")
    monkeypatch.setattr(scrutinize, "filter_findings",
                        lambda *a, **kw: [], raising=False)

    # Stub out filter_agent.filter_findings on the real module to avoid LLM
    from harness import filter_agent as _fa
    monkeypatch.setattr(_fa, "filter_findings", lambda *a, **kw: [])

    scrutinize.scrutinize(str(target), out_dir=scrutinize_dir)

    # The audit phase should never have invoked Orchestrator
    assert orch_calls == []
    # Master report should still be generated
    assert (scrutinize_dir / "scrutinize-report.md").exists()


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


def test_estimate_plan_scales_with_function_count(tmp_path: Path):
    """The estimator should report function/pair counts and a total message budget."""
    # Build a small Solidity project so decompose() finds N functions
    src = '''
contract Vault {
    uint256 public x;
    function deposit() external payable { x += msg.value; }
    function withdraw(uint a) external { x -= a; payable(msg.sender).transfer(a); }
    function emergencyShutdown() external {}
    modifier onlyOwner() { require(msg.sender == address(0)); _; }
}
'''
    target = tmp_path / "src" / "Vault.sol"
    target.parent.mkdir()
    target.write_text(src)
    # decompose() needs a project root - point at tmp_path
    plan = scrutinize.estimate_plan(
        tmp_path, scope=None,
        skip_audit=False, skip_deep_dive=False, skip_cross_fn=False,
        skip_materialize=False, skip_filter=False,
        audit_multimodel=True, audit_with_pocs=True,
        deep_dive_max_functions=None,
    )
    assert plan["function_count"] == 4  # deposit, withdraw, emergencyShutdown, onlyOwner
    assert plan["messages"]["deep_dive_per_fn"] == 4
    assert plan["messages"]["audit"] >= 3  # multimodel + pocs
    assert plan["messages"]["total"] > plan["messages"]["audit"]  # other phases contribute
    assert plan["wall_time_estimate_s"][0] < plan["wall_time_estimate_s"][1]


def test_estimate_plan_respects_skips(tmp_path: Path):
    """Skipping audit + deep-dive should produce a near-zero budget."""
    target = tmp_path / "Vault.sol"
    target.write_text("contract V { function f() external {} }")
    plan = scrutinize.estimate_plan(
        tmp_path, scope=None,
        skip_audit=True, skip_deep_dive=True, skip_cross_fn=True,
        skip_materialize=True, skip_filter=True,
        audit_multimodel=True, audit_with_pocs=True,
        deep_dive_max_functions=None,
    )
    assert plan["messages"]["total"] == 0
    assert plan["messages"]["audit"] == 0
    assert plan["messages"]["deep_dive_per_fn"] == 0


def test_estimate_plan_caps_at_max_functions(tmp_path: Path):
    """deep_dive_max_functions should cap the per-fn budget."""
    parts = ["contract C {"]
    for i in range(20):
        parts.append(f"    function f{i}() external {{}}")
    parts.append("}")
    (tmp_path / "C.sol").write_text("\n".join(parts))
    plan = scrutinize.estimate_plan(
        tmp_path, scope=None,
        skip_audit=True, skip_deep_dive=False, skip_cross_fn=True,
        skip_materialize=True, skip_filter=True,
        audit_multimodel=False, audit_with_pocs=False,
        deep_dive_max_functions=5,
    )
    assert plan["function_count"] == 5
    assert plan["messages"]["deep_dive_per_fn"] == 5


def test_dry_run_returns_none_and_doesnt_create_dir(tmp_path: Path, monkeypatch):
    target = tmp_path / "Foo.sol"
    target.write_text("contract F { function f() external {} }")
    # Patch the orchestrator + deep_dive so a non-dry-run would fail loudly if hit
    called = {"hit": False}
    monkeypatch.setattr(scrutinize, "Orchestrator", lambda *a, **kw: (_ for _ in ()).throw(AssertionError("dry-run hit Orchestrator")))
    monkeypatch.setattr(scrutinize.deep_dive, "run_deep_dive", lambda *a, **kw: (_ for _ in ()).throw(AssertionError("dry-run hit run_deep_dive")))

    result = scrutinize.scrutinize(str(tmp_path), dry_run=True)
    assert result is None
    # Should not have created an audits/ dir
    audits = (scrutinize.REPO_ROOT / "audits")
    new_dirs = [d for d in audits.iterdir() if d.is_dir() and "scrutinize-" in d.name and target.parent.name in d.name]
    # The dry-run path shouldn't create a run dir at all
    assert called["hit"] is False


def test_scrutinize_filter_merges_deep_dive_high_sev_candidates(tmp_path: Path, monkeypatch):
    """Filter phase should ingest High/Critical candidate_vulnerabilities from
    per-function.jsonl, not just audit findings + materialized."""
    scrutinize_dir = tmp_path / "scrut-x"
    scrutinize_dir.mkdir()

    audit_dir = tmp_path / "audit-pre"
    audit_dir.mkdir()
    (audit_dir / "findings.json").write_text(json.dumps([
        {"title": "Audit-side Critical", "severity": "Critical"},
    ]))
    (audit_dir / "report.md").write_text("# r")

    dd_dir = tmp_path / "dd-pre"
    dd_dir.mkdir()
    (dd_dir / "deep-dive-report.md").write_text("# dd")
    (dd_dir / "per-function.jsonl").write_text("\n".join([
        json.dumps({"function_id": "X.sol::X::a",
                    "candidate_vulnerabilities": [
                        {"title": "DD High bug", "severity": "High",
                         "description": "d", "impact": "i", "confidence": "high"},
                        {"title": "DD Low bug",  "severity": "Low"},  # should be dropped
                    ]}),
    ]))

    scrutinize._save_state(scrutinize_dir, {
        "audit_run_dir": str(audit_dir),
        "deep_dive_run_dir": str(dd_dir),
    })

    target = tmp_path / "T.sol"
    target.write_text("//")

    captured = {"findings_seen": None}

    def fake_filter_findings(findings, target_root, model="opus"):
        captured["findings_seen"] = findings
        for f in findings:
            f.setdefault("filter", {"verdict": "ACCEPT", "rationale": "ok"})
        return [(f, type("V", (), {"finding_title": f["title"], "verdict": "ACCEPT",
                                    "rationale": "ok", "raw_response": ""})())
                for f in findings]

    # Stub filter_agent.filter_findings on the real module to avoid LLM
    from harness import filter_agent as _fa
    monkeypatch.setattr(_fa, "filter_findings", fake_filter_findings)

    # Stub orchestrator + deep_dive so we don't spend LLM
    monkeypatch.setattr(
        scrutinize, "Orchestrator",
        lambda *a, **kw: (_ for _ in ()).throw(AssertionError("audit re-ran")),
    )
    monkeypatch.setattr(
        scrutinize.deep_dive, "run_deep_dive",
        lambda *a, **kw: dd_dir / "deep-dive-report.md",
    )
    monkeypatch.setattr(
        scrutinize.deep_dive_poc, "materialize_for_run",
        lambda *a, **kw: tmp_path / "mat.json",
    )
    (tmp_path / "mat.json").write_text(json.dumps([]))

    scrutinize.scrutinize(str(target), out_dir=scrutinize_dir)

    titles = {f["title"] for f in captured["findings_seen"]}
    assert "Audit-side Critical" in titles
    assert "DD High bug" in titles
    # Low-severity DD findings should be filtered out at the High threshold
    assert "DD Low bug" not in titles


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
