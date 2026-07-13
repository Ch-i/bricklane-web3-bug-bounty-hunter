#!/usr/bin/env python3
"""Autonomous autoresearch loop.

Runs continuously, synthesizing one topic at a time from the queue,
sleeping between runs. Each completed synthesis immediately appears
in the web UI Library tab.

All output is tee'd to a persistent log file so the UI can stream it.

Usage:
    uv run python scripts/autoresearch_loop.py [--interval 300] [--max-topics 20]
"""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from harness.autoresearch import get_topics_with_status, run_batch, DOMAINS

LOG_PATH = REPO_ROOT / "autoresearch-log.jsonl"
STATE_FILE = REPO_ROOT / "autoresearch-live.json"


def log(msg: str, level: str = "info", **extra):
    """Write to stdout AND append to the JSONL log file."""
    ts = datetime.now().strftime('%H:%M:%S')
    line = f"[{ts}] {msg}"
    print(line, flush=True)

    entry = {
        "ts": datetime.now().isoformat(),
        "level": level,
        "msg": msg,
        **extra,
    }
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")


def update_live_state(state: dict):
    """Write current process state for the UI to poll."""
    state["updated_at"] = datetime.now().isoformat()
    STATE_FILE.write_text(json.dumps(state, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--interval", type=int, default=60,
                        help="Seconds to wait between synthesis runs (default: 60)")
    parser.add_argument("--max-topics", type=int, default=20,
                        help="Stop after synthesizing this many topics (default: 20)")
    args = parser.parse_args()

    log("Starting autonomous autoresearch loop", level="start",
        interval=args.interval, max_topics=args.max_topics)

    update_live_state({
        "status": "running",
        "current_topic": None,
        "completed_this_session": 0,
        "max_topics": args.max_topics,
    })

    completed = 0

    while completed < args.max_topics:
        topics = get_topics_with_status()
        pending = [t for t in topics if t["status"] == "pending"]
        done = [t for t in topics if t["status"] == "done"]

        log(f"Progress: {len(done)}/{len(topics)} synthesized, {len(pending)} pending",
            level="progress", done=len(done), total=len(topics), pending=len(pending))

        if not pending:
            log("All topics synthesized! Queue complete.", level="complete")
            update_live_state({"status": "complete", "current_topic": None,
                             "completed_this_session": completed, "max_topics": args.max_topics})
            break

        next_topic = pending[0]
        log(f"▶ Synthesizing: {next_topic['title']}", level="synth_start",
            slug=next_topic["slug"], domain=next_topic["domain"],
            seed_query=next_topic["seed_query"])

        update_live_state({
            "status": "synthesizing",
            "current_topic": {
                "slug": next_topic["slug"],
                "title": next_topic["title"],
                "domain": next_topic["domain"],
                "seed_query": next_topic["seed_query"],
            },
            "completed_this_session": completed,
            "max_topics": args.max_topics,
        })

        try:
            results = run_batch(n=1)
            for r in results:
                if r["status"] == "done":
                    completed += 1
                    log(f"✓ Synthesized: {next_topic['title']} ({completed}/{args.max_topics})",
                        level="synth_done", slug=r["slug"])
                else:
                    log(f"✗ Failed: {next_topic['title']} — {r.get('error', 'unknown')}",
                        level="synth_fail", slug=r["slug"], error=r.get("error"))
        except Exception as e:
            log(f"✗ Exception on {next_topic['title']}: {e}",
                level="synth_error", slug=next_topic["slug"], error=str(e))

        if completed < args.max_topics and pending:
            log(f"Waiting {args.interval}s before next topic...", level="wait")
            update_live_state({
                "status": "waiting",
                "current_topic": None,
                "completed_this_session": completed,
                "max_topics": args.max_topics,
                "next_in_seconds": args.interval,
            })
            time.sleep(args.interval)

    log(f"Session complete. Synthesized {completed} topics.", level="session_done",
        completed=completed)
    update_live_state({"status": "idle", "current_topic": None,
                     "completed_this_session": completed, "max_topics": args.max_topics})


if __name__ == "__main__":
    main()
