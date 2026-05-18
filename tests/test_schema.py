"""Tests for harness/schema.py — Pydantic validators on the wire-format types."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from harness.schema import (
    CorpusEntryFrontmatter,
    Finding,
    FindingLocation,
    FoundryPoc,
    ModelDisagreement,
)


def test_corpus_frontmatter_basic_valid():
    fm = CorpusEntryFrontmatter(
        id="swc-107",
        source="swc",
        title="Reentrancy",
        ingested_at="2026-05-18T00:00:00Z",
        vuln_class=["reentrancy"],
    )
    assert fm.id == "swc-107"
    assert fm.source == "swc"


def test_corpus_frontmatter_id_pattern_rejects_caps():
    """IDs must start with lowercase letter."""
    with pytest.raises(ValidationError):
        CorpusEntryFrontmatter(
            id="Swc-107", source="swc", title="x",
            ingested_at="2026-05-18T00:00:00Z",
        )


def test_corpus_frontmatter_id_pattern_requires_hyphen_separator():
    """IDs must contain '<prefix>-<rest>'."""
    with pytest.raises(ValidationError):
        CorpusEntryFrontmatter(
            id="swc107", source="swc", title="x",  # no hyphen
            ingested_at="2026-05-18T00:00:00Z",
        )


def test_corpus_frontmatter_normalizes_string_vuln_class_to_list():
    """A bare string for vuln_class should become a one-item list."""
    fm = CorpusEntryFrontmatter(
        id="swc-107", source="swc", title="x",
        ingested_at="2026-05-18T00:00:00Z",
        vuln_class="reentrancy",  # not a list — should be coerced
    )
    assert fm.vuln_class == ["reentrancy"]


def test_corpus_frontmatter_normalizes_none_vuln_class_to_empty_list():
    fm = CorpusEntryFrontmatter(
        id="swc-107", source="swc", title="x",
        ingested_at="2026-05-18T00:00:00Z",
        vuln_class=None,
    )
    assert fm.vuln_class == []


def test_corpus_frontmatter_allows_extra_fields():
    """extra='allow' should let unknown fields survive (for forward-compat)."""
    fm = CorpusEntryFrontmatter(
        id="swc-107", source="swc", title="x",
        ingested_at="2026-05-18T00:00:00Z",
        my_custom_field="hello",  # not in the schema
    )
    # The custom field is stored as model_extra
    assert fm.model_extra is not None
    assert fm.model_extra.get("my_custom_field") == "hello"


def test_finding_location_minimal():
    loc = FindingLocation(file="x.sol", line_start=42)
    assert loc.line_end is None


def test_finding_location_with_range():
    loc = FindingLocation(file="x.sol", line_start=42, line_end=58)
    assert loc.line_end == 58


def test_foundry_poc_requires_all_fields():
    """FoundryPoc requires test_name, setup, exploit, assertion."""
    with pytest.raises(ValidationError):
        FoundryPoc(test_name="test_x")  # missing setup/exploit/assertion


def test_foundry_poc_full():
    poc = FoundryPoc(
        test_name="test_drainViaReentrancy",
        setup="Vault v = new Vault();",
        exploit="Attacker(v).attack();",
        assertion="assertEq(address(v).balance, 0);",
    )
    assert poc.test_name.startswith("test_")


def test_finding_with_citations_validates():
    f = Finding(
        title="bug",
        severity="High",
        location=[FindingLocation(file="x.sol", line_start=1)],
        description="d", impact="i", recommendation="r",
        citations=["swc-107"],
        novel=False,
        confidence="high",
        discovered_by="claude",
    )
    assert f.title == "bug"


def test_finding_with_novel_no_citations_validates():
    f = Finding(
        title="bug",
        severity="High",
        location=[FindingLocation(file="x.sol", line_start=1)],
        description="d", impact="i", recommendation="r",
        citations=[],
        novel=True,
        confidence="medium",
        discovered_by="claude",
    )
    assert f.novel is True


def test_finding_without_citations_or_novel_rejected():
    with pytest.raises(ValidationError, match="non-empty OR novel"):
        Finding(
            title="bug",
            severity="High",
            location=[FindingLocation(file="x.sol", line_start=1)],
            description="d", impact="i", recommendation="r",
            citations=[],
            novel=False,
            confidence="medium",
            discovered_by="claude",
        )


def test_finding_poc_status_default():
    f = Finding(
        title="bug", severity="High",
        location=[FindingLocation(file="x.sol", line_start=1)],
        description="d", impact="i", recommendation="r",
        citations=["swc-107"], novel=False,
        confidence="high", discovered_by="claude",
    )
    assert f.poc_status == "not-attempted"


def test_finding_poc_status_constrained():
    """Only the enumerated statuses should be accepted."""
    with pytest.raises(ValidationError):
        Finding(
            title="bug", severity="High",
            location=[FindingLocation(file="x.sol", line_start=1)],
            description="d", impact="i", recommendation="r",
            citations=["swc-107"], novel=False,
            confidence="high", discovered_by="claude",
            poc_status="invalid-status",
        )


def test_model_disagreement_shape():
    d = ModelDisagreement(
        topic="reentrancy in withdraw",
        claude_position="bug exists, severity High",
        codex_position="upstream guard makes it unreachable",
    )
    assert d.topic == "reentrancy in withdraw"
    assert d.reconciler_resolution is None  # optional


def test_model_disagreement_with_resolution():
    d = ModelDisagreement(
        topic="x",
        claude_position="found bug",
        codex_position="no bug",
        reconciler_resolution="claude correct; upstream guard does not cover this path",
    )
    assert d.reconciler_resolution.startswith("claude correct")
