"""Filter findings — Anthropic-style "is this real & important?" pass.

The auditor (or reconciler) emits a list of findings, citations grounded,
PoC optionally reproduced. Before submission, a final agent reads each
finding alongside the source and votes:

    accept    — real, important, worth submitting
    downgrade — real but minor / niche / not worth a submission slot
    reject    — likely false positive, theoretical, or intended behavior

This mirrors the AR-paper's "received the following bug report, can you
confirm if it's real and interesting?" trick. It catches:
  * Findings that pattern-match an anti-pattern but aren't exploitable in
    this Solidity version (e.g. classical reentrancy with checked arith)
  * Findings whose impact requires preconditions the protocol prevents
  * Duplicates of public disclosures or already-fixed bugs

CLI:
    python -m harness.filter_agent <findings.json> --target /path/to/source
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from harness.corpus import REPO_ROOT


FILTER_SYSTEM = """\
You are reviewing a security audit finding to decide whether it is:
  ACCEPT    — real, exploitable, important. Submit to bounty / publish.
  DOWNGRADE — real but minor. Anti-pattern, defense-in-depth, or affects
              edge cases unlikely to matter. Note in audit report but
              don't submit as a critical bug.
  REJECT    — false positive, theoretical (not exploitable in this version),
              intended behavior, or pattern-match without verified attack
              vector.

You will be given:
  * The finding's full text (title, severity, description, impact,
    recommendation, citations, location).
  * The source file(s) the finding references, around the relevant lines.
  * (Optionally) a Foundry PoC and its execution result.

Reason carefully. Consider:
  * Does the bug actually trigger given Solidity's compiler version's
    arithmetic semantics? (>=0.8 has checked math by default — many
    classical bugs need `unchecked {}` to be exploitable.)
  * Does the protocol have upstream guards that prevent the exploit?
    (Read modifiers / require()s on every call path that reaches the
    flagged code.)
  * Does the impact require an unreasonable precondition (e.g. owner
    being malicious already)?
  * Is the PoC test ACTUALLY demonstrating funds-at-risk, or just
    exercising the function?

Output format (single line, exact):
VERDICT: <ACCEPT|DOWNGRADE|REJECT> :: <one-line rationale, <= 200 chars>

