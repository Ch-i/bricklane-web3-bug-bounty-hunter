"""Tests for harness.onchain — Sourcify/Etherscan parsing + proxy slot decoding."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from harness.onchain import (
    ADDR_RE,
    FetchedContract,
    _slot_to_address,
    chain_to_id,
    fetch_sourcify,
    fetch_etherscan,
    materialize_to_disk,
)


def test_addr_re():
    assert ADDR_RE.match("0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45")
    assert not ADDR_RE.match("0xnotanaddress")
    assert not ADDR_RE.match("not-an-address")


def test_chain_to_id_accepts_names_and_numbers():
    assert chain_to_id(1) == 1
    assert chain_to_id("mainnet") == 1
    assert chain_to_id("1") == 1
    assert chain_to_id("arbitrum") == 42161
    with pytest.raises(ValueError):
        chain_to_id("nonexistent-chain")


def test_slot_value_to_address():
    # 32-byte slot containing a right-padded address
    full = "0x000000000000000000000000abcdef0123456789abcdef0123456789abcdef01"
    assert _slot_to_address(full) == "0xabcdef0123456789abcdef0123456789abcdef01"
    # Zero address => None
    assert _slot_to_address("0x" + "0" * 64) is None
    assert _slot_to_address(None) is None
    assert _slot_to_address("0xshort") is None


def _fake_response(status_code: int, json_data: dict, text: str | None = None):
    r = MagicMock()
    r.status_code = status_code
    r.json.return_value = json_data
    r.text = text if text is not None else json.dumps(json_data)
    return r


def test_fetch_sourcify_parses_multi_file_response():
    fake_json = {
        "status": "full",
        "files": [
            {
                "name": "Foo.sol",
                "path": "contracts/full_match/1/0x0001/sources/Foo.sol",
                "content": "// SPDX-License-Identifier: MIT\ncontract Foo {}",
            },
            {
                "name": "Bar.sol",
                "path": "contracts/full_match/1/0x0001/sources/lib/Bar.sol",
                "content": "// SPDX-License-Identifier: MIT\ncontract Bar {}",
            },
            {
                "name": "metadata.json",
                "path": "contracts/full_match/1/0x0001/metadata.json",
                "content": json.dumps(
                    {
                        "compiler": {"version": "0.8.20+commit.a1b79de6"},
                        "settings": {"compilationTarget": {"Foo.sol": "Foo"}},
                    }
                ),
            },
        ],
    }
    with patch("harness.onchain.httpx.get", return_value=_fake_response(200, fake_json)):
        result = fetch_sourcify("0x0001", 1)
    assert result is not None
    assert set(result.source_files.keys()) == {"Foo.sol", "lib/Bar.sol"}
    assert result.compiler_version == "0.8.20+commit.a1b79de6"
    assert result.name == "Foo"
    assert "sourcify" in result.fetched_via


def test_fetch_etherscan_handles_double_brace_envelope(monkeypatch):
    """Etherscan wraps multi-file source in {{...}} (literal extra braces).

    Real-world example: SourceCode = "{{\"language\":...}}". After stripping
    one char from each end we get the canonical Solidity Standard Input JSON.
    """
    inner = json.dumps({
        "language": "Solidity",
        "sources": {
            "src/Foo.sol": {"content": "contract Foo {}"},
            "src/Bar.sol": {"content": "contract Bar {}"},
        },
    })
    # Real Etherscan envelope: one extra { and } around the JSON object.
    double_brace = "{" + inner + "}"
    fake = {
        "status": "1",
        "result": [
            {
                "ContractName": "Foo",
                "CompilerVersion": "v0.8.20+commit.a1b79de6",
                "SourceCode": double_brace,
            }
        ],
    }
    monkeypatch.setenv("ETHERSCAN_API_KEY", "test-key")
    with patch("harness.onchain.httpx.get", return_value=_fake_response(200, fake)):
        result = fetch_etherscan("0x0001", 1)
    assert result is not None
    assert "src/Foo.sol" in result.source_files
    assert "src/Bar.sol" in result.source_files
    assert result.compiler_version == "v0.8.20+commit.a1b79de6"


def test_materialize_writes_files_with_directory_structure(tmp_path):
    contract = FetchedContract(
        address="0x0001",
        chain_id=1,
        name="Foo",
        source_files={
            "Foo.sol": "contract Foo {}",
            "lib/Bar.sol": "contract Bar {}",
            "@openzeppelin/contracts/utils/Address.sol": "library Address {}",
        },
        compiler_version="0.8.20",
    )
    out = materialize_to_disk(contract, tmp_path / "out")
    assert (out / "Foo.sol").exists()
    assert (out / "lib/Bar.sol").exists()
    # The @-prefixed path is sanitized (leading @ stripped) so it doesn't look
    # like a hidden file at the FS layer.
    assert (out / "openzeppelin/contracts/utils/Address.sol").exists()
    manifest = json.loads((out / "MANIFEST.json").read_text())
    assert manifest["address"] == "0x0001"
    assert manifest["file_count"] == 3


def test_materialize_writes_implementation_into_impl_subdir(tmp_path):
    impl = FetchedContract(
        address="0x0002",
        chain_id=1,
        name="ImplV1",
        source_files={"ImplV1.sol": "contract ImplV1 {}"},
    )
    proxy = FetchedContract(
        address="0x0001",
        chain_id=1,
        name="Proxy",
        source_files={"Proxy.sol": "contract Proxy {}"},
        is_proxy=True,
        implementation_address="0x0002",
        implementation=impl,
    )
    out = materialize_to_disk(proxy, tmp_path / "out")
    assert (out / "Proxy.sol").exists()
    assert (out / "impl/ImplV1.sol").exists()
