"""Unit tests for the eval scorer (no LLM calls, pure logic)."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from eval.schema import ExpectedFinding
from eval.scoring import score_entry
from harness.schema import Finding, FindingLocation


def _exp(**overrides) -> ExpectedFinding:
    base = dict(
        id="test-entry",
        title="t",
        expected_severity="High",
        required_keywords=["reentrancy", "withdraw"],
        memorization_signals=[],
        exclude_corpus_ids=[],
    )
    base.update(overrides)
    return ExpectedFinding.model_validate(base)


def _finding(**overrides) -> Finding:
    base = dict(
        title="Reentrancy in withdraw()",
        severity="High",
        location=[FindingLocation(file="Foo.sol", line_start=10)],
        description="The withdraw() function has reentrancy.",
        impact="Drain.",
        recommendation="Use CEI.",
        citations=["swc-107"],
        novel=False,
        confidence="high",
        discovered_by="claude",
    )
    base.update(overrides)
    return Finding.model_validate(base)


def test_pass_on_matching_finding():
    expected = _exp()
    findings = [_finding()]
    result = score_entry(expected, findings, Path("/tmp"), "abc")
    assert result.passed
    assert len(result.matched_findings) == 1
    assert "PASS" in result.reasoning


def test_fail_when_keyword_missing():
    expected = _exp()  # requires "reentrancy" + "withdraw"
    # Override title too — keyword check scans title + description + impact + recommendation.
    f = _finding(
        title="Generic vulnerability",
        description="The function has a vulnerability.",
        impact="bad",
        recommendation="fix it",
    )
    result = score_entry(expected, [f], Path("/tmp"), "abc")
    assert not result.passed
    assert "reentrancy" in result.reasoning


def test_fail_when_severity_too_low():
    expected = _exp()
    f = _finding(severity="Low")
    result = score_entry(expected, [f], Path("/tmp"), "abc")
    assert not result.passed


def test_pass_when_severity_exceeds_minimum():
    expected = _exp()  # min High
    f = _finding(severity="Critical")
    result = score_entry(expected, [f], Path("/tmp"), "abc")
    assert result.passed


def test_memorization_signals_are_warning_not_failure():
    expected = _exp(memorization_signals=["nomad", "$190"])
    f = _finding(description="Reentrancy in withdraw(); reminiscent of the Nomad $190M hack.")
    result = score_entry(expected, [f], Path("/tmp"), "abc")
    assert result.passed
    assert set(result.memorization_signals_hit) == {"nomad", "$190"}
    assert "memorization warning" in result.reasoning


def test_keyword_match_uses_description_and_impact():
    expected = _exp(required_keywords=["specific-keyword"])
    f = _finding(description="...", impact="This contains specific-keyword in impact.")
    result = score_entry(expected, [f], Path("/tmp"), "abc")
    assert result.passed


def test_location_hint_filters_by_function_name():
    expected = _exp(expected_locations=[{"file": "Foo.sol", "function": "withdraw"}])
    matching = _finding()  # description mentions withdraw()
    non_matching = _finding(
        title="Other bug",
        description="There's a bug in the deposit() function with reentrancy.",
        location=[FindingLocation(file="Bar.sol", line_start=1)],
    )
    result = score_entry(expected, [non_matching, matching], Path("/tmp"), "abc")
    # matching is in scope (file=Foo.sol, mentions withdraw), non_matching is not.
    assert result.passed
    assert len(result.matched_findings) == 1
