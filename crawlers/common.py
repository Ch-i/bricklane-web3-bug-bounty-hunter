"""Shared utilities for source-specific crawlers."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import yaml

from harness.schema import CorpusEntryFrontmatter


def slugify(s: str) -> str:
    """ASCII slug suitable for corpus entry IDs and filenames.

    Pattern is loose — corpus IDs are validated by Pydantic against the
    contract in ``harness.schema.CorpusEntryFrontmatter``.
    """
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def git_clone_or_pull(repo_url: str, target: Path, depth: int | None = 1) -> Path:
    """Idempotent shallow clone. If target already exists, fast-forward pull."""
    target = Path(target)
    if target.exists():
        subprocess.run(
            ["git", "-C", str(target), "fetch", "--depth", str(depth or 1), "origin"],
            capture_output=True,
            check=False,
        )
        subprocess.run(
            ["git", "-C", str(target), "reset", "--hard", "FETCH_HEAD"],
            capture_output=True,
            check=False,
        )
    else:
        cmd = ["git", "clone"]
        if depth:
            cmd += ["--depth", str(depth)]
        cmd += [repo_url, str(target)]
        subprocess.run(cmd, check=True)
    return target


def write_corpus_entry(out_path: Path, fm: CorpusEntryFrontmatter, body: str) -> None:
    """Write a markdown file with YAML frontmatter."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    data = fm.model_dump(mode="json", exclude_none=True)
    yaml_block = yaml.safe_dump(data, sort_keys=True, allow_unicode=True)
    out_path.write_text(f"---\n{yaml_block}---\n\n{body.rstrip()}\n")
