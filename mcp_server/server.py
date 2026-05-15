"""web3sentinel-corpus MCP server.

Exposes the corpus index over the Model Context Protocol so Claude Code
subagents and the Codex CLI both consume the same retrieval surface.

Run directly:
    python -m mcp_server.server          # stdio transport (default for Claude Code)

Or as the installed entry point:
    uv run web3sentinel-mcp
"""

from __future__ import annotations

import json
import os
from typing import Any

from mcp.server.fastmcp import FastMCP

from harness import corpus as corpus_mod

mcp = FastMCP("web3sentinel-corpus")


def _env_exclude_ids() -> list[str]:
    """Eval-mode exclusions, set by the eval driver before launching the MCP
    server. Merged with the per-call ``exclude_ids`` argument."""
    raw = os.environ.get("W3S_CORPUS_EXCLUDE_IDS", "").strip()
    return [s.strip() for s in raw.split(",") if s.strip()] if raw else []


@mcp.tool()
def search_corpus(
    query: str,
    vuln_class: list[str] | None = None,
    severity: list[str] | None = None,
    source: list[str] | None = None,
    exclude_ids: list[str] | None = None,
    top_k: int = 10,
) -> list[dict[str, Any]]:
    """Full-text search across the corpus.

    Args:
        query: BM25 search query. Multiple words OR-ed together.
        vuln_class: Restrict to entries tagged with any of these vuln classes
            (e.g. ["reentrancy", "external-call"]).
        severity: Restrict to entries with these severities
            (Critical | High | Medium | Low | Informational | Gas).
        source: Restrict to these sources (swc | solodit | arxiv | audit-report | rekt | dasp | synthesis).
        exclude_ids: Entry IDs to filter out. Used by eval runs to prevent
            the audit agent from reading the post-mortem for the bug it's
            supposed to find.
        top_k: Maximum hits to return (default 10).

    Returns:
        List of {id, title, source, severity, snippet, score}.
        score is BM25; lower is more relevant in sqlite FTS5.
    """
    merged_excludes = list(exclude_ids or []) + _env_exclude_ids()
    hits = corpus_mod.search(
        query=query,
        vuln_class=vuln_class,
        severity=severity,
        source=source,
        exclude_ids=merged_excludes or None,
        top_k=top_k,
    )
    return [
        {
            "id": h.id,
            "title": h.title,
            "source": h.source,
            "severity": h.severity,
            "snippet": h.snippet,
            "score": h.score,
        }
        for h in hits
    ]


@mcp.tool()
def read_corpus_entry(entry_id: str) -> dict[str, Any] | None:
    """Fetch the full markdown body + frontmatter for a single corpus entry.

    Args:
        entry_id: Stable corpus ID, e.g. "swc-107", "solodit-12345".

    Returns:
        Dict with all frontmatter fields plus body, or None if the entry
        does not exist.
    """
    entry = corpus_mod.get_entry(entry_id)
    if entry is None:
        return None
    # sqlite Row -> plain dict was already done in get_entry, but ensure
    # the raw_frontmatter blob is parsed for caller convenience.
    return entry


@mcp.tool()
def list_synthesis_notes(category: str | None = None) -> list[dict[str, Any]]:
    """List synthesis notes (distilled multi-source summaries on a topic).

    Args:
        category: Optional protocol category filter (e.g. "amm", "bridge").

    Returns:
        List of {id, title, ingested_at, severity}. Most-recent first.
    """
    return corpus_mod.list_synthesis_notes(category=category)


@mcp.tool()
def corpus_stats() -> dict[str, Any]:
    """High-level counts of corpus contents.

    Useful at audit start to confirm the corpus has been ingested and to
    see which vuln classes are well-covered vs sparse.
    """
    return corpus_mod.stats()


def main() -> None:
    # Default stdio transport is what Claude Code and Codex CLI both expect.
    mcp.run()


if __name__ == "__main__":
    main()
