"""Stage 1 Opus-driven candidate ranker.

For each candidate (a C4/Sherlock/Cantina contest or Immunefi program),
spawn a single `claude -p` call that synthesizes:

  * Static-tool counts (slither + aderyn) — quick prep
  * Lexical danger-primitive density (delegatecall / assembly / tx.origin / etc.)
  * Top corpus prior-art hits (auto-derived from contract names, file paths,
    and imported library names)
  * The most-suspect file's full source (auto-selected by SLOC + danger density)

…and emits:

    {
      "score": 1-10,
      "rationale": "...",                # one-liner read at the queue
      "top_suspects": [{"file","function","why"}, ...],
      "skip_reasons": []                  # populated only when score < 3
    }

Designed to be a SINGLE Opus message per candidate, ~$0 incremental on
Pro Max. For 100 candidates/week, that's ~100 messages of the ~900-per-
5h-window quota.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from harness import candidates as cand_store
from harness import corpus
from harness.candidates import Candidate
from harness.corpus import REPO_ROOT
from harness.static import StaticToolsConfig, run_aderyn, run_slither

STAGE1_SYSTEM = """\
You are pre-screening a Solidity bounty-eligible target to decide how much
expensive deep-audit budget it deserves. You will be given:

  * Project metadata (platform, payout cap if known, scope file count)
  * Static-tool detector counts (slither, aderyn) — terse summary
  * Lexical danger-primitive grep counts (delegatecall, assembly, tx.origin,
    unchecked, ecrecover, low-level .call, selfdestruct)
  * Top 8 corpus prior-art hits with one-line titles + severities
  * The full source of the most-suspect file (auto-selected by SLOC +
    danger density)

You must output ONLY a single JSON object matching this schema:

    {
      "score": <integer 1-10>,
      "rationale": "<<=180 char one-liner that summarizes WHY this score>",
      "top_suspects": [
        {"file": "src/Foo.sol", "function": "withdraw",
         "why": "<short why>"},
        ...up to 3 entries...
      ],
      "skip_reasons": [<strings; empty list unless score < 3>]
    }

Scoring rubric (be calibrated, not generous):
  1-2  = no real surface (constants, simple stub, fully audited mature
         protocol with no relevant prior-art match). Output skip_reasons.
  3-4  = standard application logic; likely-already-covered patterns.
  5-6  = security-critical surface (funds-touching) but constraints look
         tight; non-obvious bugs may exist.
  7-8  = high-value surface AND strong prior-art match for known bug
         classes; novel custom logic; weak coverage; unchecked / assembly.
  9-10 = exceptional alignment: novel funds-handling, untrusted parsing,
         signature verification, or recursive delegate proxies, with at
         least one corpus entry indicating the exact pattern has been
         exploited in production. Save 10 for "I'd bet money there's a bug here."

In top_suspects, name SPECIFIC functions (not just file paths) and a
specific reason — these will be passed verbatim to the deep auditor as
"start your hunt here" hints. Pick functions you'd attack first if you
were the auditor.

