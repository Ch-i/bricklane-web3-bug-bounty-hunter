"""Tests for sherlock / cantina / immunefi ingestors — pure parsing."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from crawlers.sherlock_audits import _candidate_from_api as sherlock_from_api
from crawlers.sherlock_audits import _candidate_from_github as sherlock_from_gh
from crawlers.cantina_audits import _candidate_from_api as cantina_from_api
from crawlers.immunefi_programs import (
    _candidate_from_api as immunefi_from_api,
    _extract_addresses,
)


def test_sherlock_from_api_parses_full_entry():
    entry = {
        "slug": "2026-05-some-protocol",
        "name": "Some Protocol Audit",
        "rewards": "100K",
        "ends_at": "2026-05-25T18:00:00+00:00",
        "repository": "https://github.com/sherlock-protocol/2026-05-some-protocol",
    }
    c = sherlock_from_api(entry, "2026-05-18T00:00:00+00:00")
    assert c is not None
    assert c.id == "sherlock-2026-05-some-protocol"
    assert c.platform == "sherlock"
    assert c.payout_max_usd == 100_000
    assert c.repo_url == "https://github.com/sherlock-protocol/2026-05-some-protocol"


def test_sherlock_from_api_handles_missing_fields():
    c = sherlock_from_api({"title": "untitled"}, "2026-05-18T00:00:00+00:00")
    assert c is not None
    assert c.id == "sherlock-untitled"
    assert c.payout_max_usd is None
    assert c.closes_at is None


def test_sherlock_from_github_uses_repo_name():
    c = sherlock_from_gh(
        {
            "name": "2026-05-foo-audit",
            "html_url": "https://github.com/sherlock-protocol/2026-05-foo-audit",
            "description": "Foo audit",
        },
        "2026-05-18T00:00:00+00:00",
    )
    assert c.id == "sherlock-2026-05-foo-audit"
    assert "Foo audit" in c.notes


def test_cantina_from_api_parses_full():
    entry = {
        "slug": "barfi",
        "title": "Barfi Competition",
        "prize": "$50,000",
        "end_date": "2026-06-01T00:00:00+00:00",
        "repository_url": "https://github.com/CantinaCompetitions/barfi",
    }
    c = cantina_from_api(entry, "2026-05-18T00:00:00+00:00")
    assert c is not None
    assert c.id == "cantina-barfi"
    assert c.payout_max_usd == 50_000


def test_immunefi_extract_addresses_from_list_of_strings():
    scope = [
        "Contract A: 0xAAaAaaAAaaaAAaaaAAAAaAaAaAAAAAaAAAAaAAaa",
        "vault: 0xBbBBBBbbbbbbBBbbbbbbBbBbBBBBbBbbBbbBbBbb on optimism",
        "non-address-text",
    ]
    addrs, chain = _extract_addresses(scope)
    assert len(addrs) == 2
    # chain pulled from explicit chain hint in the second entry — only if it
    # appears as a dict field, which it doesn't here, so chain may be None.


def test_immunefi_extract_addresses_dedups_case_insensitive():
    scope = [
        "0xabcdef0123456789abcdef0123456789abcdef01",
        "0xABCDEF0123456789ABCDEF0123456789ABCDEF01",  # same as above, different case
        "0xdeadbeef0123456789abcdef0123456789abcdef",
    ]
    addrs, _ = _extract_addresses(scope)
    assert len(addrs) == 2


def test_immunefi_extract_addresses_from_dict_with_chain_hint():
    scope = {
        "chain": "arbitrum",
        "assets": [
            "0x1234567890abcdef1234567890abcdef12345678",
        ],
    }
    addrs, chain = _extract_addresses(scope)
    assert len(addrs) == 1
    assert chain == 42161  # arbitrum's chain id


def test_immunefi_from_api_constructs_deployed_candidate():
    entry = {
        "slug": "aave-v4",
        "name": "Aave V4",
        "maxBounty": "1M",
        "scope": [
            {"chain": "ethereum", "asset": "0xAA00aA00aA00aA00aA00aA00aA00aA00aA00aA00"},
        ],
        "description": "Aave V4 mainnet program",
    }
    c = immunefi_from_api(entry, "2026-05-18T00:00:00+00:00")
    assert c is not None
    assert c.id == "immunefi-aave-v4"
    assert c.platform == "immunefi"
    assert c.kind == "deployed"
    assert c.payout_max_usd == 1_000_000
    assert c.chain_id == 1  # ethereum -> mainnet
    assert len(c.addresses) == 1
