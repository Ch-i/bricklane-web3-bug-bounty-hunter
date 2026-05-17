"""Tests for harness.stage1 — signal gatherers + Opus output parser (no live LLM)."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

from harness.candidates import Candidate
from harness.stage1 import (
    Stage1Result,
    _contract_names,
    _file_metrics,
    _grep_primitives,
    _select_most_suspect_file,
    apply_to_candidate,
    rank_candidate,
)


def _make_project(tmp_path, files):
    """files: dict[relative_path, source]"""
    root = tmp_path / "src"
    root.mkdir(parents=True, exist_ok=True)
    for rel, src in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(src)
    return root.parent  # project root


def test_grep_primitives_counts_each(tmp_path):
    root = _make_project(tmp_path, {
        "Foo.sol": """
pragma solidity ^0.8.20;
contract Foo {
    address admin;
    function destroy() external { selfdestruct(payable(admin)); }
    function unsafe(address t, bytes calldata d) external returns (bool ok) {
        (ok,) = t.delegatecall(d);
    }
    function origin() external view returns (address) {
        return tx.origin;
    }
    function math(uint a, uint b) external pure returns (uint) {
        unchecked { return a - b; }
    }
}
""",
    })
    counts = _grep_primitives(root)
    assert counts["selfdestruct"] >= 1
    assert counts["delegatecall"] >= 1
    assert counts["tx.origin"] >= 1
    assert counts["unchecked"] >= 1


def test_file_metrics_skips_libs(tmp_path):
    root = _make_project(tmp_path, {
        "Foo.sol": "contract Foo {}",
    })
    # Add a lib/ file we should skip.
    (root / "lib").mkdir(parents=True)
    (root / "lib" / "Oz.sol").write_text("contract Oz {}")
    # Add a test/ file we should skip.
    (root / "test").mkdir(parents=True)
    (root / "test" / "FooTest.sol").write_text("contract FT {}")

    metrics = _file_metrics(root)
    assert len(metrics) == 1
    assert metrics[0]["path"].endswith("Foo.sol")


def test_select_most_suspect_prefers_danger_density():
    metrics = [
        {"path": "low.sol", "abs_path": "/x/low.sol", "sloc": 100, "dangers": 1, "danger_density": 0.01},
        {"path": "high.sol", "abs_path": "/x/high.sol", "sloc": 100, "dangers": 30, "danger_density": 0.3},
        {"path": "huge.sol", "abs_path": "/x/huge.sol", "sloc": 2000, "dangers": 5, "danger_density": 0.0025},
    ]
    selected = _select_most_suspect_file(metrics)
    assert selected is not None
    assert "high.sol" in str(selected)


def test_contract_names_extracts(tmp_path):
    root = _make_project(tmp_path, {
        "Foo.sol": "contract Foo {}\ncontract Bar {}",
        "Baz.sol": "abstract contract Baz {}",
    })
    names = _contract_names(root)
    assert set(names) >= {"Foo", "Bar", "Baz"}


def test_apply_to_candidate_mutates_triage_fields():
    cand = Candidate(
        id="test-1", platform="c4", kind="source-only",
        title="t", sourced_at="2026-05-18T00:00:00+00:00",
    )
    result = Stage1Result(
        candidate_id="test-1",
        score=7,
        rationale="custom math, unchecked block",
        top_suspects=[{"file": "src/Math.sol", "function": "mulDiv", "why": "rounding"}],
        skip_reasons=[],
    )
    apply_to_candidate(cand, result)
    assert cand.triage_status == "stage1"
    assert cand.triage_score == 7.0
    assert cand.triage_rationale == "custom math, unchecked block"
    assert cand.triage_top_suspects[0]["file"] == "src/Math.sol"
    assert cand.last_triaged_at is not None


def _fake_claude_response(score=7, rationale="ok", suspects=None, skips=None):
    payload = {
        "score": score,
        "rationale": rationale,
        "top_suspects": suspects or [],
        "skip_reasons": skips or [],
    }
    wrapper = {"result": json.dumps(payload)}
    proc = MagicMock()
    proc.returncode = 0
    proc.stdout = json.dumps(wrapper)
    proc.stderr = ""
    return proc


def test_rank_candidate_parses_well_formed_response(tmp_path):
    root = _make_project(tmp_path, {"Foo.sol": "contract Foo {}"})
    cand = Candidate(
        id="c4-test", platform="c4", kind="source-only",
        title="t", sourced_at="2026-05-18T00:00:00+00:00",
    )
    with patch("harness.stage1.subprocess.run",
               return_value=_fake_claude_response(score=8, rationale="strong surface")):
        r = rank_candidate(cand, root)
    assert r.score == 8
    assert "strong surface" in r.rationale


def test_rank_candidate_clamps_out_of_range(tmp_path):
    root = _make_project(tmp_path, {"Foo.sol": "contract Foo {}"})
    cand = Candidate(
        id="c4-test", platform="c4", kind="source-only",
        title="t", sourced_at="2026-05-18T00:00:00+00:00",
    )
    with patch("harness.stage1.subprocess.run",
               return_value=_fake_claude_response(score=42)):
        r = rank_candidate(cand, root)
    assert r.score == 10  # clamped
