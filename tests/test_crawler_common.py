"""Tests for crawlers/common.py — slug, git clone, and corpus entry writer."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml

from crawlers.common import git_clone_or_pull, slugify, write_corpus_entry
from harness.schema import CorpusEntryFrontmatter


def test_slugify_basic():
    assert slugify("Reentrancy in withdraw()") == "reentrancy-in-withdraw"


def test_slugify_collapses_separators():
    assert slugify("A  --   B___C") == "a-b-c"


def test_slugify_strips_trailing_separators():
    assert slugify("---a---b---") == "a-b"


def test_slugify_unicode_falls_back_to_dashes():
    """Non-ASCII chars become dash separators."""
    assert slugify("héllo wörld") == "h-llo-w-rld"


def test_slugify_only_punctuation_returns_empty():
    """A string of pure punctuation becomes empty after strip — caller's job
    to handle (corpus IDs would then fail Pydantic validation)."""
    assert slugify("!!!") == ""


def test_git_clone_or_pull_fresh_clone(tmp_path):
    """If target doesn't exist, calls `git clone --depth 1 <url> <target>`."""
    target = tmp_path / "repo"
    captured_cmds = []

    def fake_run(cmd, **kw):
        captured_cmds.append(cmd)
        proc = MagicMock()
        proc.returncode = 0
        return proc

    with patch("crawlers.common.subprocess.run", side_effect=fake_run):
        result = git_clone_or_pull("https://github.com/x/y", target)
    assert result == target
    # Should have called git clone with --depth 1
    assert any(c[:2] == ["git", "clone"] and "--depth" in c for c in captured_cmds)


def test_git_clone_or_pull_existing_target_does_fetch_reset(tmp_path):
    """If target exists, calls fetch + reset --hard FETCH_HEAD."""
    target = tmp_path / "repo"
    target.mkdir()  # exists
    captured_cmds = []

    def fake_run(cmd, **kw):
        captured_cmds.append(cmd)
        proc = MagicMock()
        proc.returncode = 0
        return proc

    with patch("crawlers.common.subprocess.run", side_effect=fake_run):
        git_clone_or_pull("https://github.com/x/y", target)
    # Two calls: fetch then reset --hard FETCH_HEAD
    assert len(captured_cmds) == 2
    assert "fetch" in captured_cmds[0]
    assert "reset" in captured_cmds[1] and "FETCH_HEAD" in captured_cmds[1]


def test_git_clone_or_pull_custom_depth(tmp_path):
    target = tmp_path / "repo"
    captured_cmds = []

    def fake_run(cmd, **kw):
        captured_cmds.append(cmd)
        proc = MagicMock()
        proc.returncode = 0
        return proc

    with patch("crawlers.common.subprocess.run", side_effect=fake_run):
        git_clone_or_pull("https://github.com/x/y", target, depth=50)
    # The clone call should use --depth 50
    clone_call = [c for c in captured_cmds if c[1] == "clone"][0]
    assert "--depth" in clone_call
    depth_idx = clone_call.index("--depth")
    assert clone_call[depth_idx + 1] == "50"


def test_write_corpus_entry_emits_yaml_frontmatter_and_body(tmp_path):
    fm = CorpusEntryFrontmatter(
        id="swc-test-entry",
        source="swc",
        source_url=None,
        title="Test entry",
        ingested_at="2026-05-18T00:00:00Z",
        vuln_class=["reentrancy"],
    )
    out_path = tmp_path / "x.md"
    write_corpus_entry(out_path, fm, "# Body content\n\nA paragraph.")

    text = out_path.read_text()
    # YAML frontmatter delimiters
    assert text.startswith("---\n")
    assert "---\n\n" in text  # delimiter between frontmatter and body
    # Parse the frontmatter and verify fields
    parts = text.split("---\n", 2)
    fm_yaml = yaml.safe_load(parts[1])
    assert fm_yaml["id"] == "swc-test-entry"
    assert fm_yaml["source"] == "swc"
    assert "reentrancy" in fm_yaml["vuln_class"]
    # Body preserved
    assert "Body content" in text
    assert "A paragraph." in text


def test_write_corpus_entry_creates_parent_dirs(tmp_path):
    """Nested directories should be created on demand."""
    fm = CorpusEntryFrontmatter(
        id="swc-x", source="swc", title="x",
        ingested_at="2026-05-18T00:00:00Z",
    )
    nested = tmp_path / "a" / "b" / "c" / "entry.md"
    write_corpus_entry(nested, fm, "body")
    assert nested.exists()


def test_write_corpus_entry_excludes_none_fields(tmp_path):
    """source_url=None should not appear as a key in the YAML."""
    fm = CorpusEntryFrontmatter(
        id="swc-x", source="swc", title="x",
        ingested_at="2026-05-18T00:00:00Z",
        source_url=None,
    )
    out_path = tmp_path / "x.md"
    write_corpus_entry(out_path, fm, "body")
    text = out_path.read_text()
    assert "source_url" not in text
