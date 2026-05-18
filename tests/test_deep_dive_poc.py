"""Tests for harness/deep_dive_poc — converting poc_sketches into Foundry PoCs."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from harness import deep_dive_poc
from harness.schema import FoundryPoc


def test_convert_sketch_skips_empty_sketch():
    """Empty/short poc_sketches should return None without LLM call."""
    out = deep_dive_poc._convert_sketch({"poc_sketch": ""}, "X.sol::X::fn")
    assert out is None
    out = deep_dive_poc._convert_sketch({"poc_sketch": "short"}, "X.sol::X::fn")
    assert out is None
    out = deep_dive_poc._convert_sketch({}, "X.sol::X::fn")  # no key at all
    assert out is None


def test_convert_sketch_parses_well_formed_response():
    candidate = {
        "title": "Reentrancy in withdraw",
        "severity": "High",
        "precondition": "attacker has balance > 0",
        "impact": "drains the contract",
        "poc_sketch": "Attacker calls withdraw which calls back via fallback",
    }
    fake_payload = {
        "test_name": "test_reentrancyDrain",
        "setup": "Vault v = new Vault(); v.deposit{value: 10}();",
        "exploit": "Attacker a = new Attacker(v); a.attack();",
        "assertion": "assertEq(address(v).balance, 0);",
        "imports": ["../../src/Vault.sol"],
        "notes": "Standard reentrancy",
    }
    proc = MagicMock()
    proc.returncode = 0
    proc.stdout = json.dumps({"result": json.dumps(fake_payload)})

    with patch("harness.deep_dive_poc.shutil.which", return_value="/fake/claude"):
        with patch("harness.deep_dive_poc.subprocess.run", return_value=proc):
            result = deep_dive_poc._convert_sketch(candidate, "Vault.sol::Vault::withdraw")
    assert isinstance(result, FoundryPoc)
    assert result.test_name == "test_reentrancyDrain"
    assert "Attacker" in result.exploit


def test_convert_sketch_returns_none_when_claude_missing():
    candidate = {"poc_sketch": "a" * 50}  # plausible sketch
    with patch("harness.deep_dive_poc.shutil.which", return_value=None):
        result = deep_dive_poc._convert_sketch(candidate, "X.sol::X::fn")
    assert result is None


def test_convert_sketch_returns_none_on_subprocess_timeout():
    candidate = {"poc_sketch": "a" * 50}
    with patch("harness.deep_dive_poc.shutil.which", return_value="/fake/claude"):
        with patch("harness.deep_dive_poc.subprocess.run",
                   side_effect=subprocess.TimeoutExpired("claude", 60)):
            result = deep_dive_poc._convert_sketch(candidate, "X.sol::X::fn")
    assert result is None


def test_convert_sketch_returns_none_on_malformed_json():
    candidate = {"poc_sketch": "a" * 50}
    proc = MagicMock()
    proc.returncode = 0
    proc.stdout = "not valid json at all"
    with patch("harness.deep_dive_poc.shutil.which", return_value="/fake/claude"):
        with patch("harness.deep_dive_poc.subprocess.run", return_value=proc):
            result = deep_dive_poc._convert_sketch(candidate, "X.sol::X::fn")
    assert result is None


def test_materialize_for_run_missing_per_function_jsonl(tmp_path: Path):
    with pytest.raises(FileNotFoundError, match="no per-function.jsonl"):
        deep_dive_poc.materialize_for_run(tmp_path, tmp_path)


def test_materialize_for_run_filters_by_severity(tmp_path: Path):
    """Only candidates >= min_severity should be materialized."""
    target = tmp_path / "src" / "Vault.sol"
    target.parent.mkdir()
    target.write_text("contract V { function deposit() external {} }")
    dd_dir = tmp_path / "dd"
    dd_dir.mkdir()

    (dd_dir / "per-function.jsonl").write_text("\n".join([
        json.dumps({
            "function_id": "src/Vault.sol::V::deposit",
            "candidate_vulnerabilities": [
                {"title": "Critical bug", "severity": "Critical",
                 "poc_sketch": "x" * 50},
                {"title": "Medium bug", "severity": "Medium",
                 "poc_sketch": "y" * 50},
                {"title": "Low bug", "severity": "Low",
                 "poc_sketch": "z" * 50},  # below threshold
            ],
        }),
    ]))

    # Stub _convert_sketch to fail (return None) so we don't run forge
    converted_titles = []
    def fake_convert(candidate, fn_id, **kw):
        converted_titles.append(candidate["title"])
        return None  # nothing materializes
    with patch.object(deep_dive_poc, "_convert_sketch", side_effect=fake_convert):
        # Default min_severity = "High"
        out_path = deep_dive_poc.materialize_for_run(dd_dir, tmp_path)

    # Only Critical should have been attempted (High is the threshold; Critical > High)
    # Medium and Low are below the threshold
    assert converted_titles == ["Critical bug"]
    # Output file exists, empty since nothing materialized
    assert out_path.exists()
    data = json.loads(out_path.read_text())
    assert data == []


def test_materialize_for_run_min_severity_medium_includes_more(tmp_path: Path):
    """With --min-severity Medium, Medium + High + Critical should be attempted."""
    dd_dir = tmp_path / "dd"
    dd_dir.mkdir()
    (dd_dir / "per-function.jsonl").write_text(json.dumps({
        "function_id": "f.sol::F::a",
        "candidate_vulnerabilities": [
            {"title": "Crit", "severity": "Critical", "poc_sketch": "x" * 50},
            {"title": "High", "severity": "High", "poc_sketch": "x" * 50},
            {"title": "Med", "severity": "Medium", "poc_sketch": "x" * 50},
            {"title": "Low", "severity": "Low", "poc_sketch": "x" * 50},
        ],
    }))

    attempted = []
    def fake_convert(candidate, fn_id, **kw):
        attempted.append(candidate["title"])
        return None
    with patch.object(deep_dive_poc, "_convert_sketch", side_effect=fake_convert):
        deep_dive_poc.materialize_for_run(dd_dir, tmp_path, min_severity="Medium")
    assert attempted == ["Crit", "High", "Med"]


def test_render_materialization_summary_empty(tmp_path: Path):
    p = tmp_path / "x.json"
    p.write_text(json.dumps([]))
    summary = deep_dive_poc.render_materialization_summary(p)
    assert "no candidates above threshold" in summary or "(no" in summary


def test_render_materialization_summary_groups_by_status_and_severity(tmp_path: Path):
    p = tmp_path / "x.json"
    p.write_text(json.dumps([
        {"title": "a", "severity": "High", "poc_status": "reproduced"},
        {"title": "b", "severity": "Critical", "poc_status": "compile-failed"},
        {"title": "c", "severity": "High", "poc_status": "reproduced"},
    ]))
    summary = deep_dive_poc.render_materialization_summary(p)
    assert "materialized: 3" in summary
    assert "High=2" in summary
    assert "Critical=1" in summary
    assert "reproduced=2" in summary
    assert "compile-failed=1" in summary
