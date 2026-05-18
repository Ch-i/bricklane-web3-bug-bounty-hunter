"""Tests for harness/render.py — the audit report Jinja renderer."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from harness.render import (
    _poc_badge, _poc_summary, _severity_counts,
    render_markdown, write_report,
)
from harness.schema import (
    AuditReport, Finding, FindingLocation, StaticToolFindings,
)


def _finding(title: str = "f", severity: str = "High", citations: list | None = None,
             novel: bool = False, poc_status: str = "not-attempted") -> Finding:
    cites = citations or []
    return Finding(
        title=title, severity=severity,
        location=[FindingLocation(file="x.sol", line_start=1)],
        description="desc", impact="impact", recommendation="rec",
        citations=cites,
        # If no citations, must flag novel — pydantic schema enforces this
        novel=novel or not cites,
        confidence="medium", discovered_by="claude",
        poc_status=poc_status,
    )


def test_severity_counts_groups_by_severity():
    findings = [
        _finding(severity="Critical"),
        _finding(severity="High"),
        _finding(severity="High"),
        _finding(severity="Low"),
    ]
    counts = _severity_counts(findings)
    assert counts == {"Critical": 1, "High": 2, "Low": 1}


def test_severity_counts_empty():
    assert _severity_counts([]) == {}


def test_poc_badge_known_status():
    assert "✅" in _poc_badge("reproduced")
    assert _poc_badge("reproduced") == "✅ reproduced"


def test_poc_badge_unknown_status_passthrough():
    """An unrecognized status is returned verbatim (no crash)."""
    assert _poc_badge("custom-status") == "custom-status"


def test_poc_summary_groups_by_status():
    findings = [
        _finding(poc_status="reproduced"),
        _finding(poc_status="reproduced"),
        _finding(poc_status="not-attempted"),
    ]
    out = _poc_summary(findings)
    assert out == {"reproduced": 2, "not-attempted": 1}


def test_render_markdown_basic_report():
    report = AuditReport(
        target="src/Vault.sol",
        target_kind="single-file",
        timestamp=datetime(2026, 5, 18, tzinfo=timezone.utc),
        corpus_snapshot="abc123",
        model_versions={"claude": "opus-4-7"},
        static_tools=[
            StaticToolFindings(tool="slither", succeeded=True, version="0.10.1", output={}),
            StaticToolFindings(tool="aderyn", succeeded=False, error="not installed", output={}),
        ],
        findings=[
            _finding(title="Reentrancy in withdraw", severity="High",
                     citations=["swc-107"], poc_status="reproduced"),
            _finding(title="Novel storage pattern", severity="Low",
                     novel=True),
        ],
    )
    md = render_markdown(report)
    # Header
    assert "Audit Report — src/Vault.sol" in md
    # Severity table
    assert "| Severity | Count |" in md
    assert "| High | 1 |" in md
    assert "| Low | 1 |" in md
    # PoC table
    assert "✅ reproduced" in md
    # Static tools
    assert "slither" in md
    assert "OK" in md
    assert "FAILED" in md
    # Findings
    assert "Reentrancy in withdraw" in md
    assert "Novel storage pattern" in md
    assert "[novel]" in md
    # Citations
    assert "swc-107" in md


def test_render_markdown_no_findings():
    report = AuditReport(
        target="src/Foo.sol",
        target_kind="single-file",
        timestamp=datetime(2026, 5, 18, tzinfo=timezone.utc),
        corpus_snapshot="abc123",
        static_tools=[],
        findings=[],
    )
    md = render_markdown(report)
    assert "No findings." in md


def test_write_report_writes_md_and_json(tmp_path: Path):
    report = AuditReport(
        target="x.sol",
        target_kind="single-file",
        timestamp=datetime(2026, 5, 18, tzinfo=timezone.utc),
        corpus_snapshot="abc",
        static_tools=[],
        findings=[_finding()],
    )
    out_path = write_report(report, tmp_path)
    assert out_path.exists()
    assert out_path.suffix == ".md"
    # Should also write findings.json sibling
    findings_json = tmp_path / "findings.json"
    assert findings_json.exists()
    # And rejected.md sibling for rejected findings, if any
