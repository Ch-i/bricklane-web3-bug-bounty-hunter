"""Rank source files by likely-vulnerability-density (1-5 scale).

Anthropic Red Team's methodology for parallel security review uses a cheap
"how interesting is this file?" pre-pass to prioritize where the expensive
auditor's attention goes. A file ranked 1 (e.g. constants-only, types,
trivial setters) gets skipped; a file ranked 5 (auth, untrusted parsing,
funds movement, low-level call sites) goes first.

We use Claude Haiku for the ranking pass — fast, ~10× cheaper than Opus,
and a per-file 1-5 judgement doesn't need deep reasoning. The ranker
emits a JSON list ordered descending by rank.

CLI:
    python -m harness.ranker /path/to/project
    python -m harness.ranker /path/to/project --top-k 5
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from harness.corpus import REPO_ROOT


@dataclass
class FileRank:
    path: str
    rank: int            # 1..5; higher = more security-critical
    rationale: str       # one-line justification
    lines: int           # source line count for context
    error: str | None = None


RANKER_SYSTEM = """\
You are pre-screening a Solidity codebase to decide which files an expensive
security auditor should spend its time on. Output ONLY a single integer rank
1-5 followed by a colon followed by a one-line rationale.

Scale:
  1 = nothing security-relevant. Constants, types, simple getters, pure
      math libraries with no state, interfaces. Auditor should skip.
  2 = trivial logic. Single-purpose helpers, event-only emitters, view
      functions that read but don't mutate state, simple setters with
      onlyOwner gating.
  3 = standard application logic. Token transfers behind well-tested
      modifiers, deposit/withdraw with explicit access control, ordinary
      ERC20 wrappers. Worth a look but not the top priority.
  4 = security-critical logic with attack surface. External entry points
      that touch funds, custom math, lending/AMM/vault accounting,
      delegate proxies, on-chain pricing, governance / multisig logic.
  5 = highest priority. Untrusted parsing, signature verification,
      bridges/cross-chain message processing, flashloan callbacks,
      unprotected privileged actions, assembly blocks doing storage
      writes, contracts whose entire purpose is value custody.

Output format (single line, exact):
RANK: <N> :: <one-line rationale, <= 100 chars>

Do not output anything else. No preamble, no markdown.
"""


def _claude_bin() -> str | None:
    return shutil.which("claude")


def rank_file(
    path: Path,
    *,
    model: str = "haiku",
    timeout_seconds: int = 60,
) -> FileRank:
    """Spawn a tiny `claude -p` to rank one file."""
    cl = _claude_bin()
    if not cl:
        return FileRank(str(path), 0, "claude CLI not on PATH", 0, "no claude")

    text = path.read_text(errors="replace")
    lines = text.count("\n")
    # Trim long files: include the head + tail so the ranker sees imports + tail
    # state-mutation hot spots without burning context on the middle of big files.
    if lines > 600:
        head = "\n".join(text.splitlines()[:400])
        tail = "\n".join(text.splitlines()[-200:])
        body = head + "\n\n... [middle elided] ...\n\n" + tail
    else:
        body = text

    user_msg = (
        f"FILE: {path.name} ({lines} lines)\n"
        f"```solidity\n{body}\n```\n\n"
        f"Output exactly one line: 'RANK: <1-5> :: <rationale>'."
    )

    try:
        proc = subprocess.run(
            [
                cl, "-p", "--model", model,
                "--system-prompt", RANKER_SYSTEM,
                "--dangerously-skip-permissions",
                "--output-format", "json",
                user_msg,
            ],
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return FileRank(str(path), 0, "timeout", lines, "timeout")
    except Exception as e:  # noqa: BLE001
        return FileRank(str(path), 0, "subprocess error", lines, str(e))

    if proc.returncode != 0:
        return FileRank(str(path), 0, "claude rc != 0", lines, (proc.stderr or "")[-200:])

    # The --output-format json envelope wraps the assistant text in {"result": "..."}
    try:
        wrapper = json.loads(proc.stdout)
        text_out = wrapper.get("result", "") if isinstance(wrapper, dict) else proc.stdout
    except json.JSONDecodeError:
        text_out = proc.stdout

    m = re.search(r"RANK:\s*(\d)\s*::\s*(.+)", text_out)
    if not m:
        return FileRank(str(path), 0, "unparseable output", lines, text_out[:200])
    try:
        rank = int(m.group(1))
    except ValueError:
        return FileRank(str(path), 0, "non-int rank", lines, text_out[:200])
    rank = max(1, min(5, rank))
    return FileRank(str(path), rank, m.group(2).strip()[:200], lines)


def rank_project(
    project_root: Path,
    *,
    model: str = "haiku",
    scope: Path | None = None,
    max_files: int = 200,
) -> list[FileRank]:
    """Walk the project's .sol files, rank each, return sorted (desc) list.

    Skips lib/, node_modules/, out/, cache/, test/, scripts/, __web3sentinel_pocs__/.
    """
    root = scope or project_root
    skip_segments = {"lib", "node_modules", "out", "cache", "test", "scripts", "__web3sentinel_pocs__", ".forge-snapshots"}
    files: list[Path] = []
    if root.is_file() and root.suffix == ".sol":
        files = [root]
    else:
        for p in sorted(root.rglob("*.sol")):
            if any(seg in p.parts for seg in skip_segments):
                continue
            files.append(p)
            if len(files) >= max_files:
                break

    ranks: list[FileRank] = []
    for f in files:
        r = rank_file(f, model=model)
        ranks.append(r)
    ranks.sort(key=lambda r: (-r.rank, r.path))
    return ranks


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", help="Path to a Solidity project root or single file.")
    parser.add_argument("--scope", help="Restrict ranking to files under this subpath.")
    parser.add_argument("--top-k", type=int, default=None, help="Print only the top-K results.")
    parser.add_argument("--model", default="haiku")
    parser.add_argument("--max-files", type=int, default=200)
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of a human table.")
    args = parser.parse_args(argv)

    project = Path(args.target).expanduser().resolve()
    if not project.exists():
        print(f"error: {project} not found", file=sys.stderr)
        return 1

    scope = Path(args.scope).expanduser().resolve() if args.scope else None
    ranks = rank_project(project, scope=scope, model=args.model, max_files=args.max_files)
    if args.top_k:
        ranks = ranks[: args.top_k]

    if args.json:
        print(json.dumps([asdict(r) for r in ranks], indent=2))
        return 0

    for r in ranks:
        rel = r.path
        try:
            rel = str(Path(r.path).resolve().relative_to(project))
        except ValueError:
            pass
        flag = "  " if r.error is None else "! "
        print(f"{flag}[{r.rank}] {rel:60s}  ({r.lines:>4} lines)  {r.rationale[:80]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
