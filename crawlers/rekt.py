"""Ingest rekt.news exploit post-mortems.

rekt.news is a Next.js SPA — RSS endpoints return 500, but every page
embeds a ``__NEXT_DATA__`` JSON blob with the full article markdown.
We pull the leaderboard once for the slug list, then fetch each
``/{slug}/`` page and extract its embedded markdown content.

Usage:
    python -m crawlers.rekt              # ingest all (~295 entries)
    python -m crawlers.rekt --limit 25   # cap for dev runs
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx

from crawlers.common import slugify, write_corpus_entry
from harness.corpus import REPO_ROOT, corpus_dir, reindex
from harness.schema import CorpusEntryFrontmatter

REKT_BASE = "https://rekt.news"
USER_AGENT = "web3sentinel-research/0.1 (https://github.com/web3sentinel)"
NEXT_DATA_RE = re.compile(
    r'<script id="__NEXT_DATA__"[^>]*>(.+?)</script>', re.DOTALL
)


def _client() -> httpx.Client:
    return httpx.Client(
        headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"},
        timeout=30.0,
        follow_redirects=True,
    )


def _parse_next_data(html: str) -> dict:
    m = NEXT_DATA_RE.search(html)
    if not m:
        raise ValueError("no __NEXT_DATA__ found")
    return json.loads(m.group(1))


def fetch_leaderboard(client: httpx.Client) -> list[dict]:
    resp = client.get(f"{REKT_BASE}/leaderboard/")
    resp.raise_for_status()
    data = _parse_next_data(resp.text)
    return data["props"]["pageProps"].get("leaderboard") or []


def fetch_article(client: httpx.Client, slug: str) -> dict | None:
    """Return {data: {...meta...}, content: "markdown"} or None on failure."""
    resp = client.get(f"{REKT_BASE}/{slug}/")
    if resp.status_code != 200:
        return None
    try:
        nd = _parse_next_data(resp.text)
    except (ValueError, json.JSONDecodeError):
        return None
    pp = nd.get("props", {}).get("pageProps", {})
    if "data" not in pp or "content" not in pp:
        return None
    return {"data": pp["data"], "content": pp["content"]}


def _to_iso(date_str: str | None) -> str | None:
    if not date_str:
        return None
    for fmt in ("%m/%d/%Y", "%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(date_str, fmt).replace(tzinfo=timezone.utc).isoformat()
        except ValueError:
            continue
    return None


def ingest_article(
    slug: str,
    article: dict,
    leaderboard_meta: dict,
    *,
    out_root: Path,
    ingested_at: datetime,
) -> bool:
    """Write one corpus entry. Returns True iff actually written."""
    data = article["data"]
    content = (article["content"] or "").strip()
    if not content:
        return False

    entry_id = f"rekt-{slugify(slug)}"
    title = data.get("title") or slug
    published_iso = _to_iso(data.get("date"))
    published_dt = (
        datetime.fromisoformat(published_iso) if published_iso else None
    )

    tags = ["rekt", "exploit", "post-mortem"]
    for t in (data.get("tags") or []):
        if isinstance(t, str):
            tags.append(f"protocol:{slugify(t)}")
    rekt_meta = data.get("rekt") or leaderboard_meta.get("rekt") or {}
    if isinstance(rekt_meta.get("amount"), (int, float)):
        amount = int(rekt_meta["amount"])
        tags.append(f"loss-bucket:{_loss_bucket(amount)}")

    fm = CorpusEntryFrontmatter(
        id=entry_id,
        source="rekt",
        source_url=f"{REKT_BASE}/{slug}/",
        title=str(title)[:240],
        ingested_at=ingested_at,
        published_at=published_dt,
        severity="Critical",  # rekt.news only writes about successful exploits
        tags=tags,
    )

    body_parts = [f"# {title}"]
    if isinstance(rekt_meta, dict):
        amt = rekt_meta.get("amount")
        audit = rekt_meta.get("audit") or "—"
        incident_date = rekt_meta.get("date") or "—"
        if amt is not None:
            body_parts.append(f"\n_Loss: ${amt:,}_  ")
        body_parts.append(f"_Incident date: {incident_date}_  ")
        body_parts.append(f"_Pre-exploit audit: {audit}_  ")
    if data.get("excerpt"):
        body_parts.append(f"\n> {data['excerpt']}\n")
    body_parts.append(f"\n_Source: [{REKT_BASE}/{slug}/]({REKT_BASE}/{slug}/)_\n")
    body_parts.append("\n---\n")
    body_parts.append(content)

    out_path = out_root / "rekt" / f"{slugify(slug)}.md"
    if out_path.exists():
        return False
    write_corpus_entry(out_path, fm, "\n".join(body_parts))
    return True


def _loss_bucket(amount: int) -> str:
    if amount >= 1_000_000_000:
        return "billion-plus"
    if amount >= 100_000_000:
        return "100M-plus"
    if amount >= 10_000_000:
        return "10M-plus"
    if amount >= 1_000_000:
        return "1M-plus"
    return "under-1M"


def crawl(
    *,
    limit: int | None = None,
    sleep_seconds: float = 0.6,
    out_root: Path | None = None,
    reindex_after: bool = True,
) -> dict:
    target_root = out_root or corpus_dir()
    ingested_at = datetime.now(timezone.utc).replace(microsecond=0)
    stats = {"leaderboard_size": 0, "fetched": 0, "written": 0, "skipped": 0, "errors": 0}

    with _client() as client:
        items = fetch_leaderboard(client)
        stats["leaderboard_size"] = len(items)

        for i, item in enumerate(items):
            if limit is not None and stats["fetched"] >= limit:
                break
            slug = item.get("slug")
            if not slug:
                continue
            try:
                article = fetch_article(client, slug)
            except Exception as e:  # noqa: BLE001
                stats["errors"] += 1
                print(f"error fetching {slug}: {e}", file=sys.stderr)
                continue
            stats["fetched"] += 1
            if article is None:
                stats["skipped"] += 1
                continue
            try:
                if ingest_article(
                    slug,
                    article,
                    leaderboard_meta=item,
                    out_root=target_root,
                    ingested_at=ingested_at,
                ):
                    stats["written"] += 1
                else:
                    stats["skipped"] += 1
            except Exception as e:  # noqa: BLE001
                stats["errors"] += 1
                print(f"error ingesting {slug}: {e}", file=sys.stderr)
            time.sleep(sleep_seconds)

    if reindex_after and stats["written"]:
        print(f"\nreindexing sqlite…")
        result = reindex()
        stats["reindex"] = {
            "inserted": result.inserted,
            "updated": result.updated,
            "errors": len(result.errors),
        }

    return stats


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--sleep", type=float, default=0.6)
    parser.add_argument("--no-reindex", action="store_true")
    args = parser.parse_args(argv)

    stats = crawl(
        limit=args.limit,
        sleep_seconds=args.sleep,
        reindex_after=not args.no_reindex,
    )

    print(f"\n=== rekt crawl summary ===")
    print(f"leaderboard size: {stats['leaderboard_size']}")
    print(f"fetched: {stats['fetched']}")
    print(f"written: {stats['written']}")
    print(f"skipped: {stats['skipped']}")
    print(f"errors: {stats['errors']}")
    if "reindex" in stats:
        r = stats["reindex"]
        print(f"reindex: inserted={r['inserted']} updated={r['updated']} errors={r['errors']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
