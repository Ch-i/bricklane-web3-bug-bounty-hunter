"""CLI wrapper around harness.corpus — same surface as the MCP tools.

Useful for: (a) shell-driven corpus access from the auditor subagent when
MCP isn't loaded in the current Claude Code session, (b) ad-hoc debugging
from notebooks or terminal.

    python -m scripts.corpus_query search "reentrancy CEI" --top-k 5
    python -m scripts.corpus_query read swc-107
    python -m scripts.corpus_query stats
    python -m scripts.corpus_query list-synthesis [--category amm]
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from harness import corpus


def _env_exclude_ids() -> list[str]:
    """IDs to filter out of every search, set by the eval driver.

    Comma-separated. Empty/unset => no filtering. This is the mechanism that
    prevents the auditor from cheating on eval entries by reading the
    post-mortem of the bug it's supposed to find.
    """
    raw = os.environ.get("W3S_CORPUS_EXCLUDE_IDS", "").strip()
    return [s.strip() for s in raw.split(",") if s.strip()] if raw else []


def cmd_search(args: argparse.Namespace) -> int:
    # Merge --exclude-id flags with env-driven exclusions (eval mode).
    exclude_ids = list(args.exclude_id or []) + _env_exclude_ids()
    hits = corpus.search(
        query=args.query,
        vuln_class=args.vuln_class,
        severity=args.severity,
        source=args.source,
        exclude_ids=exclude_ids or None,
        top_k=args.top_k,
    )
    print(
        json.dumps(
            [
                {
                    "id": h.id,
                    "title": h.title,
                    "source": h.source,
                    "severity": h.severity,
                    "snippet": h.snippet,
                    "score": h.score,
                }
                for h in hits
            ],
            indent=2,
        )
    )
    return 0


def cmd_read(args: argparse.Namespace) -> int:
    entry = corpus.get_entry(args.entry_id)
    if entry is None:
        print(json.dumps({"error": f"no such entry: {args.entry_id}"}))
        return 1
    print(json.dumps(entry, indent=2, default=str))
    return 0


def cmd_stats(_args: argparse.Namespace) -> int:
    print(json.dumps(corpus.stats(), indent=2))
    return 0


def cmd_list_synthesis(args: argparse.Namespace) -> int:
    print(json.dumps(corpus.list_synthesis_notes(category=args.category), indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_search = sub.add_parser("search", help="Full-text search across corpus")
    p_search.add_argument("query")
    p_search.add_argument("--vuln-class", action="append", default=None)
    p_search.add_argument("--severity", action="append", default=None)
    p_search.add_argument("--source", action="append", default=None)
    p_search.add_argument("--exclude-id", action="append", default=None)
    p_search.add_argument("--top-k", type=int, default=10)
    p_search.set_defaults(func=cmd_search)

    p_read = sub.add_parser("read", help="Fetch a single corpus entry by ID")
    p_read.add_argument("entry_id")
    p_read.set_defaults(func=cmd_read)

    p_stats = sub.add_parser("stats", help="Corpus counts by source/severity/class")
    p_stats.set_defaults(func=cmd_stats)

    p_synth = sub.add_parser("list-synthesis", help="List synthesis notes")
    p_synth.add_argument("--category", default=None)
    p_synth.set_defaults(func=cmd_list_synthesis)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
