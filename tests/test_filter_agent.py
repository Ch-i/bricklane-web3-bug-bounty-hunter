"""Unit tests for harness.filter_agent — output parsing + source resolution."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from harness.filter_agent import FilterVerdict, _read_source_around, judge_finding


def _fake_proc(text: str, rc: int = 0):
    proc = MagicMock()
    proc.returncode = rc
    proc.stdout = json.dumps({"result": text})
    proc.stderr = ""
    return proc


def test_judge_finding_parses_accept(tmp_path):
    src = tmp_path / "Foo.sol"
    src.write_text("\n".join([f"line {i}" for i in range(50)]))
    finding = {
        "title": "test bug",
        "severity": "High",
        "description": "d",
        "impact": "i",
        "recommendation": "r",
        "citations": ["swc-107"],
        "location": [{"file": "Foo.sol", "line_start": 10, "line_end": 12}],
    }
    with patch(
        "harness.filter_agent.subprocess.run",
        return_value=_fake_proc("VERDICT: ACCEPT :: Critical, exploitable, no upstream guard"),
    ):
        v = judge_finding(finding, tmp_path)
    assert v.verdict == "ACCEPT"
    assert "Critical" in v.rationale


def test_judge_finding_parses_downgrade(tmp_path):
    src = tmp_path / "Foo.sol"
    src.write_text("contract Foo {}")
    finding = {"title": "minor", "location": [{"file": "Foo.sol", "line_start": 1}]}
    with patch(
        "harness.filter_agent.subprocess.run",
        return_value=_fake_proc("VERDICT: downgrade :: anti-pattern only"),
    ):
        v = judge_finding(finding, tmp_path)
    assert v.verdict == "DOWNGRADE"


def test_judge_finding_handles_unparseable(tmp_path):
    src = tmp_path / "Foo.sol"
    src.write_text("contract Foo {}")
    finding = {"title": "x", "location": [{"file": "Foo.sol", "line_start": 1}]}
    with patch("harness.filter_agent.subprocess.run", return_value=_fake_proc("I don't know")):
        v = judge_finding(finding, tmp_path)
    assert v.verdict == "ERROR"
    assert "unparseable" in v.rationale


def test_read_source_around_extracts_context(tmp_path):
    src = tmp_path / "Foo.sol"
    src.write_text("\n".join([f"line {i}" for i in range(100)]))
    finding = {"location": [{"file": "Foo.sol", "line_start": 50, "line_end": 52}]}
    snippet = _read_source_around(finding, tmp_path, context_lines=5)
    assert "line 49" in snippet  # within context_lines before line_start (1-indexed)
    assert "line 55" in snippet  # within context_lines after line_end
    assert "Foo.sol:50-52" in snippet


def test_read_source_around_missing_file(tmp_path):
    finding = {"location": [{"file": "MissingFoo.sol", "line_start": 1}]}
    snippet = _read_source_around(finding, tmp_path)
    assert "not found" in snippet


def test_read_source_around_empty_location(tmp_path):
    """No location entries → returns helpful placeholder."""
    snippet = _read_source_around({"location": []}, tmp_path)
    assert "no location" in snippet


def test_judge_finding_parses_reject_verdict(tmp_path):
    src = tmp_path / "Foo.sol"
    src.write_text("contract Foo {}")
    finding = {"title": "x", "location": [{"file": "Foo.sol", "line_start": 1}]}
    with patch("harness.filter_agent.subprocess.run",
               return_value=_fake_proc("VERDICT: REJECT :: internal function, no user reach")):
        v = judge_finding(finding, tmp_path)
    assert v.verdict == "REJECT"
    assert "internal function" in v.rationale


def test_judge_finding_returns_error_when_claude_missing(tmp_path):
    finding = {"title": "x", "location": []}
    with patch("harness.filter_agent._claude_bin", return_value=None):
        v = judge_finding(finding, tmp_path)
    assert v.verdict == "ERROR"
    assert "claude" in v.rationale.lower()


def test_judge_finding_returns_error_on_timeout(tmp_path):
    import subprocess as _sub
    finding = {"title": "x", "location": []}
    with patch("harness.filter_agent.subprocess.run",
               side_effect=_sub.TimeoutExpired("claude", 180)):
        v = judge_finding(finding, tmp_path)
    assert v.verdict == "ERROR"
    assert "timeout" in v.rationale


def test_filter_findings_annotates_in_place(tmp_path):
    """filter_findings should populate finding['filter'] so downstream consumers
    (submissions, master report) can read it without re-running the judge."""
    from harness.filter_agent import filter_findings

    findings = [
        {"title": "A", "location": []},
        {"title": "B", "location": []},
    ]
    with patch("harness.filter_agent.subprocess.run",
               return_value=_fake_proc("VERDICT: ACCEPT :: looks legit")):
        results = filter_findings(findings, tmp_path)
    assert len(results) == 2
    for f in findings:
        assert "filter" in f
        assert f["filter"]["verdict"] == "ACCEPT"
        assert "looks legit" in f["filter"]["rationale"]