Output ONLY the JSON. No prose, no markdown, no preamble.
"""


# ---------------------------------------------------------------------------
# Signal gatherers
# ---------------------------------------------------------------------------


DANGER_PRIMITIVES = {
    "delegatecall": r"\.delegatecall\s*\(",
    "selfdestruct": r"\b(selfdestruct|suicide)\s*\(",
    "assembly": r"\bassembly\s*\{",
    "tx.origin": r"\btx\.origin\b",
    "unchecked": r"\bunchecked\s*\{",
    "ecrecover": r"\becrecover\s*\(",
    "low_level_call": r"\.call\s*\{",
    "transferfrom_arbitrary": r"\.transferFrom\s*\(",
}


def _grep_primitives(source_root: Path) -> dict[str, int]:
    counts = {k: 0 for k in DANGER_PRIMITIVES}
    for p in source_root.rglob("*.sol"):
        if any(seg in p.parts for seg in ("lib", "node_modules", "out", "cache", "test")):
            continue
        try:
            text = p.read_text(errors="replace")
        except OSError:
            continue
        for name, pat in DANGER_PRIMITIVES.items():
            counts[name] += len(re.findall(pat, text))
    return counts


def _file_metrics(source_root: Path) -> list[dict]:
    """Per .sol file: sloc + danger-density. Skips libs/tests."""
    out: list[dict] = []
    for p in sorted(source_root.rglob("*.sol")):
        if any(seg in p.parts for seg in ("lib", "node_modules", "out", "cache", "test")):
            continue
        try:
            text = p.read_text(errors="replace")
        except OSError:
            continue
        sloc = max(1, sum(1 for line in text.splitlines() if line.strip() and not line.strip().startswith("//")))
        dangers = sum(len(re.findall(pat, text)) for pat in DANGER_PRIMITIVES.values())
        out.append({
            "path": str(p.relative_to(source_root)),
            "abs_path": str(p),
            "sloc": sloc,
            "dangers": dangers,
            "danger_density": dangers / sloc,
        })
    return out


def _select_most_suspect_file(metrics: list[dict]) -> Path | None:
    if not metrics:
        return None
    # Combined heuristic: rank by danger_density then sloc; cap at 1000 SLOC
    # to keep the prompt-size bounded.
    ranked = sorted(metrics, key=lambda d: (-d["danger_density"], -d["sloc"]))
    for m in ranked:
        if m["sloc"] <= 1500:
            return Path(m["abs_path"])
    # If everything is huge, pick the largest anyway
    return Path(ranked[0]["abs_path"])


def _quick_static(source_root: Path) -> dict:
    """Run slither + aderyn for terse detector counts. Returns {} on failure."""
    cfg = StaticToolsConfig(target=source_root, target_kind="foundry-project")
    slither = run_slither(cfg)
    aderyn = run_aderyn(cfg)
    return {
        "slither_detectors": (slither.output or {}).get("detector_count", 0) if slither.succeeded else None,
        "slither_error": None if slither.succeeded else slither.error,
        "aderyn_issues": (aderyn.output or {}).get("issue_count", 0) if aderyn.succeeded else None,
        "aderyn_error": None if aderyn.succeeded else aderyn.error,
    }


def _corpus_priors(source_root: Path, contract_names: list[str], top_k: int = 8) -> list[dict]:
    """Search the corpus for prior art using contract names + danger keywords."""
    queries: list[str] = []
    queries.extend(contract_names[:3])
    # Sample some import paths for additional grounding
    imports: set[str] = set()
    for p in source_root.rglob("*.sol"):
        if any(seg in p.parts for seg in ("lib", "node_modules", "out", "cache", "test")):
            continue
        try:
            text = p.read_text(errors="replace")
        except OSError:
            continue
        for m in re.finditer(r'import\s+(?:\{[^}]+\}\s+from\s+)?["\']([^"\']+)["\']', text):
            imports.add(m.group(1).rsplit("/", 1)[-1].replace(".sol", ""))
    queries.extend(sorted(imports)[:3])

    seen: set[str] = set()
    hits: list[dict] = []
    for q in queries:
        if not q:
            continue
        for h in corpus.search(q, top_k=top_k):
            if h.id in seen:
                continue
            seen.add(h.id)
            hits.append({
                "id": h.id,
                "title": h.title,
                "source": h.source,
                "severity": h.severity,
                "snippet": h.snippet,
            })
    # Sort by severity (Critical first) then by source preference (synthesis first)
    sev_rank = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Informational": 4, "Gas": 5}
    src_rank = {"synthesis": 0, "rekt": 1, "solodit": 2, "swc": 3, "arxiv": 4}
    hits.sort(key=lambda h: (sev_rank.get(h["severity"] or "", 99), src_rank.get(h["source"], 9)))
    return hits[: top_k * 2]


def _contract_names(source_root: Path) -> list[str]:
    names: set[str] = set()
    for p in source_root.rglob("*.sol"):
        if any(seg in p.parts for seg in ("lib", "node_modules", "out", "cache", "test")):
            continue
        try:
            text = p.read_text(errors="replace")
        except OSError:
            continue
        for m in re.finditer(r"^\s*(?:abstract\s+)?contract\s+(\w+)", text, re.MULTILINE):
            names.add(m.group(1))
    return sorted(names)


# ---------------------------------------------------------------------------
# Opus call
# ---------------------------------------------------------------------------


def _claude_bin() -> str | None:
    return shutil.which("claude")


def _format_prior_art(hits: list[dict], limit: int = 8) -> str:
    if not hits:
        return "(no relevant corpus prior-art)"
    lines = []
    for h in hits[:limit]:
        sev = (h.get("severity") or "—")[:4]
        lines.append(f"- [{sev}] [{h['source']}] {h['id']} :: {(h.get('title') or '')[:120]}")
    return "\n".join(lines)


def _build_brief(cand: Candidate, source_root: Path) -> str:
    metrics = _file_metrics(source_root)
    contracts = _contract_names(source_root)
    dangers = _grep_primitives(source_root)
    static = _quick_static(source_root)
    suspect = _select_most_suspect_file(metrics)
    prior = _corpus_priors(source_root, contracts)

    files_summary = (
        ", ".join(f"{m['path']}({m['sloc']}sloc, {m['dangers']}danger)" for m in metrics[:15])
        + (f"... and {len(metrics) - 15} more" if len(metrics) > 15 else "")
    )
    suspect_src = ""
    if suspect:
        try:
            text = suspect.read_text(errors="replace")
        except OSError:
            text = ""
        # Trim to ~600 lines max to keep the prompt under budget
        if text.count("\n") > 600:
            head = "\n".join(text.splitlines()[:400])
            tail = "\n".join(text.splitlines()[-150:])
            text = head + "\n\n// ... [middle elided] ...\n\n" + tail
        suspect_src = f"## Most-suspect file: {suspect.relative_to(source_root)}\n```solidity\n{text}\n```"

    payout = f"${cand.payout_max_usd:,}" if cand.payout_max_usd else "unknown"

    return (
        f"# Stage 1 triage: {cand.title}\n\n"
        f"- platform:        {cand.platform}\n"
        f"- kind:            {cand.kind}\n"
        f"- payout cap:      {payout}\n"
        f"- closes_at:       {cand.closes_at or '(continuous)'}\n"
        f"- repo:            {cand.repo_url or '(deployed)'}\n"
        f"- commit:          {cand.commit or '(unpinned)'}\n"
        f"- contracts:       {', '.join(contracts[:10]) or '(none parsed)'}\n"
        f"- scope files:     {len(metrics)}\n"
        f"- files (snip):    {files_summary}\n\n"
        f"## Static-tool counts\n"
        f"- slither detectors: {static.get('slither_detectors')}  err={static.get('slither_error')}\n"
        f"- aderyn issues:     {static.get('aderyn_issues')}  err={static.get('aderyn_error')}\n\n"
        f"## Dangerous-primitive grep\n"
        f"{json.dumps(dangers)}\n\n"
        f"## Corpus prior-art (top hits)\n"
        f"{_format_prior_art(prior)}\n\n"
        f"{suspect_src}\n\n"
        f"Output ONLY the JSON object per your system prompt."
    )


@dataclass
class Stage1Result:
    candidate_id: str
    score: int
    rationale: str
    top_suspects: list[dict]
    skip_reasons: list[str]
    raw_response: str = ""
    error: str | None = None


def rank_candidate(
    cand: Candidate,
    source_root: Path,
    *,
    model: str = "opus",
    timeout_seconds: int = 600,
) -> Stage1Result:
    """Spawn a single claude -p, return the structured Stage1Result."""
    cl = _claude_bin()
    if not cl:
        return Stage1Result(cand.id, 0, "claude CLI missing", [], ["claude CLI not on PATH"], error="no claude")

    brief = _build_brief(cand, source_root)

    try:
        proc = subprocess.run(
            [
                cl, "-p", "--model", model,
                "--system-prompt", STAGE1_SYSTEM,
                "--dangerously-skip-permissions",
                "--output-format", "json",
                brief,
            ],
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return Stage1Result(cand.id, 0, "timeout", [], ["claude timeout"], error="timeout")
    except Exception as e:  # noqa: BLE001
        return Stage1Result(cand.id, 0, "subprocess error", [], [str(e)], error=str(e))

    if proc.returncode != 0:
        tail = (proc.stderr or "")[-300:]
        return Stage1Result(cand.id, 0, "claude rc != 0", [], [tail], error=tail)

    try:
        wrapper = json.loads(proc.stdout)
        text_out = wrapper.get("result", "") if isinstance(wrapper, dict) else proc.stdout
    except json.JSONDecodeError:
        text_out = proc.stdout

    # Extract the JSON object from the response (may have stray prefix/suffix)
    payload = None
    m = re.search(r"\{.*\}", text_out, re.DOTALL)
    if m:
        try:
            payload = json.loads(m.group(0))
        except json.JSONDecodeError:
            payload = None
    if not isinstance(payload, dict):
        return Stage1Result(cand.id, 0, "unparseable JSON", [], [text_out[:200]], raw_response=text_out[:500])

    score = int(payload.get("score", 0))
    score = max(1, min(10, score)) if score else 0
    return Stage1Result(
        candidate_id=cand.id,
        score=score,
        rationale=str(payload.get("rationale", ""))[:240],
        top_suspects=list(payload.get("top_suspects") or [])[:3],
        skip_reasons=list(payload.get("skip_reasons") or []),
        raw_response=text_out[:1500],
    )


def apply_to_candidate(cand: Candidate, result: Stage1Result) -> Candidate:
    """Mutate-and-return: write Stage1 results into the Candidate fields."""
    cand.triage_status = "stage1"
    cand.triage_score = float(result.score)
    cand.triage_rationale = result.rationale
    cand.triage_top_suspects = result.top_suspects
    cand.triage_skip_reasons = result.skip_reasons
    cand.last_triaged_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    return cand


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate_id", help="Stage-1 rank a specific candidate by id.")
    parser.add_argument("--model", default="opus")
    args = parser.parse_args(argv)

    cand = cand_store.get(args.candidate_id)
    if not cand:
        print(f"error: no candidate {args.candidate_id}", file=sys.stderr)
        return 1
    if not cand.local_path or not Path(cand.local_path).exists():
        print(f"error: candidate has no local source ({cand.local_path}); run sweep first", file=sys.stderr)
        return 2

    result = rank_candidate(cand, Path(cand.local_path), model=args.model)
    apply_to_candidate(cand, result)
    cand_store.upsert(cand)
    cand_store.reindex()

    print(f"score: {result.score}/10  ::  {result.rationale}")
    for s in result.top_suspects:
        print(f"  suspect: {s.get('file')}::{s.get('function')}  --  {s.get('why')}")
    for r in result.skip_reasons:
        print(f"  skip:    {r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
