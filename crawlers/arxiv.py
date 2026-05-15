"""Ingest smart-contract-relevant arXiv papers via the official Atom API.

The arXiv API is rate-limited (default: 3 sec between requests, no auth).
We use ``feedparser`` to parse the Atom feed, paginate with ``start=`` /
``max_results=``, and dedup against the existing corpus by source_url.

Usage:
    python -m crawlers.arxiv                  # default keyword set
    python -m crawlers.arxiv --query "..."    # custom query
    python -m crawlers.arxiv --limit 100      # cap number of new entries
"""

from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode

import feedparser
import httpx

from crawlers.common import slugify, write_corpus_entry
from harness.corpus import REPO_ROOT, corpus_dir, reindex
from harness.schema import CorpusEntryFrontmatter

ARXIV_API = "https://export.arxiv.org/api/query"

# Categories + keyword union targeting the web3 / smart-contract literature.
DEFAULT_QUERY = (
    "(cat:cs.CR OR cat:cs.PL OR cat:cs.SE) AND "
    "(abs:smart-contract OR abs:solidity OR abs:ethereum OR abs:EVM OR "
    "abs:DeFi OR abs:blockchain-security OR abs:reentrancy OR abs:fuzzing)"
)


def _entry_id(arxiv_id: str) -> str:
    # arxiv:abs/2203.00364v1 -> 2203.00364
    bare = arxiv_id.rsplit("/", 1)[-1].split("v")[0]
    return f"arxiv-{bare}"


def _to_datetime(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def fetch_page(query: str, start: int, max_results: int) -> list[dict]:
    """Fetch one page from arXiv's Atom API and return entries as dicts."""
    params = urlencode(
        {
            "search_query": query,
            "start": start,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
    )
    url = f"{ARXIV_API}?{params}"
    resp = httpx.get(url, timeout=30.0, follow_redirects=True)
    resp.raise_for_status()
    feed = feedparser.parse(resp.text)
    return list(feed.entries)


def ingest_entry(
    entry: dict,
    *,
    out_root: Path,
    ingested_at: datetime,
) -> bool:
    """Write one corpus entry. Returns True if written, False if skipped/duplicate."""
    arxiv_id = entry.get("id") or ""
    if not arxiv_id:
        return False
    bare = arxiv_id.rsplit("/", 1)[-1].split("v")[0]
    fm = CorpusEntryFrontmatter(
        id=_entry_id(arxiv_id),
        source="arxiv",
        source_url=entry.get("link") or f"https://arxiv.org/abs/{bare}",
        title=(entry.get("title") or "").replace("\n", " ").strip()[:240],
        ingested_at=ingested_at,
        published_at=_to_datetime(entry.get("published")),
        tags=["arxiv"]
        + [
            f"category:{t['term']}"
            for t in (entry.get("tags") or [])
            if isinstance(t, dict) and t.get("term")
        ],
    )

    authors = ", ".join(
        a.get("name", "") for a in (entry.get("authors") or []) if isinstance(a, dict)
    ) or entry.get("author", "")
    summary = (entry.get("summary") or "").strip()
    comment = entry.get("arxiv_comment") or ""

    body = (
        f"# {fm.title}\n\n"
        f"_arXiv ID: {bare}_  \n"
        f"_Authors: {authors}_  \n"
    )
    if fm.published_at:
        body += f"_Published: {fm.published_at.date().isoformat()}_  \n"
    if comment:
        body += f"_Note: {comment}_  \n"
    body += f"_Source: [{fm.source_url}]({fm.source_url})_\n\n"
    body += "---\n\n## Abstract\n\n" + summary + "\n"

    out_path = out_root / "arxiv" / f"{bare}.md"
    if out_path.exists():
        return False  # Idempotent — don't overwrite (dedups across runs)
    write_corpus_entry(out_path, fm, body)
    return True


def crawl(
    query: str = DEFAULT_QUERY,
    *,
    limit: int = 500,
    page_size: int = 50,
    sleep_seconds: float = 3.5,
    out_root: Path | None = None,
    reindex_after: bool = True,
) -> dict:
    target_root = out_root or corpus_dir()
    ingested_at = datetime.now(timezone.utc).replace(microsecond=0)

    stats = {"fetched": 0, "written": 0, "duplicates": 0, "pages": 0}
    start = 0
    while stats["written"] + stats["duplicates"] < limit:
        page = fetch_page(query, start, min(page_size, limit - stats["written"] - stats["duplicates"]))
        stats["pages"] += 1
        stats["fetched"] += len(page)
        if not page:
            break
        for e in page:
            if ingest_entry(e, out_root=target_root, ingested_at=ingested_at):
                stats["written"] += 1
            else:
                stats["duplicates"] += 1
        start += len(page)
        if len(page) < page_size:
            break  # exhausted
        time.sleep(sleep_seconds)  # respect arXiv's rate limit

    if reindex_after and stats["written"]:
        print(f"\nreindexing sqlite ({stats['written']} new entries)…")
        result = reindex()
        stats["reindex"] = {
            "inserted": result.inserted,
            "updated": result.updated,
            "errors": len(result.errors),
        }
    return stats


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", default=DEFAULT_QUERY)
    parser.add_argument("--limit", type=int, default=500, help="Max new entries to ingest.")
    parser.add_argument("--page-size", type=int, default=50)
    parser.add_argument("--sleep", type=float, default=3.5, help="Seconds between API calls.")
    parser.add_argument("--no-reindex", action="store_true")
    args = parser.parse_args(argv)

    stats = crawl(
        args.query,
        limit=args.limit,
        page_size=args.page_size,
        sleep_seconds=args.sleep,
        reindex_after=not args.no_reindex,
    )

    print(f"\n=== arXiv crawl summary ===")
    print(f"pages fetched: {stats['pages']}")
    print(f"entries fetched: {stats['fetched']}")
    print(f"new entries written: {stats['written']}")
    print(f"duplicates skipped: {stats['duplicates']}")
    if "reindex" in stats:
        r = stats["reindex"]
        print(f"reindex: inserted={r['inserted']} updated={r['updated']} errors={r['errors']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
