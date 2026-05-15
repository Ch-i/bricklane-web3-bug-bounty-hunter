"""Tests for harness.poc — scaffold + execute Foundry PoCs."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from harness.poc import (
    _normalize_test_name,
    _sanitize_contract_name,
    execute_poc,
    scaffold_poc,
)
from harness.schema import Finding, FindingLocation, FoundryPoc


def _make_finding(**overrides) -> Finding:
    base = dict(
        title="Reentrancy in withdraw()",
        severity="High",
        location=[FindingLocation(file="Foo.sol", line_start=1)],
        description="...",
        impact="...",
        recommendation="...",
        citations=["swc-107"],
        novel=False,
        confidence="high",
        discovered_by="claude",
        foundry_poc=FoundryPoc(
            test_name="test_drains",
            setup="Vault v = new Vault();",
            exploit="v.withdraw(100);",
            assertion="assertEq(v.balance, 0);",
            imports=["../src/Vault.sol"],
            notes=None,
        ),
    )
    base.update(overrides)
    return Finding.model_validate(base)


def test_sanitize_contract_name_camelcases_and_appends_Test():
    assert _sanitize_contract_name("Reentrancy in withdraw()") == "ReentrancyInWithdrawTest"
    assert _sanitize_contract_name("1bad-first-char") == "F1badFirstCharTest"
    assert _sanitize_contract_name("") == "FindingTest"


def test_normalize_test_name_prepends_test():
    assert _normalize_test_name("drains") == "test_drains"
    assert _normalize_test_name("test_already_prefixed") == "test_already_prefixed"
    assert _normalize_test_name("foo bar") == "test_foo_bar"


def test_scaffold_writes_compileable_shape(tmp_path):
    f = _make_finding()
    result = scaffold_poc(f, out_dir=tmp_path)
    assert result is not None
    content = result.test_path.read_text()
    # Solidity essentials present
    assert "pragma solidity ^0.8.20;" in content
    assert "import \"forge-std/Test.sol\";" in content
    assert "import \"../src/Vault.sol\";" in content
    # The four bodies are inlined
    assert "Vault v = new Vault();" in content
    assert "v.withdraw(100);" in content
    assert "assertEq(v.balance, 0);" in content
    # Test contract name + function name follow forge conventions
    assert result.contract_name.endswith("Test")
    assert result.test_name.startswith("test_")
    # The test file references the contract + function names
    assert f"contract {result.contract_name} is Test" in content
    assert f"function {result.test_name}() public" in content


def test_scaffold_returns_none_when_no_foundry_poc(tmp_path):
    f = _make_finding(foundry_poc=None, novel=True, citations=[])
    assert scaffold_poc(f, out_dir=tmp_path) is None


def test_execute_returns_not_applicable_without_foundry(tmp_path):
    # tmp_path has no foundry.toml; executor should bail gracefully.
    fake_test = tmp_path / "X.t.sol"
    fake_test.write_text("// stub")
    result = execute_poc(
        fake_test,
        contract_name="XTest",
        test_name="test_x",
        project_root=tmp_path,
    )
    assert result.status == "not-applicable"
    assert "foundry.toml" in result.stderr.lower() or "forge" in result.stderr.lower()
