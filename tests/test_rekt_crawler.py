"""Unit tests for crawlers.rekt.ingest_article (no network)."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import frontmatter

from crawlers.rekt import ingest_article


def _fake_article() -> dict:
    return {
        "data": {
            "title": "Example Protocol — REKT",
            "date": "03/29/2022",
            "excerpt": "Example exploit summary.",
            "rekt": {"amount": 624_000_000, "audit": "Unaudited", "date": "03/23/2022"},
            "tags": ["Example", "Bridge"],
        },
        "content": (
            "**[Example Protocol](https://example.com) has been hit.**\n\n"
            "The attacker exploited a signature verification flaw..."
        ),
    }


def test_rekt_entry_written_with_loss_bucket(tmp_path):
    written = ingest_article(
        slug="example-rekt",
        article=_fake_article(),
        leaderboard_meta={},
        out_root=tmp_path,
        ingested_at=datetime.now(timezone.utc),
    )
    assert written
    out = tmp_path / "rekt" / "example-rekt.md"
    assert out.exists()

    post = frontmatter.load(out)
    assert post.metadata["id"] == "rekt-example-rekt"
    assert post.metadata["severity"] == "Critical"
    assert "rekt" in post.metadata["tags"]
    # $624M -> 100M-plus bucket
    assert "loss-bucket:100M-plus" in post.metadata["tags"]
    assert "protocol:example" in post.metadata["tags"]
    assert "signature verification" in post.content


def test_rekt_entry_idempotent(tmp_path):
    art = _fake_article()
    ingested_at = datetime.now(timezone.utc)
    assert ingest_article("example-rekt", art, {}, out_root=tmp_path, ingested_at=ingested_at) is True
    assert ingest_article("example-rekt", art, {}, out_root=tmp_path, ingested_at=ingested_at) is False


def test_rekt_skips_empty_content(tmp_path):
    art = {"data": {"title": "Empty", "date": "01/01/2020"}, "content": ""}
    assert ingest_article("empty", art, {}, out_root=tmp_path, ingested_at=datetime.now(timezone.utc)) is False
