"""Sanity checks for synthesis notes already on disk.

No LLM calls — this just asserts that the synthesizer's output format
parses cleanly against the corpus loader and lands as a queryable entry.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from harness import corpus

REPO_ROOT = Path(__file__).resolve().parent.parent
SYNTHESIS_DIR = REPO_ROOT / "corpus" / "synthesis"


def _synthesis_files() -> list[Path]:
    if not SYNTHESIS_DIR.exists():
        return []
    return sorted(SYNTHESIS_DIR.glob("*.md"))


@pytest.mark.skipif(not _synthesis_files(), reason="no synthesis notes on disk yet")
def test_every_synthesis_note_parses_and_grounds():
    for path in _synthesis_files():
        fm, body = corpus.parse_entry(path)
        assert fm.source == "synthesis", f"{path}: source must be 'synthesis'"
        assert fm.id.startswith("synthesis-"), f"{path}: id must start with 'synthesis-'"
        assert fm.title, f"{path}: empty title"
        # Hard rule from the synthesizer system prompt: >=5 derives_from entries.
        assert len(fm.derives_from) >= 5, (
            f"{path}: only {len(fm.derives_from)} derives_from entries — "
            f"synthesizer requires >=5"
        )
        # Body must include the "Pattern" and "Audit checklist" sections.
        assert "## Pattern" in body, f"{path}: missing ## Pattern section"
        assert "Audit checklist" in body, f"{path}: missing audit checklist"


@pytest.mark.skipif(not _synthesis_files(), reason="no synthesis notes on disk yet")
def test_synthesis_derives_from_ids_exist_in_corpus():
    """No invented citations — every derives_from ID must be a real entry."""
    for path in _synthesis_files():
        fm, _ = corpus.parse_entry(path)
        missing: list[str] = []
        for cid in fm.derives_from:
            if corpus.get_entry(cid) is None:
                missing.append(cid)
        assert not missing, (
            f"{path}: derives_from points to nonexistent corpus entries: {missing[:5]}"
        )
