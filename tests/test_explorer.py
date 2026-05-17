"""Tests for harness.explorer — pure parsing logic, no live API calls."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

from harness.explorer import (
    DeploymentInfo,
    creator_deployments,
    get_deployment_info,
    outgoing_call_targets,
    participants,
    recent_transactions,
    token_transfers,
)


def _fake_resp(json_data, status=200):
    r = MagicMock()
    r.status_code = status
    r.raise_for_status = MagicMock()
    r.json.return_value = json_data
    return r


def test_recent_transactions_requires_api_key(monkeypatch):
    monkeypatch.delenv("ETHERSCAN_API_KEY", raising=False)
    try:
        recent_transactions("0x0001")
        assert False, "should have raised"
    except RuntimeError as e:
        assert "ETHERSCAN_API_KEY" in str(e)


def test_recent_transactions_parses_response(monkeypatch):
    monkeypatch.setenv("ETHERSCAN_API_KEY", "test")
    fake_txs = {
        "status": "1",
        "result": [
            {"hash": "0xa", "from": "0xAA", "to": "0xBB", "blockNumber": "100", "value": "0"},
            {"hash": "0xb", "from": "0xCC", "to": "0xBB", "blockNumber": "101", "value": "1000"},
        ],
    }
    with patch("harness.explorer.httpx.get", return_value=_fake_resp(fake_txs)):
        out = recent_transactions("0xBB", n=10)
    assert len(out) == 2
    assert out[0]["from"] == "0xAA"


def test_participants_aggregates(monkeypatch):
    monkeypatch.setenv("ETHERSCAN_API_KEY", "test")
    fake_txs = {
        "status": "1",
        "result": [
            {"hash": "0xa", "from": "0xAA", "to": "0xBB", "blockNumber": "100", "value": "10"},
            {"hash": "0xb", "from": "0xAA", "to": "0xBB", "blockNumber": "101", "value": "20"},
            {"hash": "0xc", "from": "0xCC", "to": "0xBB", "blockNumber": "102", "value": "5"},
        ],
    }
    with patch("harness.explorer.httpx.get", return_value=_fake_resp(fake_txs)):
        df = participants("0xBB", n=10)
    assert len(df) == 2
    assert df.loc["0xAA", "calls"] == 2
    assert df.loc["0xCC", "calls"] == 1
    assert df.loc["0xAA", "eth_value_sent_wei"] == 30


def test_token_transfers_returns_dataframe(monkeypatch):
    monkeypatch.setenv("ETHERSCAN_API_KEY", "test")
    fake = {
        "status": "1",
        "result": [
            {
                "blockNumber": "100", "timeStamp": "1700000000",
                "hash": "0xa", "from": "0xAA", "to": "0xBB",
                "tokenSymbol": "USDC", "value": "1000000", "tokenDecimal": "6",
            },
        ],
    }
    with patch("harness.explorer.httpx.get", return_value=_fake_resp(fake)):
        df = token_transfers("0xBB", n=10, kind="erc20")
    assert len(df) == 1
    assert df.iloc[0]["tokenSymbol"] == "USDC"


def test_creator_deployments_filters_to_creation_txs(monkeypatch):
    monkeypatch.setenv("ETHERSCAN_API_KEY", "test")
    # Mix of regular txs (to set) and creation txs (to="", contractAddress set)
    fake_txs = {
        "status": "1",
        "result": [
            {"hash": "0xa", "from": "0xDEPLOYER", "to": "", "contractAddress": "0xNEWCONTRACT", "blockNumber": "100", "value": "0"},
            {"hash": "0xb", "from": "0xDEPLOYER", "to": "0xOLD", "contractAddress": "", "blockNumber": "101", "value": "0"},
            {"hash": "0xc", "from": "0xDEPLOYER", "to": None, "contractAddress": "0xNEWER", "blockNumber": "102", "value": "0"},
        ],
    }
    with patch("harness.explorer.httpx.get", return_value=_fake_resp(fake_txs)):
        out = creator_deployments("0xDEPLOYER")
    assert len(out) == 2
    assert {o["contractAddress"] for o in out} == {"0xNEWCONTRACT", "0xNEWER"}


def test_get_deployment_info_handles_missing_source():
    # When fetch_verified_source raises, get_deployment_info should still
    # return a DeploymentInfo with empty source fields, not crash.
    with patch("harness.explorer._fetch_source", side_effect=Exception("no source")):
        with patch("harness.explorer._api_key", return_value=None):
            info = get_deployment_info("0x0001", chain="mainnet")
    assert info.address == "0x0001"
    assert info.chain_id == 1
    assert info.contract_name is None
    assert info.source_files == {}
