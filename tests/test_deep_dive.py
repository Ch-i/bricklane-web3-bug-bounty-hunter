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


def test_function_analysis_parses_invariants(tmp_path):
    """analyze_function should parse invariants_assumed + invariants_established."""
    from harness.deep_dive import analyze_function

    src = """contract Bank {
    function withdraw() external {}
}"""
    p = _write(tmp_path, "Bank.sol", src)
    units = decompose_file(p, tmp_path)
    u = units[0]

    fake_payload = {
        "function_id": u.fn_id,
        "summary": "withdraw all",
        "state_writes": [],
        "external_calls": [],
        "invariants_assumed": [
            "balances[msg.sender] >= amount",
            "totalSupply == sum(balances)",
        ],
        "invariants_established": [
            "balances[msg.sender] == prev - amount",
        ],
        "candidate_vulnerabilities": [],
        "safe_observations": [],
    }
    proc = MagicMock()
    proc.returncode = 0
    proc.stdout = json.dumps({"result": json.dumps(fake_payload)})
    proc.stderr = ""

    with patch("harness.deep_dive.subprocess.run", return_value=proc):
        a = analyze_function(u, tmp_path)
    assert "balances[msg.sender] >= amount" in a.invariants_assumed
    assert "totalSupply == sum(balances)" in a.invariants_assumed
    assert len(a.invariants_established) == 1


def test_function_analysis_truncates_long_invariants(tmp_path):
    """Each invariant is capped at 300 chars; list capped at 20."""
    from harness.deep_dive import analyze_function

    src = "contract X { function f() external {} }"
    p = _write(tmp_path, "X.sol", src)
    u = decompose_file(p, tmp_path)[0]

    fake_payload = {
        "function_id": u.fn_id,
        "summary": "x",
        "invariants_assumed": ["x" * 500],  # too long
        "invariants_established": ["a"] * 30,  # too many
        "state_writes": [], "external_calls": [],
        "candidate_vulnerabilities": [], "safe_observations": [],
    }
    proc = MagicMock()
    proc.returncode = 0
    proc.stdout = json.dumps({"result": json.dumps(fake_payload)})

    with patch("harness.deep_dive.subprocess.run", return_value=proc):
        a = analyze_function(u, tmp_path)
    assert len(a.invariants_assumed[0]) == 300
    assert len(a.invariants_established) == 20


def test_render_invariants_produces_focused_doc():
    """render_invariants should aggregate + section the invariants nicely."""
    from harness.deep_dive import CrossFnAnalysis, render_invariants

    fns = {
        "F.sol::F::deposit": FunctionAnalysis(
            function_id="F.sol::F::deposit", summary="dep",
            invariants_established=["totalSupply == sum(balances)"],
        ),
        "F.sol::F::mint": FunctionAnalysis(
            function_id="F.sol::F::mint", summary="mint",
            invariants_established=["totalSupply == sum(balances)"],
            invariants_assumed=["caller has MINTER_ROLE"],
        ),
    }
    cross = [
        CrossFnAnalysis(
            pair_id="deposit+mint", shared_state=["totalSupply"],
            broken_invariants=[
                {"invariant": "totalSupply == sum(balances)",
                 "broken_by": "mint",
                 "how": "increments totalSupply without updating balances"}
            ],
        ),
    ]
    doc = render_invariants(Path("/x/MyContract"), fns, cross)
    assert "Invariants — MyContract" in doc
    assert "Postconditions established" in doc
    assert "totalSupply == sum(balances)" in doc
    assert "Established by 2 function(s)" in doc
    assert "caller has MINTER_ROLE" in doc
    assert "Detected invariant breakages" in doc
    assert "increments totalSupply without updating balances" in doc
    assert "Suggested next steps" in doc


def test_render_invariants_empty_input_has_placeholder():
    from harness.deep_dive import render_invariants
    doc = render_invariants(Path("/x/Empty"), {}, [])
    assert "No explicit invariants surfaced" in doc


def test_render_report_aggregates_invariants_across_fns():
    """When multiple functions assume/establish the same invariant, the
    aggregated section should group them and surface a count."""
    from harness.deep_dive import CrossFnAnalysis, render_report

    fns = {
        "F.sol::F::deposit": FunctionAnalysis(
            function_id="F.sol::F::deposit", summary="dep",
            invariants_established=["totalSupply == sum(balances)"],
        ),
        "F.sol::F::mint": FunctionAnalysis(
            function_id="F.sol::F::mint", summary="mint",
            invariants_established=["totalSupply == sum(balances)"],  # same!
        ),
        "F.sol::F::transfer": FunctionAnalysis(
            function_id="F.sol::F::transfer", summary="xfer",
            invariants_assumed=["balances[u] >= amount"],
        ),
    }
    units = [
        FunctionUnit(file="F.sol", contract="F", name=n, visibility="external",
                     mutability="nonpayable", line_start=1, line_end=2, source="//")
        for n in ("deposit", "mint", "transfer")
    ]
    report = render_report(Path("."), units, fns, [])
    assert "Aggregated invariants" in report
    # The shared invariant appears once with count 2
    assert "totalSupply == sum(balances)" in report
    assert "(2 fn)" in report
    # Assumed section also surfaces
    assert "balances[u] >= amount" in report
    assert "fuzz-target candidates" in report


