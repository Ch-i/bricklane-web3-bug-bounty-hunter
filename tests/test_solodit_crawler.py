"""Unit tests for crawlers.solodit.parse_report (no network / no clone)."""

from __future__ import annotations

from pathlib import Path

from crawlers.solodit import parse_report


SAMPLE_REPORT = """\
**Lead Auditors**

[Alice](https://twitter.com/alice)

# Findings

## Critical Risk
### Total funds drainable via reentrancy
**Description:** The withdraw function ...

(more body content that is definitely longer than the forty-character stub filter)

**Recommendation:** Use ReentrancyGuard.

### Another critical issue
**Description:** Some other unrelated issue with enough length to pass the
forty-character body filter that we apply to skip stubs.

## High Risk
### A high finding
This is a high-risk finding body with enough characters to pass the threshold.

## Vulnerability Details
this section should be skipped because the header is on the non-finding list

## Informational
### tiny stub
short

### Real info finding
This is a proper informational finding with a substantive body that should be ingested.

## Gas Optimization
### Save gas on storage read
Body content for the gas finding, with enough text to clear the stub filter.
"""


def test_parser_splits_findings_by_section(tmp_path):
    md = tmp_path / "report.md"
    md.write_text(SAMPLE_REPORT)
    findings = list(parse_report(md))

    titles_by_severity = {}
    for f in findings:
        titles_by_severity.setdefault(f.severity, []).append(f.title)

    assert titles_by_severity.get("Critical") == [
        "Total funds drainable via reentrancy",
        "Another critical issue",
    ]
    assert titles_by_severity.get("High") == ["A high finding"]
    # "tiny stub" is filtered (body < 40 chars); "Real info finding" passes.
    assert titles_by_severity.get("Informational") == ["Real info finding"]
    assert titles_by_severity.get("Gas") == ["Save gas on storage read"]

    # "Vulnerability Details" is on the non-finding skip list.
    all_titles = [f.title for f in findings]
    assert not any("Vulnerability Details" in t for t in all_titles)


def test_parser_handles_section_only_report(tmp_path):
    """Some Solodit reports use ## for the finding itself, no ### inside."""
    md = tmp_path / "single.md"
    md.write_text(
        "## Reentrancy in withdraw\n"
        "There is a reentrancy bug in withdraw, here are the details, with "
        "enough body content to pass the substantive-body filter at 200 chars. "
        "The withdraw function transfers before updating state, allowing the "
        "attacker to drain the contract via a malicious receiver callback.\n"
    )
    findings = list(parse_report(md))
    # Section header is not a known severity; falls back to Medium because body > 200 chars.
    assert len(findings) == 1
    assert findings[0].severity == "Medium"
    assert findings[0].title == "Reentrancy in withdraw"


def test_parser_returns_nothing_on_empty_report(tmp_path):
    md = tmp_path / "empty.md"
    md.write_text("# Title\n\nNo sections here.\n")
    assert list(parse_report(md)) == []
