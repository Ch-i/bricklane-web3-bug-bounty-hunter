"""Deep-dive analysis: scrutinize ONE target exhaustively.

After Stage 1 ranks a candidate and Stage 2 produces an audit, deep-dive
is the "spend a whole day on one subject" pattern. It walks every
function in the target, runs an Opus pass per function with the FULL
file context + corpus priors + cross-function hints, then aggregates
into a per-function risk map and a cross-function interaction matrix.

Two phases:
  1. Decompose  — extract every (contract, function) unit with metadata
  2. Per-function audit — one Opus call per function, focused on its
                          attack surface; results saved to JSONL
  3. Cross-function reasoning — for pairs of functions that share state
                                 or call each other, run an interaction
                                 audit pass
  4. Aggregate  — render a deep_dive_report.md with full per-function
                  analyses + an interaction matrix

State is persisted between runs so a 4+ hour session can be paused and
resumed. Each function's analysis is cached by (target_sha, fn_id) so
re-runs only burn LLM budget on what changed.

Cost discipline:
  * Per function: 1 Opus call (~5-15k tokens) = 1 message on Pro Max.
  * For a 30-function target: ~30 messages. Comfortable.
  * Cross-function pass: ~N*(N-1)/2 in the worst case; we cap at 50
    highest-risk pairs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from collections.abc import Iterator
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from harness import corpus
from harness.corpus import REPO_ROOT

DEEP_DIR_NAME = "deep-dive"
PER_FN_SYSTEM = """\
You are doing an EXHAUSTIVE, focused security audit of one function in a
Solidity codebase. You will be told:

  * The target's overall purpose (1-2 lines)
  * The function's FULL source with line numbers
  * The enclosing contract's full source for context
  * Corpus prior-art hits relevant to this function's pattern
  * Any prior deep-dive findings on related functions

Your job: enumerate EVERY plausible vulnerability in this function. Be
thorough — list things you're 70% sure of, things you're 30% sure of,
and explicitly flag both. Walk through the function step by step. For
each candidate vulnerability, give:

  * what the bug is
  * the precondition for exploit (who can call, what state needed)
  * the postcondition / impact (what attacker gains)
  * a confidence rating (high / medium / low / speculative)
  * whether Solidity 0.8 checked math matters here
  * an estimated severity (Critical / High / Medium / Low / Info)
  * a sketch of a Foundry PoC if exploitable

ALSO list the INVARIANTS this function relies on or maintains. An
invariant is a property the function ASSUMES is true (a precondition
the rest of the codebase is supposed to enforce) or ESTABLISHES
(a postcondition the function guarantees on success). Examples:

  * "totalShares == sum(balances)"     — system-wide accounting invariant
  * "userBalance[u] <= totalBalance"   — per-user can't exceed total
  * "msg.sender is owner OR proposal passed"  — access invariant
  * "block.timestamp >= unlockTime"    — temporal invariant

Invariants are how the cross-function pass detects violations: if fn A
establishes an invariant and fn B can break it, that's a bug.

Output ONLY this JSON shape:

{
  "function_id": "<file>::<contract>::<fn>",
  "summary": "one-line description of what this function does",
  "trust_boundary": "<who can call: anyone | onlyOwner | onlyRole | only<contract>>",
  "value_flow": "<does ETH or tokens move in/out? where?>",
  "state_writes": [{"slot": "<var>", "condition": "<when>"}],
  "external_calls": [{"target": "<addr-or-var>", "kind": "call | delegatecall | staticcall | transfer | safeTransfer", "before_state_update": <bool>}],
  "invariants_assumed": ["<property this function depends on being true>"],
  "invariants_established": ["<property this function guarantees on success>"],
  "candidate_vulnerabilities": [
    {
      "title": "...",
      "description": "...",
      "precondition": "...",
      "impact": "...",
      "severity": "Critical|High|Medium|Low|Info",
      "confidence": "high|medium|low|speculative",
      "blocked_by_solc_08_checks": <bool or null>,
      "poc_sketch": "<solidity-like pseudocode or null>"
    }
  ],
  "safe_observations": ["<things you checked and confirmed are NOT bugs>"],
  "notes": "<any open questions or context the cross-function pass should consider>"
}

Be brutal in your enumeration. If you don't list a vulnerability now, no
one will. But also be calibrated — confidence:low / speculative is fine,
hallucinating Critical confidence is not.
"""


CROSS_FN_SYSTEM = """\
You are reasoning about the INTERACTION between two functions a security
auditor has individually analyzed. The single-function audits each
covered their own surface; you must find bugs that ONLY appear in the
interaction — re-entrancy across functions, ordering attacks, state
asymmetry, donation-based liquidation, etc.

You will be given:
  * Function A's full source + the prior single-fn analysis
  * Function B's full source + its analysis
  * The shared state (variables both functions write or read)
  * Each function's invariants_assumed + invariants_established
  * Corpus prior-art on cross-function attack patterns

