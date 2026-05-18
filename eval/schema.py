"""Schema for an eval entry's ``expected-finding.md`` frontmatter.

The body of the file is human-readable prose describing the canonical bug;
the frontmatter is what the scorer reads.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from harness.schema import Severity


class ExpectedFinding(BaseModel):
    """One historical exploit, described in terms the scorer can match against."""

    model_config = ConfigDict(extra="allow")

    id: str = Field(..., description="Stable eval id, e.g. 'euler-donate-2023'.")
    title: str
    post_mortem_url: str | None = None
    incident_date: str | None = None
    funds_at_risk_usd: int | None = None
    target_protocol: str | None = None

    expected_vuln_class: list[str] = Field(default_factory=list)
    expected_severity: Severity = "High"
    expected_locations: list[dict] = Field(
        default_factory=list,
        description="Hints for the scorer: [{file, function, line_hint}]. "
        "Optional; scoring is primarily semantic.",
    )

    required_keywords: list[str] = Field(
        default_factory=list,
        description="Substrings (case-insensitive) that must appear in the "
        "auditor's finding for a positive match. Pick keywords that are "
        "specific enough to indicate understanding, but generic enough that "
        "an auditor would actually use them when reasoning from source alone.",
    )

    memorization_signals: list[str] = Field(
        default_factory=list,
        description="Strings whose appearance suggests the auditor pulled "
        "from training data rather than (or in addition to) reading the "
        "source — protocol names, specific dollar amounts, attack dates. "
        "Logged as a warning on the result; does NOT auto-fail. The eval "
        "grades on whether the bug was found, not on attribution style.",
    )

    exclude_corpus_ids: list[str] = Field(
        default_factory=list,
        description="Corpus entries to filter out at audit time so the "
        "auditor cannot trivially solve this case by reading the post-mortem.",
    )

    grading_mode: Literal["keyword", "llm-judge", "hybrid"] = "keyword"


class EvalResult(BaseModel):
    """One row of ``eval/scores.jsonl`` — append-only."""

    entry_id: str
    timestamp: str
    run_dir: str
    corpus_snapshot: str
    mode: Literal["single", "multimodel", "scrutinize"] = "single"

    matched_findings: list[dict] = Field(default_factory=list)
    """Each: {finding_title, severity, matched_keywords, location_hit}."""

    passed: bool
    reasoning: str

    # Diagnostics
    all_finding_titles: list[str] = Field(default_factory=list)
    total_findings: int = 0
    memorization_signals_hit: list[str] = Field(
        default_factory=list,
        description="Subset of expected.memorization_signals that appeared "
        "in the auditor's output. Warning only — not a fail criterion.",
    )