def test_render_report_includes_invariants():
    """render_report should surface assumed + established invariants per function."""
    from harness.deep_dive import CrossFnAnalysis, render_report

    fn = FunctionAnalysis(
        function_id="Bank.sol::Bank::withdraw",
        summary="withdraw all",
        invariants_assumed=["balances[u] >= amount"],
        invariants_established=["balances[u] decreased"],
    )
    cross = [
        CrossFnAnalysis(
            pair_id="A+B",
            shared_state=["balances"],
            interaction_kind="shares-state",
            broken_invariants=[
                {"invariant": "totalSupply == sum(balances)",
                 "broken_by": "b", "how": "mints without increasing total"}
            ],
            vulnerabilities=[],
        ),
    ]
    units = [FunctionUnit(file="Bank.sol", contract="Bank", name="withdraw",
                          visibility="external", mutability="nonpayable",
                          line_start=1, line_end=10, source="//")]
    report = render_report(Path("."), units, {"Bank.sol::Bank::withdraw": fn}, cross)
    assert "Assumes invariants" in report
    assert "balances[u] >= amount" in report
    assert "Establishes invariants" in report
    assert "Invariant breakages" in report
    assert "totalSupply == sum(balances)" in report
    assert "mints without increasing total" in report


def test_corpus_priors_for_fn_boosts_synthesis_source(monkeypatch):
    """Synthesis-source entries should come first in the prior-art list,
    ahead of Solodit/SWC entries even if they have lower severity."""
    from dataclasses import dataclass

    from harness import deep_dive

    @dataclass
    class FakeHit:
        id: str
        title: str
        source: str
        severity: str

    # Build a mock corpus.search that returns a mix
    def fake_search(query: str, top_k: int = 5):
        return [
            FakeHit(id="solodit-crit-1", title="solodit critical", source="solodit", severity="Critical"),
            FakeHit(id="synth-low-2", title="synthesis low", source="synthesis", severity="Low"),
            FakeHit(id="swc-high-3", title="swc high", source="swc", severity="High"),
            FakeHit(id="synth-med-4", title="synthesis medium", source="synthesis", severity="Medium"),
        ]

    monkeypatch.setattr(deep_dive.corpus, "search", fake_search)

    u = FunctionUnit(
        file="V.sol", contract="V", name="myFn",
        visibility="external", mutability="nonpayable",
        line_start=1, line_end=10, source="function myFn() external {}",
        danger_grep={"delegatecall": 1},
    )
    priors = deep_dive._corpus_priors_for_fn(u)

    # First two entries must both be synthesis-source
    assert priors[0]["source"] == "synthesis"
    assert priors[1]["source"] == "synthesis"
    # Within synthesis, Medium ranks above Low
    assert priors[0]["id"] == "synth-med-4"
    assert priors[1]["id"] == "synth-low-2"
    # Then the non-synthesis entries follow, in severity order
    assert priors[2]["id"] == "solodit-crit-1"
    assert priors[3]["id"] == "swc-high-3"


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


def test_shared_state_pairs_uses_invariant_overlap(tmp_path):
    """Functions that share invariants (A establishes X, B assumes X) should
    be paired even if their state_writes don't overlap."""
    src = """contract Vault {
    uint256 totalShares;
    uint256 totalAssets;
    function deposit() external {}
    function priceCheck() external view {}
}"""
    p = _write(tmp_path, "Vault.sol", src)
    units = decompose_file(p, tmp_path)
    by_name = {u.name: u for u in units}

    analyses = {
        by_name["deposit"].fn_id: FunctionAnalysis(
            function_id=by_name["deposit"].fn_id,
            state_writes=[{"slot": "totalShares", "condition": "always"}],
            invariants_established=["totalShares >= 0"],
        ),
        by_name["priceCheck"].fn_id: FunctionAnalysis(
            function_id=by_name["priceCheck"].fn_id,
            state_writes=[],  # view function, no writes
            invariants_assumed=["totalShares >= 0"],  # same invariant!
        ),
    }
    pairs = _shared_state_pairs(units, analyses, max_pairs=10)
    # Even with no overlapping state_writes, the shared invariant should pair them
    assert len(pairs) >= 1
    a, b, overlap = pairs[0]
    fn_ids = {a.fn_id, b.fn_id}
    assert by_name["deposit"].fn_id in fn_ids
    assert by_name["priceCheck"].fn_id in fn_ids
    # The overlap should include the invariant prefix
    assert any(o.startswith("INV:") for o in overlap)


def test_shared_state_pairs_dedups_orderless(tmp_path):
    """(a, b) and (b, a) should be returned once, not twice."""
    src = """contract X {
    uint256 z;
    function a() external { z = 1; }
    function b() external { z = 2; }
}"""
    p = _write(tmp_path, "X.sol", src)
    units = decompose_file(p, tmp_path)
    analyses = {
        u.fn_id: FunctionAnalysis(
            function_id=u.fn_id,
            state_writes=[{"slot": "z", "condition": "always"}],
        )
        for u in units
    }
    pairs = _shared_state_pairs(units, analyses, max_pairs=10)
    # Exactly one pair, not two
    assert len(pairs) == 1


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
    # Exactly 1 pair: deposit↔withdraw (deduped — order-independent)
    assert len(pairs) == 1
    a, b, shared = pairs[0]
    assert "balances" in shared
