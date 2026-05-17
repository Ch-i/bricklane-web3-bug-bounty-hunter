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