PRIMARY ATTACK SHAPE: INVARIANT BREAKAGE.
Look for cases where fn A ESTABLISHES an invariant that fn B then
BREAKS or RELIES on differently. Examples to think about:

  * A assumes "totalSupply == sum(balances)" but B mints without updating both
  * A assumes "msg.sender == owner" via modifier, but B can be reached via
    a delegatecall path that bypasses the modifier
  * A establishes "lockedUntil >= now + DELAY" but B can reduce lockedUntil
  * A reads price, then B executes — price changed (oracle stale)
  * A's reentry guard doesn't cover B (multi-function reentrancy)

Output ONLY this JSON:

{
  "pair_id": "<fn_a> + <fn_b>",
  "shared_state": ["<var names>"],
  "interaction_kind": "shares-state | a-calls-b | b-calls-a | both-public-shared",
  "broken_invariants": [
    {"invariant": "<which invariant>", "broken_by": "<a|b>", "how": "<short>"}
  ],
  "vulnerabilities": [
    {
      "title": "Cross-fn ...",
      "sequence": "<call sequence>",
      "description": "...",
      "impact": "...",
      "severity": "Critical|High|Medium|Low|Info",
      "confidence": "high|medium|low|speculative",
      "poc_sketch": "..."
    }
  ],
  "notes": "<additional context>"
}