Do not output markdown, preamble, or anything else. Single line only.
"""


@dataclass
class FilterVerdict:
    finding_title: str
    verdict: str          # ACCEPT | DOWNGRADE | REJECT | ERROR
    rationale: str
    raw_response: str = ""


def _claude_bin() -> str | None:
    return shutil.which("claude")


def _read_source_around(finding: dict, target_root: Path, context_lines: int = 25) -> str:
    """Return source snippets around each location in the finding."""
    out_chunks: list[str] = []
    for loc in finding.get("location", []):
        file = loc.get("file", "")
        line_start = loc.get("line_start", 0)
        line_end = loc.get("line_end") or line_start
        # Resolve path
        for cand in (Path(file), target_root / file, target_root / Path(file).name):
            if cand.exists():
                src_path = cand
                break
        else:
            out_chunks.append(f"// {file}: not found")
            continue
        text = src_path.read_text(errors="replace").splitlines()
        a = max(0, line_start - 1 - context_lines)
        b = min(len(text), line_end + context_lines)
        numbered = [f"{i + 1:>4}: {text[i]}" for i in range(a, b)]
        out_chunks.append(f"// {file}:{line_start}-{line_end}\n" + "\n".join(numbered))
    return "\n\n".join(out_chunks) if out_chunks else "(no location resolvable)"


def judge_finding(
    finding: dict,
    target_root: Path,
    *,
    model: str = "opus",
    timeout_seconds: int = 180,
) -> FilterVerdict:
    """Spawn a single claude -p call to verdict on this finding."""
    cl = _claude_bin()
    if not cl:
        return FilterVerdict(finding.get("title", "?"), "ERROR", "claude CLI not on PATH")

    title = finding.get("title", "(no title)")
    severity = finding.get("severity", "?")
    description = finding.get("description", "")
    impact = finding.get("impact", "")
    recommendation = finding.get("recommendation", "")
    citations = ", ".join(finding.get("citations") or []) or "—"
    poc_status = finding.get("poc_status", "not-attempted")
    foundry_poc = finding.get("foundry_poc")

    source_snippet = _read_source_around(finding, target_root)

    poc_block = ""
    if foundry_poc:
        poc_block = (
            f"\n## Foundry PoC (status: {poc_status})\n"
            f"setup:\n```solidity\n{foundry_poc.get('setup', '')}\n```\n"
            f"exploit:\n```solidity\n{foundry_poc.get('exploit', '')}\n```\n"
            f"assertion:\n```solidity\n{foundry_poc.get('assertion', '')}\n```\n"
        )

    user_msg = (
        f"# Finding\n\n"
        f"**{title}** [{severity}]\n\n"
        f"## Description\n{description}\n\n"
        f"## Impact\n{impact}\n\n"
        f"## Recommendation\n{recommendation}\n\n"
        f"## Citations\n{citations}\n\n"
        f"## Source context\n```solidity\n{source_snippet}\n```\n"
        f"{poc_block}\n"
        f"Issue your verdict now. Single line: 'VERDICT: <ACCEPT|DOWNGRADE|REJECT> :: <rationale>'."
    )

    try:
        proc = subprocess.run(
            [
                cl, "-p", "--model", model,
                "--system-prompt", FILTER_SYSTEM,
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
        return FilterVerdict(title, "ERROR", "timeout")
    except Exception as e:  # noqa: BLE001
        return FilterVerdict(title, "ERROR", f"subprocess: {e}")

    try:
        wrapper = json.loads(proc.stdout)
        text_out = wrapper.get("result", "") if isinstance(wrapper, dict) else proc.stdout
    except json.JSONDecodeError:
        text_out = proc.stdout

    m = re.search(r"VERDICT:\s*(ACCEPT|DOWNGRADE|REJECT)\s*::\s*(.+)", text_out, re.IGNORECASE)
    if not m:
        return FilterVerdict(title, "ERROR", "unparseable", text_out[:400])
    return FilterVerdict(
        finding_title=title,
        verdict=m.group(1).upper(),
        rationale=m.group(2).strip()[:400],
        raw_response=text_out[:400],
    )


def filter_findings(
    findings: list[dict],
    target_root: Path,
    *,
    model: str = "opus",
) -> list[tuple[dict, FilterVerdict]]:
    """Judge each finding, return list of (finding, verdict) tuples."""
    out: list[tuple[dict, FilterVerdict]] = []
    for f in findings:
        v = judge_finding(f, target_root, model=model)
        # Annotate the finding in-place too so downstream consumers can re-render.
        f.setdefault("filter", {})
        f["filter"]["verdict"] = v.verdict
        f["filter"]["rationale"] = v.rationale
        out.append((f, v))
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("findings_path", help="Path to findings.json or reconciled.json.")
    parser.add_argument("--target", required=True, help="Path to source root for resolving locations.")
    parser.add_argument("--model", default="opus")
    parser.add_argument("--out", help="Write annotated JSON here (default: in-place).")
    args = parser.parse_args(argv)

    data = json.loads(Path(args.findings_path).read_text())
    findings = data if isinstance(data, list) else data.get("findings", [])
    target_root = Path(args.target).expanduser().resolve()

    print(f"Judging {len(findings)} findings against {target_root}...\n")
    results = filter_findings(findings, target_root, model=args.model)
    for f, v in results:
        sym = {"ACCEPT": "✓", "DOWNGRADE": "↓", "REJECT": "✗", "ERROR": "!"}[v.verdict]
        print(f"  {sym} [{v.verdict:9s}] {v.finding_title[:60]:60s} — {v.rationale[:80]}")

    out_path = Path(args.out) if args.out else Path(args.findings_path)
    if isinstance(data, list):
        out_path.write_text(json.dumps(findings, indent=2))
    else:
        data["findings"] = findings
        out_path.write_text(json.dumps(data, indent=2))
    print(f"\nWrote annotated findings → {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
