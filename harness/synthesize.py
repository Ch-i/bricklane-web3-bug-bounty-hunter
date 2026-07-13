"""Run the synthesizer subagent non-interactively via `claude -p`.

Used by:
  * the /research skill (interactive)
  * scheduled cron / GH Actions jobs that want to refresh a fixed set of
    synthesis topics (e.g. weekly).
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from harness.corpus import REPO_ROOT, corpus_dir, reindex


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") or "topic"


@dataclass
class SynthesizeResult:
    note_path: Path
    stdout_tail: str
    derives_count: int | None
    error: str | None


SYNTHESIZER_BRIEF = """\
TOPIC: {topic}
SLUG: {slug}
SEED QUERY: {seed_query}
OUTPUT PATH: {output_path}

SEVERITY FOCUS: You are a HIGH-TO-CRITICAL severity specialist. This means:

1. SEARCH STRATEGY — When querying the corpus, bias toward Critical and High
   severity findings. Run at least one search with severity="Critical" and one
   with severity="High" in addition to your general queries.
2. REQUIRED SECTIONS — Your synthesis note MUST include:
   • "## Severity Profile" — classify the overall risk as Critical, High, or
     context-dependent. Explain what determines the severity (fund loss,
     permanent state corruption, governance takeover, etc.).
   • "## Attack Scenarios" — at least 2 concrete attack flows with step-by-step
     descriptions of how an attacker exploits this pattern. Reference real
     incidents from the corpus where possible.
   • "## Invariants & Guards" — the mathematical or logical invariants that
     MUST hold. Express as require() conditions where possible.
   • "## Severity Escalation Paths" — how a Medium finding of this type
     becomes Critical (composability with other patterns, market conditions,
     governance states, etc.).
3. GROUNDING RULE — At least 50%% of your derives_from entries MUST come from
   Critical or High severity corpus findings. If insufficient high-severity
   entries exist, note this gap explicitly.
4. REAL-WORLD LOSSES — Where applicable, reference real protocol losses from
   rekt entries (amounts, dates, root causes).

Follow the workflow in your system prompt. Use the MCP corpus tools
(search_corpus, read_corpus_entry) to gather grounding entries. Write
the synthesis note to OUTPUT PATH via the Write tool. End your
response with the "SYNTHESIS NOTE WRITTEN" confirmation block.

Do not paste the note content into chat -- write it to the file.
"""


CONFIRMATION_RE = re.compile(
    r"SYNTHESIS\s+NOTE\s+WRITTEN.*?derives_from_count:\s*(\d+)",
    re.DOTALL | re.IGNORECASE,
)


def synthesize(
    topic: str,
    *,
    seed_query: str | None = None,
    slug: str | None = None,
    model: str = "opus",
    timeout_seconds: int = 1800,
    reindex_after: bool = True,
) -> SynthesizeResult:
    """Run the web3-synthesizer subagent headlessly."""
    claude_bin = shutil.which("claude")
    if not claude_bin:
        raise FileNotFoundError("claude CLI not on PATH")

    final_slug = slug or slugify(topic)
    final_query = seed_query or topic
    note_path = corpus_dir() / "synthesis" / f"{final_slug}.md"
    note_path.parent.mkdir(parents=True, exist_ok=True)

    brief = SYNTHESIZER_BRIEF.format(
        topic=topic,
        slug=final_slug,
        seed_query=final_query,
        output_path=str(note_path),
    )

    cmd = [
        claude_bin,
        "-p",
        "--agent",
        "web3-synthesizer",
        "--model",
        model,
        "--add-dir",
        str(REPO_ROOT.resolve()),
        "--output-format",
        "json",
        "--dangerously-skip-permissions",
        brief,
    ]

    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        timeout=timeout_seconds,
        check=False,
    )

    # Persist logs for debugging
    logs = REPO_ROOT / "audits" / f"synthesize-{final_slug}"
    logs.mkdir(parents=True, exist_ok=True)
    (logs / "claude-stdout.log").write_text(proc.stdout)
    (logs / "claude-stderr.log").write_text(proc.stderr)

    # Parse the assistant message wrapper for confirmation/derives count.
    derives_count: int | None = None
    try:
        import json as _json

        wrapper = _json.loads(proc.stdout)
        msg = wrapper.get("result", "") if isinstance(wrapper, dict) else ""
    except Exception:  # noqa: BLE001
        msg = proc.stdout

    m = CONFIRMATION_RE.search(msg)
    if m:
        try:
            derives_count = int(m.group(1))
        except ValueError:
            pass

    error: str | None = None
    if not note_path.exists():
        error = (
            f"synthesizer did not write {note_path} (rc={proc.returncode}); "
            f"see {logs}/claude-stderr.log for details"
        )
    elif derives_count is not None and derives_count < 5:
        error = (
            f"note written with only {derives_count} derives_from entries — "
            f"the synthesizer's hard rule requires >=5. Consider rerunning "
            f"with a broader seed query."
        )

    if note_path.exists() and reindex_after:
        result = reindex()
        if result.errors:
            tail = "; ".join(f"{p}: {e[:80]}" for p, e in result.errors[:3])
            error = (error + " | " if error else "") + f"reindex errors: {tail}"

    return SynthesizeResult(
        note_path=note_path,
        stdout_tail=proc.stdout[-1500:],
        derives_count=derives_count,
        error=error,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("topic", help="The topic to synthesize, e.g. 'flash loan governance attacks'.")
    parser.add_argument("--seed-query", help="Override the corpus search query (defaults to topic).")
    parser.add_argument("--slug", help="Override the filename slug (defaults to slugified topic).")
    parser.add_argument("--model", default="opus")
    parser.add_argument("--no-reindex", action="store_true")
    parser.add_argument("--timeout", type=int, default=1800)
    args = parser.parse_args(argv)

    result = synthesize(
        args.topic,
        seed_query=args.seed_query,
        slug=args.slug,
        model=args.model,
        reindex_after=not args.no_reindex,
        timeout_seconds=args.timeout,
    )

    print(f"note_path: {result.note_path}")
    print(f"derives_count: {result.derives_count}")
    if result.error:
        print(f"error: {result.error}", file=sys.stderr)
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
