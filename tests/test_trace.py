"""Tests for harness.trace — no network, pure parsing + validation."""

from __future__ import annotations

import pytest

from harness.trace import TX_HASH_RE, chain_to_id


def test_tx_hash_re():
    good = "0x" + "a" * 64
    assert TX_HASH_RE.match(good)
    assert not TX_HASH_RE.match("0xshort")
    assert not TX_HASH_RE.match("not-a-hash")


def test_chain_to_id():
    assert chain_to_id("mainnet") == 1
    assert chain_to_id("ethereum") == 1
    assert chain_to_id("arbitrum") == 42161
    assert chain_to_id(8453) == 8453
    assert chain_to_id("8453") == 8453
    with pytest.raises(ValueError):
        chain_to_id("unknown-network")
