"""Tests for harness.deep_dive — decomposition + parsing (no live LLM)."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from harness.deep_dive import (
    FunctionAnalysis,
    FunctionUnit,
    _match_braces,
    _shared_state_pairs,
    analyze_function,
    decompose,
    decompose_file,
)


def _write(tmp_path: Path, rel: str, src: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(src)
    return p


def test_match_braces_handles_strings_and_comments():
    src = '{ if (x) { /* } */ } "}\\"}" }'
    end = _match_braces(src, 0)
    assert end == len(src)


def test_decompose_file_finds_normal_functions(tmp_path):
    src = '''
contract Foo {
    uint256 public x;

    function deposit() external payable {
        x += msg.value;
    }

    function withdraw(uint256 amt) external {
        require(amt <= x);
        (bool ok,) = msg.sender.call{value: amt}("");
        require(ok);
        x -= amt;
    }

    receive() external payable {}

    fallback() external {
        revert();
    }
}
'''
    p = _write(tmp_path, "Foo.sol", src)
    units = decompose_file(p, tmp_path)
    names = {u.name for u in units}
    assert "deposit" in names
    assert "withdraw" in names
    assert "receive" in names or "fallback" in names  # at least one of the unnamed


def test_decompose_extracts_visibility_and_mutability(tmp_path):
    src = '''
contract Foo {
    function pub() public pure returns (uint) { return 1; }
    function ext() external view returns (uint) { return 2; }
    function priv() private {}
    function pay() external payable {}
}
'''
    p = _write(tmp_path, "Foo.sol", src)
    units = decompose_file(p, tmp_path)
    by = {u.name: u for u in units}
    assert by["pub"].visibility == "public"
    assert by["pub"].mutability == "pure"
    assert by["ext"].visibility == "external"
    assert by["ext"].mutability == "view"
    assert by["priv"].visibility == "private"
    assert by["pay"].mutability == "payable"


def test_decompose_skips_libs_and_tests(tmp_path):
    _write(tmp_path, "src/A.sol", "contract A { function a() public {} }")
    _write(tmp_path, "lib/L.sol", "contract L { function l() public {} }")
    _write(tmp_path, "test/T.sol", "contract T { function t() public {} }")
    units = decompose(tmp_path)
    fn_ids = {u.fn_id for u in units}
    assert any("A.sol" in i for i in fn_ids)
    assert not any("L.sol" in i for i in fn_ids)
    assert not any("T.sol" in i for i in fn_ids)


def test_decompose_extracts_danger_grep(tmp_path):
    src = '''
contract Risky {
    function unsafe(address t, bytes calldata d) external {
        (bool ok, ) = t.delegatecall(d);
        require(ok);
    }
    function auth(address admin) external {
        require(tx.origin == admin);
    }
}
'''
    p = _write(tmp_path, "Risky.sol", src)
    units = decompose_file(p, tmp_path)
    by = {u.name: u for u in units}
    assert by["unsafe"].danger_grep.get("delegatecall", 0) >= 1
    assert by["auth"].danger_grep.get("tx.origin", 0) >= 1


def test_decompose_extracts_modifiers(tmp_path):
    """Modifiers contain critical access-control logic — must be analyzed too."""
    src = '''
contract Auth {
    address public owner;
    mapping(address => bool) admins;

    modifier onlyOwner() {
        require(msg.sender == owner, "not owner");
        _;
    }

    modifier onlyAdmin(uint256 role) {
        require(admins[msg.sender], "no role");
        require(role > 0);
        _;
    }

    modifier nonReentrant {
        _;
    }

    function setOwner(address x) external onlyOwner {
        owner = x;
    }
}
'''
    p = _write(tmp_path, "Auth.sol", src)
    units = decompose_file(p, tmp_path)
    names = {u.name for u in units}
    # Modifier definitions must be discovered
    assert "onlyOwner" in names, f"missing onlyOwner; got {names}"
    assert "onlyAdmin" in names
    assert "nonReentrant" in names, "modifier without parens must still be found"
    assert "setOwner" in names

    # And modifiers should be tied to the right contract
    by = {u.name: u for u in units}
    assert by["onlyOwner"].contract == "Auth"
    assert by["nonReentrant"].contract == "Auth"


def test_decompose_modifier_body_captures_require(tmp_path):
    """The source slice for a modifier must include its require checks."""
    src = '''
contract X {
    address owner;
    modifier onlyOwner() {
        require(msg.sender == owner, "denied");
        _;
    }
}
'''
    p = _write(tmp_path, "X.sol", src)
    units = decompose_file(p, tmp_path)
    by = {u.name: u for u in units}
    assert "require(msg.sender == owner" in by["onlyOwner"].source


def test_function_analysis_max_severity():
    a = FunctionAnalysis(
        function_id="x",
        candidate_vulnerabilities=[
            {"severity": "Low", "title": "low bug"},
            {"severity": "High", "title": "high bug"},
            {"severity": "Medium", "title": "medium bug"},
        ],
    )
    assert a.max_severity == "High"


def test_analyze_function_parses_well_formed_response(tmp_path):
    src = """contract Foo {
    function withdraw() external {}
}"""
    p = _write(tmp_path, "Foo.sol", src)
    units = decompose_file(p, tmp_path)
    u = units[0]

    fake_payload = {
        "function_id": u.fn_id,
        "summary": "external withdraw, no body",
        "trust_boundary": "anyone",
        "value_flow": "no value moves",
        "state_writes": [],
        "external_calls": [],
        "candidate_vulnerabilities": [
            {"title": "Empty function pattern", "severity": "Low", "confidence": "low",
             "precondition": "any", "impact": "denial-of-service stub",
             "blocked_by_solc_08_checks": False, "poc_sketch": None,
             "description": "intentional placeholder"},
        ],
        "safe_observations": ["no external call"],
        "notes": "",
    }
    proc = MagicMock()
    proc.returncode = 0
    proc.stdout = json.dumps({"result": json.dumps(fake_payload)})
    proc.stderr = ""

    with patch("harness.deep_dive.subprocess.run", return_value=proc):
        a = analyze_function(u, tmp_path)
    assert a.function_id == u.fn_id
    assert len(a.candidate_vulnerabilities) == 1
    assert a.candidate_vulnerabilities[0]["title"] == "Empty function pattern"
    assert a.max_severity == "Low"


def test_shared_state_pairs_identifies_overlap(tmp_path):
    # Two functions in same contract that both write to "balances"
    src = """contract Bank {
    mapping(address => uint) balances;
    function deposit() external payable { balances[msg.sender] += msg.value; }
    function withdraw(uint a) external { balances[msg.sender] -= a; payable(msg.sender).transfer(a); }
}"""
    p = _write(tmp_path, "Bank.sol", src)
    units = decompose_file(p, tmp_path)
    analyses = {
        u.fn_id: FunctionAnalysis(
            function_id=u.fn_id,
            state_writes=[{"slot": "balances", "condition": "always"}],
        )
        for u in units
    }
    pairs = _shared_state_pairs(units, analyses, max_pairs=10)
    assert len(pairs) >= 2  # deposit↔withdraw, withdraw↔deposit (or both directions)
    a, b, shared = pairs[0]
    assert "balances" in shared
