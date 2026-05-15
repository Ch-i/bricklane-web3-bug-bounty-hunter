"""Pydantic models for corpus entries (frontmatter) and audit findings.

Two distinct schemas live here:

* ``CorpusEntryFrontmatter`` — the YAML at the top of every ``corpus/*.md`` file.
  Mirrored row-by-row into ``corpus_entries`` (+ side tables for list fields).

* ``Finding`` / ``AuditReport`` — the structured output every audit subagent
  must emit. Citation enforcement happens by validating this model.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

Severity = Literal["Critical", "High", "Medium", "Low", "Informational", "Gas"]
SourceKind = Literal[
    "swc",
    "solodit",
    "arxiv",
    "audit-report",
    "rekt",
    "dasp",
    "synthesis",
]
DiscoveredBy = Literal["claude", "codex", "reconciler", "human"]
Confidence = Literal["high", "medium", "low"]


class CorpusEntryFrontmatter(BaseModel):
    """YAML frontmatter contract for a single corpus markdown file."""

    model_config = ConfigDict(extra="allow")

    id: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9-]*-[A-Za-z0-9._-]+$",
        description="Stable id, e.g. 'swc-107', 'solodit-12345', 'arxiv-2401.12345'.",
    )
    source: SourceKind
    source_url: str | None = None
    title: str
    ingested_at: datetime
    published_at: datetime | None = None

    vuln_class: list[str] = Field(default_factory=list)
    severity: Severity | None = None
    protocol_category: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    related_swc: list[str] = Field(default_factory=list)
    derives_from: list[str] = Field(default_factory=list)

    cve: str | None = None
    # Each item: {"address": "0x...", "chain": "mainnet" | "arbitrum" | ...}
    affected_contracts: list[dict[str, str]] = Field(default_factory=list)

    @field_validator("vuln_class", "tags", "protocol_category", mode="before")
    @classmethod
    def _normalize_str_list(cls, v):
        if v is None:
            return []
        if isinstance(v, str):
            return [v]
        return list(v)


class FindingLocation(BaseModel):
    file: str
    line_start: int
    line_end: int | None = None


class FoundryPoc(BaseModel):
    """Structured-enough proof-of-concept that we can generate a runnable
    Foundry test file from it. The auditor fills the four bodies with
    Solidity-like code (or pseudocode that closely resembles Solidity);
    the PoC scaffolder wraps them with `forge-std/Test.sol` boilerplate.

    The point: turn `proof_of_concept` prose into AFL-crash-file-style
    reproducible artifacts that anyone can run with `forge test`. A
    failing test on the buggy code is the demonstration that the bug
    exists.
    """

    test_name: str = Field(
        ...,
        description="Function name for the test, e.g. 'test_drainViaReentrancy'. "
        "Must start with 'test_' to be picked up by forge.",
    )
    setup: str = Field(
        ...,
        description="Solidity / pseudocode body for the test's setUp() function "
        "— initial state, deployments, deals, approvals.",
    )
    exploit: str = Field(
        ...,
        description="Solidity / pseudocode body for the test function — the "
        "actual attack sequence (calls, transfers, etc).",
    )
    assertion: str = Field(
        ...,
        description="Solidity body asserting the bug manifested — e.g. "
        "'assertGt(attacker.balance, 100 ether)' or 'vm.expectRevert(); ...'. "
        "A passing assertion = bug confirmed.",
    )
    imports: list[str] = Field(
        default_factory=list,
        description="Extra imports needed, e.g. ['../src/Foo.sol', "
        "'@openzeppelin/contracts/token/ERC20/IERC20.sol'].",
    )
    notes: str | None = Field(
        default=None,
        description="Caveats: 'requires fork at block N', 'assumes attacker funded', etc.",
    )


class Finding(BaseModel):
    """One vulnerability surfaced by an audit pass.

    Citation rule: ``citations`` must be non-empty OR ``novel`` must be True.
    Enforced by ``model_validator`` below; the reconciler also re-checks at
    report-write time so the rule cannot be silently bypassed.
    """

    title: str
    severity: Severity
    location: list[FindingLocation] = Field(default_factory=list)
    description: str
    impact: str
    recommendation: str
    proof_of_concept: str | None = Field(
        default=None,
        description="Free-form prose PoC (legacy, also accepted by the schema).",
    )
    foundry_poc: FoundryPoc | None = Field(
        default=None,
        description="Structured PoC suitable for auto-generating a runnable Foundry test.",
    )
    citations: list[str] = Field(
        default_factory=list,
        description="Corpus entry IDs that informed this finding.",
    )
    novel: bool = Field(
        default=False,
        description="True if the finding cannot be grounded in any corpus entry.",
    )
    confidence: Confidence = "medium"
    discovered_by: DiscoveredBy = "claude"
    # Populated post-finalize by the PoC executor; lets the report render a
    # "reproducible / unconfirmed / not-applicable" badge per finding.
    poc_status: Literal["not-attempted", "reproduced", "unconfirmed", "compile-error", "not-applicable"] = "not-attempted"
    poc_artifacts: dict[str, str] = Field(
        default_factory=dict,
        description="Paths to runnable artifacts: {test_path, stdout_log, stderr_log, ...}",
    )

    @model_validator(mode="after")
    def _require_citation_or_novel(self) -> Finding:
        if not self.citations and not self.novel:
            raise ValueError(
                f"Finding '{self.title}': citations must be non-empty OR novel=true. "
                "This is the load-bearing constraint of the harness — every claim "
                "must either ground in prior art or explicitly flag itself as a "
                "pattern we haven't seen before."
            )
        return self


class StaticToolFindings(BaseModel):
    """Raw output blob from a single static analyzer."""

    tool: Literal["slither", "aderyn", "foundry", "halmos", "mythril"]
    version: str | None = None
    succeeded: bool
    output: dict | list | str
    error: str | None = None


class ModelDisagreement(BaseModel):
    """A point where Claude and Codex came to different conclusions."""

    topic: str
    claude_position: str
    codex_position: str
    reconciler_resolution: str | None = None


class AuditReport(BaseModel):
    """Final artifact written to ``audits/<target>-<ts>/report.md``."""

    target: str
    target_kind: Literal["foundry-project", "single-file", "directory", "deployed-address"]
    target_metadata: dict = Field(default_factory=dict)
    timestamp: datetime
    corpus_snapshot: str = Field(
        ...,
        description="Git SHA of corpus directory at audit time (for reproducibility).",
    )
    model_versions: dict[str, str] = Field(default_factory=dict)
    static_tools: list[StaticToolFindings] = Field(default_factory=list)
    findings: list[Finding] = Field(default_factory=list)
    model_disagreements: list[ModelDisagreement] = Field(default_factory=list)
