"""Tests for harness/citations.py — validates that auditor findings cite real
corpus entries (or are flagged novel)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from harness.citations import CitationCheck, validate_findings
from harness.schema import Finding, FindingLocation


def _finding(*, title: str = "f", citations: list | None = None, novel: bool = False) -> Finding:
    return Finding(
        title=title,
        severity="High",
        location=[FindingLocation(file="x.sol", line_start=1)],
        description="d",
        impact="i",
        recommendation="r",
        citations=citations or [],
        novel=novel,
        confidence="medium",
        discovered_by="claude",
    )


def _mock_connect_with_ids(*existing_ids: str):
    """Build a context-manager that returns the given ids on SELECT."""
    rows = [{"id": eid} for eid in existing_ids]
    cm = MagicMock()
    fake_conn = MagicMock()
    fake_conn.execute.return_value.fetchall.return_value = rows
    cm.__enter__.return_value = fake_conn
    cm.__exit__.return_value = None
    return cm


def test_validate_findings_accepts_real_citations():
    f = _finding(citations=["swc-107"])
    with patch("harness.citations.corpus.connect",
               return_value=_mock_connect_with_ids("swc-107")):
        result = validate_findings([f])
    assert len(result.valid) == 1
    assert not result.rejected


def test_validate_findings_rejects_invented_citations():
    f = _finding(citations=["swc-99999-fake"])
    with patch("harness.citations.corpus.connect",
               return_value=_mock_connect_with_ids()):  # nothing exists
        result = validate_findings([f])
    assert not result.valid
    assert len(result.rejected) == 1
    _, reason = result.rejected[0]
    assert "nonexistent corpus entries" in reason
    assert "swc-99999-fake" in reason


def test_validate_findings_accepts_novel_without_citations():
    f = _finding(citations=[], novel=True)
    with patch("harness.citations.corpus.connect",
               return_value=_mock_connect_with_ids()):
        result = validate_findings([f])
    assert len(result.valid) == 1


def test_finding_schema_blocks_uncited_non_novel():
    """The Pydantic schema rejects uncited-non-novel BEFORE citations.py sees it
    — this is the load-bearing constraint of the harness, encoded at the
    schema level. Verify it stays load-bearing."""
    from pydantic import ValidationError
    with pytest.raises(ValidationError, match="non-empty OR novel"):
        Finding(
            title="bad",
            severity="High",
            location=[FindingLocation(file="x.sol", line_start=1)],
            description="d", impact="i", recommendation="r",
            citations=[], novel=False,
            confidence="medium", discovered_by="claude",
        )


def test_validate_findings_partial_invalid_citation_rejects_finding():
    """If ANY citation is bogus, the whole finding is rejected."""
    f = _finding(citations=["swc-107", "swc-fake"])
    with patch("harness.citations.corpus.connect",
               return_value=_mock_connect_with_ids("swc-107")):
        result = validate_findings([f])
    assert not result.valid
    _, reason = result.rejected[0]
    assert "swc-fake" in reason
    assert "swc-107" not in reason  # only the bogus one is named


def test_validate_findings_batches_db_lookup():
    """Even with N findings citing M total IDs, only one DB query happens."""
    findings = [
        _finding(title="a", citations=["id-1", "id-2"]),
        _finding(title="b", citations=["id-2", "id-3"]),
    ]
    fake_conn = MagicMock()
    fake_conn.execute.return_value.fetchall.return_value = [
        {"id": "id-1"}, {"id": "id-2"}, {"id": "id-3"},
    ]
    cm = MagicMock()
    cm.__enter__.return_value = fake_conn
    cm.__exit__.return_value = None
    with patch("harness.citations.corpus.connect", return_value=cm):
        result = validate_findings(findings)
    assert len(result.valid) == 2
    # The SELECT query was called exactly once
    fake_conn.execute.assert_called_once()