Skip the pair (output empty vulnerabilities array) if the interaction
is provably safe (e.g., disjoint state, no call edge, no overlapping
reentry path, no shared invariant).
"""


# ---------------------------------------------------------------------------
# Decomposition
# ---------------------------------------------------------------------------


_FN_RE = re.compile(
    r"(?ms)\b(function|receive|fallback|constructor|modifier)\b(?:\s+(\w+))?\s*"
    r"(?:\(([^)]*)\))?([^{]*?)(\{)"
)
_CONTRACT_RE = re.compile(
    r"^(\s*)(?:abstract\s+)?(contract|library|interface)\s+(\w+)",
    re.MULTILINE,
)


@dataclass
class FunctionUnit:
    file: str            # relative path under target_root
    contract: str
    name: str            # may be "fallback" / "receive" for unnamed
    visibility: str      # public | external | internal | private | unknown
    mutability: str      # view | pure | payable | nonpayable
    line_start: int
    line_end: int
    source: str          # full source slice including signature + body
    # Computed at decompose-time
    danger_grep: dict[str, int] = field(default_factory=dict)
    reads_state: list[str] = field(default_factory=list)
    writes_state: list[str] = field(default_factory=list)

    @property
    def fn_id(self) -> str:
        return f"{self.file}::{self.contract}::{self.name}"


DANGER_PATTERNS = {
    "delegatecall": r"\.delegatecall\s*\(",
    "selfdestruct": r"\b(selfdestruct|suicide)\s*\(",
    "assembly": r"\bassembly\s*\{",
    "tx.origin": r"\btx\.origin\b",
    "unchecked": r"\bunchecked\s*\{",
    "ecrecover": r"\becrecover\s*\(",
    "low_level_call": r"\.call\s*\{",
    "transferfrom": r"\.transferFrom\s*\(",
    "external_call": r"\.call\s*\(",
}


def _match_braces(text: str, start: int) -> int:
    """Return the index AFTER the matching closing brace of `{` at text[start]."""
    depth = 0
    i = start
    in_str = None
    in_comment_line = False
    in_comment_block = False
    while i < len(text):
        ch = text[i]
        nxt = text[i + 1] if i + 1 < len(text) else ""
        if in_comment_line:
            if ch == "\n":
                in_comment_line = False
        elif in_comment_block:
            if ch == "*" and nxt == "/":
                in_comment_block = False
                i += 1
        elif in_str:
            if ch == "\\":
                i += 1
            elif ch == in_str:
                in_str = None
        else:
            if ch == "/" and nxt == "/":
                in_comment_line = True
            elif ch == "/" and nxt == "*":
                in_comment_block = True
            elif ch in ("'", '"'):
                in_str = ch
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return i + 1
        i += 1
    return len(text)


def _extract_contract_for_offset(text: str, offset: int) -> str:
    """Find the most-recent contract/library/interface name before offset."""
    last = "(global)"
    for m in _CONTRACT_RE.finditer(text):
        if m.start() > offset:
            break
        last = m.group(3)
    return last


def _grep_dangers(source: str) -> dict[str, int]:
    return {k: len(re.findall(p, source)) for k, p in DANGER_PATTERNS.items()}


def _line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def decompose_file(file_path: Path, root: Path) -> list[FunctionUnit]:
    """Extract every function from one .sol file."""
    text = file_path.read_text(errors="replace")
    rel = str(file_path.relative_to(root))
    units: list[FunctionUnit] = []
    for m in _FN_RE.finditer(text):
        keyword = m.group(1)
        name = m.group(2) or keyword  # "receive" / "fallback" / "constructor" are unnamed
        sig_extras = m.group(4) or ""
        body_start = m.end(5) - 1  # index of `{`
        body_end = _match_braces(text, body_start)
        source = text[m.start() : body_end]
        # Parse visibility + mutability from signature extras
        vis = "unknown"
        for v in ("public", "external", "internal", "private"):
            if re.search(rf"\b{v}\b", sig_extras):
                vis = v
                break
        mut = "nonpayable"
        for m2 in ("view", "pure", "payable"):
            if re.search(rf"\b{m2}\b", sig_extras):
                mut = m2
                break
        contract = _extract_contract_for_offset(text, m.start())
        units.append(
            FunctionUnit(
                file=rel,
                contract=contract,
                name=name,
                visibility=vis,
                mutability=mut,
                line_start=_line_of(text, m.start()),
                line_end=_line_of(text, body_end),
                source=source,
                danger_grep=_grep_dangers(source),
            )
        )
    return units


def decompose(target_root: Path, scope: Path | None = None) -> list[FunctionUnit]:
    """Walk the target, decompose every in-scope .sol into FunctionUnits."""
    walk_root = scope or target_root
    # Single-file target: decompose just that file (resolve relative-to the parent dir).
    if walk_root.is_file():
        if walk_root.suffix != ".sol":
            return []
        anchor = target_root if target_root.is_dir() else walk_root.parent
        try:
            return decompose_file(walk_root, anchor)
        except Exception:  # noqa: BLE001
            return []
    skip_segments = {"lib", "node_modules", "out", "cache", "test", "scripts", "__web3sentinel_pocs__"}
    units: list[FunctionUnit] = []
    anchor = target_root if target_root.is_dir() else target_root.parent
    for p in sorted(walk_root.rglob("*.sol")):
        if any(seg in p.parts for seg in skip_segments):
            continue
        try:
            units.extend(decompose_file(p, anchor))
        except Exception:  # noqa: BLE001
            continue
    return units


# ---------------------------------------------------------------------------
# Per-function Opus pass
# ---------------------------------------------------------------------------


def _claude_bin() -> str | None:
    return shutil.which("claude")


def _hash_unit(u: FunctionUnit) -> str:
    return hashlib.sha1(u.source.encode("utf-8")).hexdigest()[:12]


def _corpus_priors_for_fn(u: FunctionUnit, top_k: int = 5) -> list[dict]:
    """Search the corpus for prior art relevant to this specific function.

    Synthesis-source entries (dense corpus distillations) are boosted to the
    top of the result list — they're the highest-density grounding the agent
    will get and reading them first changes which bugs surface.
    """
    queries: list[str] = []
    # Function name (e.g., "donateToReserves", "flashLoan")
    if u.name and u.name not in ("constructor", "fallback", "receive"):
        queries.append(u.name)
    # Danger-keyword combos
    for danger, count in u.danger_grep.items():
        if count > 0:
            queries.append(danger)
    seen: set[str] = set()
    hits: list[dict] = []
    for q in queries[:6]:
        for h in corpus.search(q, top_k=top_k):
            if h.id in seen:
                continue
            seen.add(h.id)
            hits.append(
                {"id": h.id, "title": h.title, "source": h.source, "severity": h.severity}
            )
    # Two-key sort: synthesis-source first, then by severity rank.
    sev_rank = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Informational": 4, "Gas": 5}
    hits.sort(key=lambda h: (
        0 if h["source"] == "synthesis" else 1,
        sev_rank.get(h["severity"] or "", 99),
    ))
    return hits[: top_k * 2]


def _build_fn_brief(u: FunctionUnit, target_root: Path, prior_findings: list[dict] | None = None) -> str:
    """Compose the prompt body for one per-function deep-dive call."""
    full_file_path = target_root / u.file
    file_src = full_file_path.read_text(errors="replace") if full_file_path.exists() else ""
    # Trim file source if huge — keep ±200 lines around the function.
    if file_src.count("\n") > 700:
        lines = file_src.splitlines()
        a = max(0, u.line_start - 200)
        b = min(len(lines), u.line_end + 200)
        file_src = "\n".join(lines[a:b])

    priors = _corpus_priors_for_fn(u)
    priors_block = "\n".join(
        f"- [{(h['severity'] or '—')[:4]}] {h['source']}: {h['id']} :: {(h.get('title') or '')[:90]}"
        for h in priors
    ) or "(no prior art)"

    prior_findings_block = ""
    if prior_findings:
        prior_findings_block = (
            "## Prior single-fn analyses on related functions\n"
            + "\n".join(
                f"- {p.get('function_id')}: {p.get('summary', '')[:140]}"
                for p in prior_findings[:8]
            )
            + "\n"
        )

    return (
        f"# Deep-dive: {u.fn_id}\n\n"
        f"- visibility:  {u.visibility}\n"
        f"- mutability:  {u.mutability}\n"
        f"- lines:       {u.line_start}-{u.line_end}\n"
        f"- dangers:     {json.dumps(u.danger_grep)}\n\n"
        f"## Function (line-numbered)\n"
        f"```solidity\n"
        f"{_with_line_numbers(u.source, u.line_start)}\n"
        f"```\n\n"
        f"## Enclosing file context\n"
        f"```solidity\n"
        f"{file_src}\n"
        f"```\n\n"
        f"## Corpus prior art\n{priors_block}\n\n"
        f"{prior_findings_block}\n"
        f"Output ONLY the JSON described in the system prompt."
    )


def _with_line_numbers(text: str, start_line: int) -> str:
    out = []
    for i, line in enumerate(text.splitlines(), start=start_line):
        out.append(f"{i:>4}: {line}")
    return "\n".join(out)


@dataclass
class FunctionAnalysis:
    function_id: str
    summary: str = ""
    trust_boundary: str = ""
    value_flow: str = ""
    state_writes: list = field(default_factory=list)
    external_calls: list = field(default_factory=list)
    invariants_assumed: list = field(default_factory=list)
    invariants_established: list = field(default_factory=list)
    candidate_vulnerabilities: list = field(default_factory=list)
    safe_observations: list = field(default_factory=list)
    notes: str = ""
    raw_response: str = ""
    error: str | None = None
    analyzed_at: str = ""
    source_hash: str = ""

    @property
    def max_severity(self) -> str:
        sev_rank = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Info": 4, "Informational": 4}
        best = 99
        best_sev = "—"
        for v in self.candidate_vulnerabilities:
            r = sev_rank.get(v.get("severity"), 99)
            if r < best:
                best = r
                best_sev = v.get("severity")
        return best_sev


def analyze_function(
    u: FunctionUnit,
    target_root: Path,
    *,
    model: str = "opus",
    timeout_seconds: int = 600,
    prior_findings: list[dict] | None = None,
) -> FunctionAnalysis:
    cl = _claude_bin()
    if not cl:
        return FunctionAnalysis(function_id=u.fn_id, error="claude CLI missing")

    brief = _build_fn_brief(u, target_root, prior_findings)

    try:
        proc = subprocess.run(
            [
                cl, "-p", "--model", model,
                "--system-prompt", PER_FN_SYSTEM,
                "--dangerously-skip-permissions",
                "--output-format", "json",
                brief,
            ],
            capture_output=True, text=True, timeout=timeout_seconds, check=False,
        )
    except subprocess.TimeoutExpired:
        return FunctionAnalysis(function_id=u.fn_id, error="claude timeout")
    except Exception as e:  # noqa: BLE001
        return FunctionAnalysis(function_id=u.fn_id, error=f"subprocess: {e}")

    if proc.returncode != 0:
        return FunctionAnalysis(
            function_id=u.fn_id,
            error=f"rc={proc.returncode}: {(proc.stderr or '')[-200:]}",
        )

    try:
        wrapper = json.loads(proc.stdout)
        text_out = wrapper.get("result", "") if isinstance(wrapper, dict) else proc.stdout
    except json.JSONDecodeError:
        text_out = proc.stdout

    m = re.search(r"\{.*\}", text_out, re.DOTALL)
    if not m:
        return FunctionAnalysis(
            function_id=u.fn_id, error="unparseable JSON", raw_response=text_out[:1500],
        )
    try:
        payload = json.loads(m.group(0))
    except json.JSONDecodeError as e:
        return FunctionAnalysis(
            function_id=u.fn_id, error=f"JSON decode: {e}", raw_response=text_out[:1500],
        )

    return FunctionAnalysis(
        function_id=u.fn_id,
        summary=str(payload.get("summary", ""))[:500],
        trust_boundary=str(payload.get("trust_boundary", ""))[:240],
        value_flow=str(payload.get("value_flow", ""))[:500],
        state_writes=list(payload.get("state_writes") or []),
        external_calls=list(payload.get("external_calls") or []),
        invariants_assumed=[str(i)[:300] for i in (payload.get("invariants_assumed") or [])][:20],
        invariants_established=[str(i)[:300] for i in (payload.get("invariants_established") or [])][:20],
        candidate_vulnerabilities=list(payload.get("candidate_vulnerabilities") or []),
        safe_observations=list(payload.get("safe_observations") or []),
        notes=str(payload.get("notes", ""))[:1000],
        raw_response=text_out[:3000],
        analyzed_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        source_hash=_hash_unit(u),
    )


# ---------------------------------------------------------------------------
# Cross-function pass
# ---------------------------------------------------------------------------


def _shared_state_pairs(units: list[FunctionUnit], analyses: dict[str, FunctionAnalysis], max_pairs: int = 50) -> list[tuple[FunctionUnit, FunctionUnit, list[str]]]:
    """Find pairs of functions in the same contract that:
      1. Share state writes (the slot intersection is non-empty), OR
      2. Share invariants (one establishes what another assumes).

    Pairs are deduped (a,b) so we don't analyze (a,b) and (b,a) separately.
    Sorted by max-severity-of-either-function then by overlap size.
    """
    # Group by contract
    by_contract: dict[str, list[FunctionUnit]] = {}
    for u in units:
        by_contract.setdefault(f"{u.file}::{u.contract}", []).append(u)

    seen_pairs: set[tuple[str, str]] = set()
    pairs: list[tuple[FunctionUnit, FunctionUnit, list[str]]] = []
    for key, group in by_contract.items():
        for i, a in enumerate(group):
            for b in group[i + 1:]:
                if a.fn_id == b.fn_id:
                    continue
                pair_key = tuple(sorted([a.fn_id, b.fn_id]))
                if pair_key in seen_pairs:
                    continue

                a_an = analyses.get(a.fn_id, FunctionAnalysis(function_id=a.fn_id))
                b_an = analyses.get(b.fn_id, FunctionAnalysis(function_id=b.fn_id))

                # 1. Shared state writes
                a_writes = {s.get("slot") for s in a_an.state_writes if isinstance(s, dict)}
                b_writes = {s.get("slot") for s in b_an.state_writes if isinstance(s, dict)}
                shared_state = list(a_writes & b_writes)

                # 2. Cross-invariant overlap: A_established ∩ B_assumed (or B_est ∩ A_ass)
                a_est = set(a_an.invariants_established)
                a_ass = set(a_an.invariants_assumed)
                b_est = set(b_an.invariants_established)
                b_ass = set(b_an.invariants_assumed)
                cross_inv = list((a_est & b_ass) | (b_est & a_ass))

                overlap = shared_state + [f"INV:{i}" for i in cross_inv]
                if not overlap:
                    continue

                seen_pairs.add(pair_key)
                pairs.append((a, b, overlap))

    sev_rank = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Info": 4, "Informational": 4}
    def score(p):
        a, b, overlap = p
        max_sev = min(
            sev_rank.get(analyses[a.fn_id].max_severity, 99) if a.fn_id in analyses else 99,
            sev_rank.get(analyses[b.fn_id].max_severity, 99) if b.fn_id in analyses else 99,
        )
        # tie-break: more overlap = more interesting pair
        return (max_sev, -len(overlap))
    pairs.sort(key=score)
    return pairs[:max_pairs]


@dataclass
class CrossFnAnalysis:
    pair_id: str
    shared_state: list = field(default_factory=list)
    interaction_kind: str = ""
    broken_invariants: list = field(default_factory=list)
    vulnerabilities: list = field(default_factory=list)
    notes: str = ""
    raw_response: str = ""
    error: str | None = None
    analyzed_at: str = ""


def analyze_cross_pair(
    a: FunctionUnit,
    b: FunctionUnit,
    shared: list[str],
    analyses: dict[str, FunctionAnalysis],
    target_root: Path,
    *,
    model: str = "opus",
    timeout_seconds: int = 600,
) -> CrossFnAnalysis:
    cl = _claude_bin()
    if not cl:
        return CrossFnAnalysis(pair_id=f"{a.fn_id}+{b.fn_id}", error="claude CLI missing")

    a_an = analyses.get(a.fn_id)
    b_an = analyses.get(b.fn_id)

    def _inv_block(an: FunctionAnalysis | None, label: str) -> str:
        if not an:
            return ""
        parts = []
        if an.invariants_assumed:
            parts.append(f"  invariants_assumed: {an.invariants_assumed}")
        if an.invariants_established:
            parts.append(f"  invariants_established: {an.invariants_established}")
        return ("\n" + "\n".join(parts)) if parts else ""

    brief = (
        f"# Cross-function pair: {a.fn_id}  +  {b.fn_id}\n\n"
        f"## Shared state: {shared}\n\n"
        f"## Function A: {a.fn_id}\n"
        f"prior single-fn analysis summary: {a_an.summary if a_an else ''}"
        f"{_inv_block(a_an, 'A')}\n"
        f"```solidity\n{_with_line_numbers(a.source, a.line_start)}\n```\n\n"
        f"## Function B: {b.fn_id}\n"
        f"prior single-fn analysis summary: {b_an.summary if b_an else ''}"
        f"{_inv_block(b_an, 'B')}\n"
        f"```solidity\n{_with_line_numbers(b.source, b.line_start)}\n```\n\n"
        f"Output ONLY the JSON described in the system prompt."
    )

    try:
        proc = subprocess.run(
            [
                cl, "-p", "--model", model,
                "--system-prompt", CROSS_FN_SYSTEM,
                "--dangerously-skip-permissions",
                "--output-format", "json",
                brief,
            ],
            capture_output=True, text=True, timeout=timeout_seconds, check=False,
        )
    except subprocess.TimeoutExpired:
        return CrossFnAnalysis(pair_id=f"{a.fn_id}+{b.fn_id}", error="timeout")
    except Exception as e:  # noqa: BLE001
        return CrossFnAnalysis(pair_id=f"{a.fn_id}+{b.fn_id}", error=f"subprocess: {e}")

    if proc.returncode != 0:
        return CrossFnAnalysis(
            pair_id=f"{a.fn_id}+{b.fn_id}",
            error=f"rc={proc.returncode}",
        )
    try:
        wrapper = json.loads(proc.stdout)
        text_out = wrapper.get("result", "") if isinstance(wrapper, dict) else proc.stdout
    except json.JSONDecodeError:
        text_out = proc.stdout
    m = re.search(r"\{.*\}", text_out, re.DOTALL)
    if not m:
        return CrossFnAnalysis(pair_id=f"{a.fn_id}+{b.fn_id}", error="unparseable", raw_response=text_out[:1000])
    try:
        payload = json.loads(m.group(0))
    except json.JSONDecodeError:
        return CrossFnAnalysis(pair_id=f"{a.fn_id}+{b.fn_id}", error="JSON decode")

    return CrossFnAnalysis(
        pair_id=str(payload.get("pair_id", f"{a.fn_id}+{b.fn_id}")),
        shared_state=list(payload.get("shared_state") or []),
        interaction_kind=str(payload.get("interaction_kind", "")),
        broken_invariants=list(payload.get("broken_invariants") or []),
        vulnerabilities=list(payload.get("vulnerabilities") or []),
        notes=str(payload.get("notes", ""))[:600],
        raw_response=text_out[:2000],
        analyzed_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    )


# ---------------------------------------------------------------------------
# Run state persistence (resumable)
# ---------------------------------------------------------------------------


def _state_path(out_dir: Path) -> Path:
    return out_dir / "deep-dive-state.json"


def _load_state(out_dir: Path) -> dict:
    p = _state_path(out_dir)
    if not p.exists():
        return {"per_fn": {}, "cross": {}, "started_at": None, "last_updated": None}
    return json.loads(p.read_text())


def _save_state(out_dir: Path, state: dict) -> None:
    state["last_updated"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    _state_path(out_dir).write_text(json.dumps(state, indent=2, default=str))


# ---------------------------------------------------------------------------
# Aggregate report
# ---------------------------------------------------------------------------


def render_report(
    target_root: Path,
    units: list[FunctionUnit],
    analyses: dict[str, FunctionAnalysis],
    cross: list[CrossFnAnalysis],
) -> str:
    """Markdown deep-dive report."""
    sev_rank = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Info": 4, "Informational": 4}
    fn_by_sev: dict[str, list[FunctionAnalysis]] = {}
    for a in analyses.values():
        s = a.max_severity
        fn_by_sev.setdefault(s, []).append(a)

    total_vulns = sum(len(a.candidate_vulnerabilities) for a in analyses.values())
    cross_vulns = sum(len(c.vulnerabilities) for c in cross)

    parts = []
    parts.append(f"# Deep-dive report — {target_root.name}")
    parts.append("")
    parts.append(f"- Generated: {datetime.now(timezone.utc).isoformat()}")
    parts.append(f"- Functions analyzed: {len(analyses)} / {len(units)}")
    parts.append(f"- Candidate vulnerabilities surfaced: {total_vulns}")
    parts.append(f"- Cross-function vulnerabilities: {cross_vulns}")
    parts.append("")

    parts.append("## Summary by max severity")
    parts.append("| Severity | Function count |")
    parts.append("| --- | ---: |")
    for sev in ("Critical", "High", "Medium", "Low", "Info", "—"):
        n = len(fn_by_sev.get(sev, []))
        if n:
            parts.append(f"| {sev} | {n} |")
    parts.append("")

    # Per-function details, sorted by max severity
    parts.append("## Per-function analyses")
    parts.append("")
    sorted_analyses = sorted(
        analyses.values(),
        key=lambda a: (sev_rank.get(a.max_severity, 99), a.function_id),
    )
    for a in sorted_analyses:
        parts.append(f"### {a.function_id} — max_sev: {a.max_severity}")
        parts.append(f"_{a.summary}_")
        parts.append("")
        if a.trust_boundary:
            parts.append(f"**Trust boundary:** {a.trust_boundary}")
        if a.value_flow:
            parts.append(f"**Value flow:** {a.value_flow}")
        if a.state_writes:
            parts.append("**State writes:** " + ", ".join(
                f"`{s.get('slot', '?')}` (when: {s.get('condition', '?')})" for s in a.state_writes
            ))
        if a.external_calls:
            parts.append("**External calls:** " + ", ".join(
                f"`{c.get('target', '?')}` ({c.get('kind','?')})"
                + (" [BEFORE state-update]" if c.get('before_state_update') else "")
                for c in a.external_calls
            ))
        if a.invariants_assumed:
            parts.append("**Assumes invariants:**")
            for inv in a.invariants_assumed:
                parts.append(f"  - {inv}")
        if a.invariants_established:
            parts.append("**Establishes invariants:**")
            for inv in a.invariants_established:
                parts.append(f"  - {inv}")
        parts.append("")
        if a.candidate_vulnerabilities:
            parts.append("#### Candidate vulnerabilities")
            for v in a.candidate_vulnerabilities:
                parts.append(f"- **[{v.get('severity','?')}] [{v.get('confidence','?')}] {v.get('title','?')}**")
                parts.append(f"  - precondition: {v.get('precondition','?')}")
                parts.append(f"  - impact: {v.get('impact','?')}")
                if v.get("blocked_by_solc_08_checks"):
                    parts.append(f"  - blocked by solc 0.8 checks: yes (downgrade severity)")
                if v.get("poc_sketch"):
                    parts.append(f"  - PoC sketch:")
                    parts.append("    ```")
                    parts.append("    " + str(v["poc_sketch"]).replace("\n", "\n    ")[:1200])
                    parts.append("    ```")
        if a.safe_observations:
            parts.append("#### Safe observations")
            for s in a.safe_observations[:6]:
                parts.append(f"- {s}")
        parts.append("")

    # Aggregated invariants — the contract's "rules of the road"
    all_assumed: dict[str, set[str]] = {}
    all_established: dict[str, set[str]] = {}
    for a in analyses.values():
        for inv in a.invariants_assumed:
            all_assumed.setdefault(inv, set()).add(a.function_id)
        for inv in a.invariants_established:
            all_established.setdefault(inv, set()).add(a.function_id)
    if all_assumed or all_established:
        parts.append("## Aggregated invariants (across the audited surface)")
        parts.append("")
        if all_established:
            parts.append("### Established (postconditions on success)")
            for inv, fns in sorted(all_established.items(), key=lambda kv: -len(kv[1])):
                parts.append(f"- `{inv}`  _({len(fns)} fn)_")
                if len(fns) <= 4:
                    for fn in sorted(fns):
                        parts.append(f"  - {fn}")
            parts.append("")
        if all_assumed:
            parts.append("### Assumed (preconditions — fuzz-target candidates)")
            for inv, fns in sorted(all_assumed.items(), key=lambda kv: -len(kv[1])):
                parts.append(f"- `{inv}`  _({len(fns)} fn)_")
                if len(fns) <= 4:
                    for fn in sorted(fns):
                        parts.append(f"  - {fn}")
            parts.append("")

    if cross:
        parts.append("## Cross-function interactions")
        for c in cross:
            has_findings = c.vulnerabilities or c.broken_invariants or c.error
            if not has_findings:
                continue
            parts.append(f"### {c.pair_id}")
            parts.append(f"shared: {', '.join(c.shared_state)} | kind: {c.interaction_kind}")
            if c.broken_invariants:
                parts.append("**Invariant breakages:**")
                for bi in c.broken_invariants:
                    parts.append(
                        f"  - `{bi.get('invariant','?')}` broken by "
                        f"`{bi.get('broken_by','?')}` — {bi.get('how','?')}"
                    )
            for v in c.vulnerabilities:
                parts.append(f"- **[{v.get('severity','?')}] {v.get('title','?')}**")
                parts.append(f"  - sequence: {v.get('sequence','?')}")
                parts.append(f"  - impact: {v.get('impact','?')}")
                if v.get("poc_sketch"):
                    parts.append(f"  - PoC sketch: `{str(v['poc_sketch'])[:400]}`")
            parts.append("")

    return "\n".join(parts)


def render_invariants(
    target_root: Path,
    analyses: dict[str, FunctionAnalysis],
    cross: list[CrossFnAnalysis],
) -> str:
    """Render a focused `invariants.md` doc — the contract's rules of the road.

    This is the artifact you hand to a fuzzer, paste into an audit report's
    "preconditions/postconditions" section, or use as the spec for invariant
    tests.
    """
    parts: list[str] = []
    parts.append(f"# Invariants — {target_root.name}")
    parts.append("")
    parts.append(f"_Auto-extracted from deep-dive analysis of "
                 f"{len(analyses)} function(s)._")
    parts.append("")

    # Aggregate
    by_established: dict[str, set[str]] = {}
    by_assumed: dict[str, set[str]] = {}
    for a in analyses.values():
        for inv in a.invariants_established:
            by_established.setdefault(inv, set()).add(a.function_id)
        for inv in a.invariants_assumed:
            by_assumed.setdefault(inv, set()).add(a.function_id)

    breakages = []
    for c in cross:
        for bi in c.broken_invariants:
            breakages.append({**bi, "pair": c.pair_id})

    if not by_established and not by_assumed and not breakages:
        parts.append("_No explicit invariants surfaced — the analyzer didn't "
                     "extract any. (This may indicate a too-shallow analysis "
                     "or a function set with no shared state.)_")
        return "\n".join(parts)

    parts.append("## Postconditions established (on successful return)")
    parts.append("")
    if by_established:
        for inv, fns in sorted(by_established.items(), key=lambda kv: -len(kv[1])):
            parts.append(f"### `{inv}`")
            parts.append(f"_Established by {len(fns)} function(s):_")
            for fn in sorted(fns):
                parts.append(f"  - `{fn}`")
            parts.append("")
    else:
        parts.append("_(none surfaced)_")
        parts.append("")

    parts.append("## Preconditions assumed (potential fuzz targets)")
    parts.append("")
    if by_assumed:
        for inv, fns in sorted(by_assumed.items(), key=lambda kv: -len(kv[1])):
            parts.append(f"### `{inv}`")
            parts.append(f"_Assumed by {len(fns)} function(s):_")
            for fn in sorted(fns):
                parts.append(f"  - `{fn}`")
            parts.append("")
    else:
        parts.append("_(none surfaced)_")
        parts.append("")

    parts.append("## Detected invariant breakages (cross-function)")
    parts.append("")
    if breakages:
        for bi in breakages:
            parts.append(f"- **`{bi.get('invariant', '?')}`**")
            parts.append(f"  - Broken by: `{bi.get('broken_by', '?')}` in pair `{bi.get('pair', '?')}`")
            parts.append(f"  - How: {bi.get('how', '?')}")
        parts.append("")
    else:
        parts.append("_(none detected — cross-fn pass found no breakages)_")
        parts.append("")

    parts.append("## Suggested next steps")
    parts.append("")
    parts.append("- Translate `Established` postconditions into Foundry invariant "
                 "tests (`function invariant_X() public`).")
    parts.append("- Use `Assumed` preconditions as fuzz boundaries — values that "
                 "violate them should never reach the function.")
    parts.append("- Investigate every `breakage` entry as a candidate bug.")

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Top-level orchestrator
# ---------------------------------------------------------------------------


def run_deep_dive(
    target_root: Path,
    *,
    out_dir: Path | None = None,
    scope: Path | None = None,
    model: str = "opus",
    max_functions: int | None = None,
    skip_cross: bool = False,
    max_cross_pairs: int = 30,
    progress_callback=None,
    resume: bool = True,
) -> Path:
    """End-to-end deep dive. Returns the report path."""
    target_root = target_root.resolve()
    if out_dir is None:
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        out_dir = REPO_ROOT / "audits" / f"deep-dive-{target_root.name}-{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    state = _load_state(out_dir) if resume else {"per_fn": {}, "cross": {}, "started_at": None}
    if not state.get("started_at"):
        state["started_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    # Decompose
    units = decompose(target_root, scope=scope)
    if max_functions:
        units = units[:max_functions]
    if progress_callback:
        progress_callback("decompose", 0, len(units), f"{len(units)} functions to analyze")

    # Persist decomposition for inspection
    (out_dir / "decomposition.jsonl").write_text(
        "\n".join(json.dumps({k: v for k, v in asdict(u).items() if k != "source"}) for u in units)
    )

    # Per-function pass (resumable)
    analyses: dict[str, FunctionAnalysis] = {
        k: FunctionAnalysis(**v) for k, v in state["per_fn"].items()
    }
    for i, u in enumerate(units):
        if u.fn_id in analyses and analyses[u.fn_id].source_hash == _hash_unit(u):
            if progress_callback:
                progress_callback("per_fn", i, len(units), f"cached: {u.fn_id}")
            continue
        if progress_callback:
            progress_callback("per_fn", i, len(units), f"analyzing: {u.fn_id}")
        a = analyze_function(u, target_root, model=model)
        analyses[a.function_id] = a
        state["per_fn"][a.function_id] = asdict(a)
        _save_state(out_dir, state)

    # Cross-function pass
    cross_results: list[CrossFnAnalysis] = [
        CrossFnAnalysis(**v) for v in state["cross"].values()
    ]
    if not skip_cross:
        pairs = _shared_state_pairs(units, analyses, max_pairs=max_cross_pairs)
        for i, (a_u, b_u, shared) in enumerate(pairs):
            key = f"{a_u.fn_id}+{b_u.fn_id}"
            if key in state["cross"]:
                if progress_callback:
                    progress_callback("cross", i, len(pairs), f"cached: {key}")
                continue
            if progress_callback:
                progress_callback("cross", i, len(pairs), f"analyzing: {key}")
            c = analyze_cross_pair(a_u, b_u, shared, analyses, target_root, model=model)
            cross_results.append(c)
            state["cross"][key] = asdict(c)
            _save_state(out_dir, state)

    # Render aggregate report
    report = render_report(target_root, units, analyses, cross_results)
    report_path = out_dir / "deep-dive-report.md"
    report_path.write_text(report)

    # Side-output: invariants.md — a focused doc of the contract's rules
    invariants_md = render_invariants(target_root, analyses, cross_results)
    (out_dir / "invariants.md").write_text(invariants_md)

    # Also dump JSONL for tooling
    (out_dir / "per-function.jsonl").write_text(
        "\n".join(json.dumps(asdict(a)) for a in analyses.values())
    )
    (out_dir / "cross-function.jsonl").write_text(
        "\n".join(json.dumps(asdict(c)) for c in cross_results)
    )

    return report_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", help="Path to a Solidity project root (or single file).")
    parser.add_argument("--scope", help="Restrict to .sol under this subpath.")
    parser.add_argument("--out", help="Output dir (default: audits/deep-dive-<name>-<ts>).")
    parser.add_argument("--model", default="opus")
    parser.add_argument("--max-functions", type=int, default=None)
    parser.add_argument("--skip-cross", action="store_true")
    parser.add_argument("--max-cross-pairs", type=int, default=30)
    parser.add_argument("--no-resume", action="store_true", help="Don't load previous state; start fresh.")
    args = parser.parse_args(argv)

    target = Path(args.target).expanduser().resolve()
    scope = Path(args.scope).expanduser().resolve() if args.scope else None
    out_dir = Path(args.out).expanduser().resolve() if args.out else None

    def progress(phase, idx, total, msg):
        print(f"[{phase} {idx + 1}/{total}] {msg}")

    report_path = run_deep_dive(
        target,
        out_dir=out_dir,
        scope=scope,
        model=args.model,
        max_functions=args.max_functions,
        skip_cross=args.skip_cross,
        max_cross_pairs=args.max_cross_pairs,
        progress_callback=progress,
        resume=not args.no_resume,
    )
    print(f"\nReport: {report_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
