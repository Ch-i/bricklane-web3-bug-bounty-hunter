"""Unit tests for crawlers.arxiv.ingest_entry (no network)."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import frontmatter

from crawlers.arxiv import ingest_entry


def _fake_entry() -> dict:
    return {
        "id": "http://arxiv.org/abs/2401.12345v2",
        "link": "https://arxiv.org/abs/2401.12345v2",
        "title": "A Survey of Smart Contract Vulnerabilities",
        "published": "2024-01-15T08:00:00Z",
        "summary": "We survey known smart contract vulnerabilities including reentrancy, "
                   "integer overflow, and access control issues.",
        "authors": [{"name": "Alice Smith"}, {"name": "Bob Jones"}],
        "arxiv_comment": "Accepted to CCS 2024",
        "tags": [{"term": "cs.CR"}, {"term": "cs.PL"}],
    }


def test_arxiv_entry_written(tmp_path):
    written = ingest_entry(
        _fake_entry(),
        out_root=tmp_path,
        ingested_at=datetime.now(timezone.utc),
    )
    assert written
    out = tmp_path / "arxiv" / "2401.12345.md"
    assert out.exists()

    post = frontmatter.load(out)
    assert post.metadata["id"] == "arxiv-2401.12345"
    assert post.metadata["source"] == "arxiv"
    assert post.metadata["title"].startswith("A Survey")
    assert "arxiv" in post.metadata["tags"]
    assert "category:cs.CR" in post.metadata["tags"]
    assert "category:cs.PL" in post.metadata["tags"]
    assert "Alice Smith" in post.content
    assert "Accepted to CCS 2024" in post.content


def test_arxiv_entry_is_idempotent(tmp_path):
    entry = _fake_entry()
    ingested_at = datetime.now(timezone.utc)
    assert ingest_entry(entry, out_root=tmp_path, ingested_at=ingested_at) is True
    # Second call: file exists, should not overwrite or count as new.
    assert ingest_entry(entry, out_root=tmp_path, ingested_at=ingested_at) is False
