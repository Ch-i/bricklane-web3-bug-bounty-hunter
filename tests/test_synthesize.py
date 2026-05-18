"""Tests for harness/synthesize.py — the synthesis subagent CLI wrapper.

Focuses on the input/output handling that doesn't require a real LLM
roundtrip: slug generation, confirmation parsing, error paths.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from harness import synthesize as syn


def test_slugify_basic():
    assert syn.slugify("Oracle staleness and price feed manipulation") == \
        "oracle-staleness-and-price-feed-manipulation"


def test_slugify_strips_punctuation():
    assert syn.slugify("ERC-4337 & EIP-7702 Account Abstraction!") == \
        "erc-4337-eip-7702-account-abstraction"


def test_slugify_empty_input_returns_topic():
    assert syn.slugify("") == "topic"
    assert syn.slugify("---") == "topic"


def test_slugify_collapses_repeated_separators():
    assert syn.slugify("a    b___c--d") == "a-b-c-d"


def test_confirmation_regex_extracts_derives_count():
    msg = "SYNTHESIS NOTE WRITTEN\nderives_from_count: 30\nnote_path: /x.md"
    m = syn.CONFIRMATION_RE.search(msg)
    assert m is not None
    assert m.group(1) == "30"


def test_confirmation_regex_handles_multiline_arrangement():
    msg = "Some preamble.\n\nSYNTHESIS NOTE WRITTEN\n  derives_from_count: 7\n"
    m = syn.CONFIRMATION_RE.search(msg)
    assert m is not None
    assert m.group(1) == "7"


def test_confirmation_regex_returns_none_on_missing():
    assert syn.CONFIRMATION_RE.search("nothing of note") is None


def test_synthesize_raises_without_claude_binary():
    with patch("harness.synthesize.shutil.which", return_value=None):
        with pytest.raises(FileNotFoundError, match="claude CLI"):
            syn.synthesize("topic")


def test_synthesize_passes_correct_cli_args(tmp_path, monkeypatch):
    """The subprocess.run call must include --agent web3-synthesizer,
    --output-format json, --dangerously-skip-permissions, and the brief."""
    monkeypatch.setattr(syn, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(syn, "corpus_dir", lambda: tmp_path / "corpus")
    (tmp_path / "corpus" / "synthesis").mkdir(parents=True)

    captured_cmd = []

    def fake_run(cmd, **kw):
        captured_cmd.extend(cmd)
        # The real subagent writes the note file. Mock that side-effect:
        note_path = tmp_path / "corpus" / "synthesis" / "test-slug.md"
        note_path.write_text("---\ntitle: test\n---\nbody")
        proc = MagicMock()
        proc.returncode = 0
        proc.stdout = json.dumps({"result": "SYNTHESIS NOTE WRITTEN\nderives_from_count: 10"})
        proc.stderr = ""
        return proc

    with patch("harness.synthesize.shutil.which", return_value="/fake/claude"):
        with patch("harness.synthesize.subprocess.run", side_effect=fake_run):
            # Skip reindex to avoid hitting the real corpus DB
            result = syn.synthesize("test topic", slug="test-slug", reindex_after=False)

    assert "--agent" in captured_cmd
    assert "web3-synthesizer" in captured_cmd
    assert "--output-format" in captured_cmd
    assert "json" in captured_cmd
    assert "--dangerously-skip-permissions" in captured_cmd
    # The brief should reference the slug
    brief_arg = [a for a in captured_cmd if "test topic" in a]
    assert brief_arg, f"brief not in args: {captured_cmd}"
    assert result.derives_count == 10
    assert result.error is None


def test_synthesize_records_logs_under_audits_dir(tmp_path, monkeypatch):
    """Both stdout and stderr should be persisted to audits/synthesize-<slug>/."""
    monkeypatch.setattr(syn, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(syn, "corpus_dir", lambda: tmp_path / "corpus")
    (tmp_path / "corpus" / "synthesis").mkdir(parents=True)

    def fake_run(cmd, **kw):
        proc = MagicMock()
        proc.returncode = 0
        proc.stdout = json.dumps({"result": "ok"})
        proc.stderr = "some stderr noise"
        return proc

    with patch("harness.synthesize.shutil.which", return_value="/fake/claude"):
        with patch("harness.synthesize.subprocess.run", side_effect=fake_run):
            syn.synthesize("test", slug="test-x", reindex_after=False)

    log_dir = tmp_path / "audits" / "synthesize-test-x"
    assert (log_dir / "claude-stdout.log").exists()
    assert (log_dir / "claude-stderr.log").exists()
    assert "some stderr noise" in (log_dir / "claude-stderr.log").read_text()


def test_synthesize_extracts_derives_count_from_unwrapped_stdout(tmp_path, monkeypatch):
    """If claude's stdout isn't JSON-wrapped (older format), still parse it."""
    monkeypatch.setattr(syn, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(syn, "corpus_dir", lambda: tmp_path / "corpus")
    (tmp_path / "corpus" / "synthesis").mkdir(parents=True)

    def fake_run(cmd, **kw):
        # Mock side-effect: write the note
        (tmp_path / "corpus" / "synthesis" / "t.md").write_text("body")
        proc = MagicMock()
        proc.returncode = 0
        # Raw stdout, not JSON-wrapped
        proc.stdout = "SYNTHESIS NOTE WRITTEN\nderives_from_count: 42\nnote_path: /x"
        proc.stderr = ""
        return proc

    with patch("harness.synthesize.shutil.which", return_value="/fake/claude"):
        with patch("harness.synthesize.subprocess.run", side_effect=fake_run):
            result = syn.synthesize("test", slug="t", reindex_after=False)
    assert result.derives_count == 42
