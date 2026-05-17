"""Tests for the --from-candidate resolver in harness/tui.py.

The resolver bridges the bounty-hunt sweep output and the audit/deep-dive
pipeline so the user can run `w3s scrutinize --from-candidate <id>` instead
of manually copying the local_path.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from unittest.mock import patch

import pytest

from harness import tui
from harness.candidates import Candidate


def _make_candidate(local_path: str | None = None, scope_paths: list | None = None) -> Candidate:
    return Candidate(
        id="c4-2026-05-aave-v4",
        platform="code4rena",
        kind="source",
        title="Aave V4",
        sourced_at="2026-05-15T00:00:00+00:00",
        local_path=local_path,
        scope_paths=scope_paths or [],
    )


def test_resolve_candidate_target_returns_path_and_scope():
    cand = _make_candidate(local_path="/tmp/repos/aave-v4", scope_paths=["src/core"])
    with patch("harness.candidates.get", return_value=cand):
        target, scope = tui._resolve_candidate_target("c4-2026-05-aave-v4")
    assert target == "/tmp/repos/aave-v4"
    assert scope == "src/core"


def test_resolve_candidate_target_returns_no_scope_when_unset():
    cand = _make_candidate(local_path="/tmp/repos/x")
    with patch("harness.candidates.get", return_value=cand):
        target, scope = tui._resolve_candidate_target("c4-2026-05-aave-v4")
    assert target == "/tmp/repos/x"
    assert scope is None


def test_resolve_candidate_target_missing_raises():
    with patch("harness.candidates.get", return_value=None):
        with pytest.raises(SystemExit, match="not found in queue"):
            tui._resolve_candidate_target("nonexistent-id")


def test_resolve_candidate_target_no_local_path_raises():
    cand = _make_candidate(local_path=None)
    with patch("harness.candidates.get", return_value=cand):
        with pytest.raises(SystemExit, match="no local_path"):
            tui._resolve_candidate_target("c4-2026-05-aave-v4")


def test_resolve_target_args_uses_from_candidate():
    """_resolve_target_args is used by cmd_deep_dive — make sure it routes through resolver."""
    args = argparse.Namespace(target=None, scope=None, from_candidate="c4-foo")
    cand = _make_candidate(local_path="/repos/foo", scope_paths=["contracts/"])
    with patch("harness.candidates.get", return_value=cand):
        target, scope = tui._resolve_target_args(args)
    assert target == "/repos/foo"
    assert scope == "contracts/"


def test_resolve_target_args_explicit_scope_overrides_candidate_scope():
    """If user passes both --scope and --from-candidate, --scope wins."""
    args = argparse.Namespace(target=None, scope="custom/path", from_candidate="c4-foo")
    cand = _make_candidate(local_path="/repos/foo", scope_paths=["contracts/"])
    with patch("harness.candidates.get", return_value=cand):
        target, scope = tui._resolve_target_args(args)
    assert target == "/repos/foo"
    assert scope == "custom/path"  # user override


def test_resolve_target_args_without_from_candidate_passes_through():
    """Plain positional target should pass through unchanged."""
    args = argparse.Namespace(target="/some/path", scope="my/scope", from_candidate=None)
    target, scope = tui._resolve_target_args(args)
    assert target == "/some/path"
    assert scope == "my/scope"
