"""Tests for harness/orchestrator.py — focuses on testable data-shaping logic
(brief composition, Stage-1 suspects merge) without invoking subprocesses."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from harness.orchestrator import Orchestrator, OrchestratorOptions
from harness.candidates import Candidate


def _make_orch(target: str = "/tmp/Foo.sol", target_files=None) -> Orchestrator:
    o = Orchestrator(OrchestratorOptions(target=target))
    o.prep_meta = {
        "target": target,
        "target_kind": "single-file",
        "target_files": target_files or ["Foo.sol"],
        "run_dir": "/tmp/run-abc",
        "static_tools_path": "/tmp/run-abc/static-tools.json",
    }
    return o


def test_claude_brief_includes_target_and_files():
    o = _make_orch(target="/tmp/Foo.sol",
                   target_files=["src/Vault.sol", "src/Library.sol"])
    with patch("harness.candidates.find_by_local_path", return_value=None):
        brief = o._claude_brief()
    assert "TARGET: /tmp/Foo.sol" in brief
    assert "src/Vault.sol" in brief
    assert "src/Library.sol" in brief
    assert "auditor-output.json" in brief
    assert "discovered_by" in brief


def test_claude_brief_includes_stage1_block_when_candidate_match():
    """If find_by_local_path returns a candidate with triage_top_suspects,
    the brief should include the STAGE-1 PRIOR ANALYSIS section."""
    cand = Candidate(
        id="c4-test",
        platform="code4rena",
        kind="source",
        title="Test",
        sourced_at="2026-05-15T00:00:00+00:00",
        local_path="/tmp/Foo.sol",
        triage_score=8.5,
        triage_rationale="High-payout AMM with complex math",
        triage_top_suspects=[
            {"file": "src/Vault.sol", "function": "swap",
             "why": "non-standard slippage check"},
            {"file": "src/Router.sol", "function": "addLiquidity",
             "why": "share inflation pattern"},
        ],
    )
    o = _make_orch()
    with patch("harness.candidates.find_by_local_path", return_value=cand):
        brief = o._claude_brief()
    assert "STAGE-1 PRIOR ANALYSIS" in brief
    assert "score=8.5" in brief
    assert "High-payout AMM" in brief
    assert "src/Vault.sol::swap" in brief
    assert "non-standard slippage check" in brief
    assert "DO NOT be limited" in brief  # the "don't anchor too hard" instruction


def test_claude_brief_omits_stage1_block_when_no_candidate():
    o = _make_orch()
    with patch("harness.candidates.find_by_local_path", return_value=None):
        brief = o._claude_brief()
    assert "STAGE-1 PRIOR ANALYSIS" not in brief


def test_claude_brief_omits_stage1_block_when_no_suspects():
    """A candidate match without top_suspects shouldn't insert an empty block."""
    cand = Candidate(
        id="c4-noscore",
        platform="code4rena",
        kind="source",
        title="Test",
        sourced_at="2026-05-15T00:00:00+00:00",
        local_path="/tmp/Foo.sol",
        triage_top_suspects=[],  # empty
    )
    o = _make_orch()
    with patch("harness.candidates.find_by_local_path", return_value=cand):
        brief = o._claude_brief()
    assert "STAGE-1 PRIOR ANALYSIS" not in brief


def test_stage1_suspects_block_handles_missing_optional_fields():
    """If triage_top_suspects has dicts missing 'why' or 'file', still render."""
    cand = Candidate(
        id="c4-partial",
        platform="code4rena",
        kind="source",
        title="Test",
        sourced_at="2026-05-15T00:00:00+00:00",
        local_path="/tmp/Foo.sol",
        triage_score=7.0,
        triage_top_suspects=[
            {"function": "withdraw"},  # missing file + why
            {"file": "x.sol"},          # missing function + why
        ],
    )
    o = _make_orch()
    with patch("harness.candidates.find_by_local_path", return_value=cand):
        block = o._stage1_suspects_block()
    # Doesn't crash
    assert "STAGE-1 PRIOR ANALYSIS" in block
    assert "withdraw" in block
    assert "x.sol" in block


def test_stage1_suspects_block_swallows_candidate_lookup_errors():
    """If candidates.find_by_local_path raises, return empty string (graceful)."""
    o = _make_orch()
    with patch("harness.candidates.find_by_local_path",
               side_effect=RuntimeError("db locked")):
        block = o._stage1_suspects_block()
    assert block == ""


def test_orchestrator_options_defaults():
    """Sanity check that the options dataclass holds the right defaults."""
    opts = OrchestratorOptions(target="x.sol")
    assert opts.chain == "mainnet"
    assert opts.scope is None
    assert opts.model == "opus"
    assert opts.codex_model == "gpt-5.5"
    assert opts.deep is False
    assert opts.with_pocs is True
    assert opts.dry_run is False
