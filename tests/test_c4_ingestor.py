"""Tests for crawlers.c4_contests — pure parsing logic, no network."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from crawlers.c4_contests import (
    _candidate_from_github,
    _candidate_from_sveltekit,
    _parse_payout,
    _parse_scope_from_readme,
)


def test_parse_payout_handles_formats():
    assert _parse_payout(100_000) == 100_000
    assert _parse_payout("100K") == 100_000
    assert _parse_payout("$100,000") == 100_000
    assert _parse_payout("1.5M") == 1_500_000
    assert _parse_payout("$1,500,000") == 1_500_000
    assert _parse_payout(None) is None
    assert _parse_payout("invalid") is None


def test_candidate_from_sveltekit_with_full_fields():
    entry = {
        "slug": "2026-05-some-protocol",
        "title": "Some Protocol Audit",
        "totalAmount": "100K",
        "endTime": "2026-05-25T18:00:00+00:00",
        "repoUrl": "https://github.com/code-423n4/2026-05-some-protocol",
        "description": "A test contest",
    }
    c = _candidate_from_sveltekit(entry, "2026-05-18T00:00:00+00:00")
    assert c is not None
    assert c.id == "c4-2026-05-some-protocol"
    assert c.platform == "c4"
    assert c.kind == "source-only"
    assert c.payout_max_usd == 100_000
    assert c.closes_at == "2026-05-25T18:00:00+00:00"
    assert c.repo_url == "https://github.com/code-423n4/2026-05-some-protocol"
    assert "test contest" in c.notes


def test_candidate_from_sveltekit_defaults_repo_url():
    entry = {"slug": "2026-05-foo", "title": "Foo"}
    c = _candidate_from_sveltekit(entry, "2026-05-18T00:00:00+00:00")
    assert c is not None
    assert c.repo_url == "https://github.com/code-423n4/2026-05-foo"


def test_candidate_from_sveltekit_requires_slug():
    entry = {"title": "No Slug"}
    assert _candidate_from_sveltekit(entry, "2026-05-18T00:00:00+00:00") is None


def test_candidate_from_github_uses_repo_name():
    entry = {
        "name": "2026-05-aave-v4",
        "html_url": "https://github.com/code-423n4/2026-05-aave-v4",
        "description": "Aave V4 audit",
    }
    c = _candidate_from_github(entry, "2026-05-18T00:00:00+00:00")
    assert c.id == "c4-2026-05-aave-v4"
    assert c.platform == "c4"
    assert c.repo_url == "https://github.com/code-423n4/2026-05-aave-v4"
    assert "Aave V4" in c.notes


def test_parse_scope_from_readme(tmp_path):
    readme = tmp_path / "README.md"
    readme.write_text("""\
# Some Audit

## Scope

| File | nSLOC |
| --- | --- |
| `src/Vault.sol` | 100 |
| `src/Router.sol` | 50 |

These are in scope.

## Out of scope

* `src/Mock.sol`

## Setup

run forge install
""")
    paths = _parse_scope_from_readme(tmp_path)
    assert "src/Vault.sol" in paths
    assert "src/Router.sol" in paths
    # Headings differ; "out of scope" doesn't match SCOPE_HEADERS so the
    # parser captures the first scope section only.


def test_parse_scope_returns_empty_on_no_readme(tmp_path):
    assert _parse_scope_from_readme(tmp_path) == []
