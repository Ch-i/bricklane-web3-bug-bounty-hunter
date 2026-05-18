"""`w3s scrutinize <target>` — the maximum-depth analysis pipeline.

Runs every analysis layer in sequence on ONE target. This is the
"spend-a-whole-day-on-one-subject" workflow:

  1. prep                   — static analyzers (slither + aderyn + forge cov)
  2. audit (multimodel)     — Claude + Codex auditors + reconciler with PoCs
  3. deep-dive (per-fn)     — every function gets its own Opus pass
  4. cross-fn deep-dive     — paired interaction analysis on overlapping state
  5. materialize-pocs       — convert deep-dive poc_sketches into forge tests
  6. filter pass            — judge every finding ACCEPT/DOWNGRADE/REJECT
  7. master report          — aggregate everything into one markdown doc

Each phase is resumable — state is persisted so a long run can be
interrupted + continued. Default mode runs the WHOLE pipeline; you can
skip individual phases with --skip-audit / --skip-deep-dive / etc. for
re-runs or cost control.

Pro Max x200 cost estimate for a 20-function target:
  audit multimodel    ~3 messages
  deep-dive per-fn    ~20 messages
  deep-dive cross-fn  ~10 messages
  materialize-pocs    ~5-10 messages
  filter pass         ~10 messages
  TOTAL               ~50 messages, ~30-60 min wall clock

For a 100-function target, scale linearly: ~150 messages, ~3 hours.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table

from harness import candidates as cand_store
from harness import deep_dive
from harness import deep_dive_poc
from harness.corpus import REPO_ROOT
from harness.orchestrator import Orchestrator, OrchestratorOptions

console = Console()


def _load_state(scrutinize_dir: Path) -> dict:
    p = scrutinize_dir / "state.json"
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text())
    except (json.JSONDecodeError, OSError):
        return {}


def _save_state(scrutinize_dir: Path, partial: dict) -> None:
    """Merge new keys into the on-disk state file. Each phase persists its own
    `<phase>_run_dir` / path; subsequent re-runs detect them and skip the phase."""
    p = scrutinize_dir / "state.json"
    current = _load_state(scrutinize_dir)
    current.update(partial)
    current["last_updated"] = datetime.now(timezone.utc).isoformat()
    p.write_text(json.dumps(current, indent=2))


def _section(title: str, n: int, total: int, elapsed: int) -> None:
    console.print()
    console.print(Rule(
        f"[bold cyan][{n}/{total}] {title}[/bold cyan] [dim]· {elapsed}s elapsed[/dim]",
        style="cyan",
    ))


def _master_report(
    *,
    target: Path,
    scrutinize_dir: Path,
    audit_run_dir: Path | None,
    deep_dive_run_dir: Path | None,
    filter_results_path: Path | None,
    materialized_path: Path | None,
    elapsed_s: int,
) -> Path:
    """Aggregate all phases' outputs into a single navigable markdown doc."""

    parts: list[str] = []
    parts.append(f"# Scrutinize report — {target.name}")
    parts.append("")
    parts.append(f"- Generated: {datetime.now(timezone.utc).isoformat()}")
    parts.append(f"- Target: `{target}`")
    parts.append(f"- Total wall time: {elapsed_s}s ({elapsed_s // 60}m {elapsed_s % 60}s)")
    parts.append("")

    # Phase 1: Audit summary
    parts.append("## 1. Multi-model audit")
    if audit_run_dir and (audit_run_dir / "report.md").exists():
        try:
            findings = json.loads((audit_run_dir / "findings.json").read_text())
            findings = findings if isinstance(findings, list) else findings.get("findings", [])
            sev_counts: dict[str, int] = {}
            poc_counts: dict[str, int] = {}
            for f in findings:
                sev_counts[f.get("severity", "?")] = sev_counts.get(f.get("severity", "?"), 0) + 1
                poc_counts[f.get("poc_status", "not-attempted")] = poc_counts.get(f.get("poc_status", "not-attempted"), 0) + 1
            parts.append(f"Run dir: `{audit_run_dir}`")
            parts.append(f"Findings: {len(findings)} ({', '.join(f'{k}={v}' for k,v in sev_counts.items())})")
            parts.append(f"PoCs: {', '.join(f'{k}={v}' for k,v in poc_counts.items())}")
            parts.append("")
            parts.append("See full audit report: " + f"`{audit_run_dir / 'report.md'}`")
        except Exception as e:  # noqa: BLE001
            parts.append(f"_(audit summary failed: {e})_")
    else:
        parts.append("_(skipped or failed)_")
    parts.append("")

    # Phase 2: Deep-dive summary
    parts.append("## 2. Deep-dive (per-function + cross-function)")
    if deep_dive_run_dir and (deep_dive_run_dir / "deep-dive-report.md").exists():
        try:
            pf_path = deep_dive_run_dir / "per-function.jsonl"
            pf_lines = pf_path.read_text().splitlines() if pf_path.exists() else []
            n_fn = len(pf_lines)
            total_vulns = 0
            for line in pf_lines:
                try:
                    fn = json.loads(line)
                    total_vulns += len(fn.get("candidate_vulnerabilities") or [])
                except Exception:  # noqa: BLE001
                    continue
            cross_path = deep_dive_run_dir / "cross-function.jsonl"
            cross_vulns = 0
            if cross_path.exists():
                for line in cross_path.read_text().splitlines():
                    try:
                        c = json.loads(line)
                        cross_vulns += len(c.get("vulnerabilities") or [])
                    except Exception:  # noqa: BLE001
                        continue
            parts.append(f"Run dir: `{deep_dive_run_dir}`")
            parts.append(f"Functions analyzed: {n_fn}")
            parts.append(f"Candidate vulnerabilities (per-fn): {total_vulns}")
            parts.append(f"Cross-function vulnerabilities: {cross_vulns}")
            parts.append("")
            parts.append("See full deep-dive report: " + f"`{deep_dive_run_dir / 'deep-dive-report.md'}`")
        except Exception as e:  # noqa: BLE001
            parts.append(f"_(deep-dive summary failed: {e})_")
    else:
        parts.append("_(skipped or failed)_")
    parts.append("")

    # Phase 3: Materialized PoCs
    parts.append("## 3. Materialized PoCs (verified executability)")
    if materialized_path and materialized_path.exists():
        try:
            data = json.loads(materialized_path.read_text())
            if data:
                by_status: dict[str, int] = {}
                for f in data:
                    by_status[f.get("poc_status", "not-attempted")] = by_status.get(f.get("poc_status", "not-attempted"), 0) + 1
                parts.append(f"Materialized: {len(data)} candidates")
                parts.append(f"  by status: {', '.join(f'{k}={v}' for k,v in by_status.items())}")
                parts.append("")
                reproduced = [f for f in data if f.get("poc_status") == "reproduced"]
                if reproduced:
                    parts.append("### ✓ Reproduced candidates")
                    for f in reproduced:
                        parts.append(f"- **[{f.get('severity')}] {f.get('title','')[:80]}**")
                        if f.get("poc_artifacts", {}).get("test_path"):
                            parts.append(f"  - test: `{f['poc_artifacts']['test_path']}`")
            else:
                parts.append("_(no candidates met the materialization severity threshold)_")
        except Exception as e:  # noqa: BLE001
            parts.append(f"_(materialization summary failed: {e})_")
    else:
        parts.append("_(skipped)_")
    parts.append("")

    # Phase 4: Filter verdicts
    parts.append("## 4. Filter verdicts (Mythos-style)")
    if filter_results_path and filter_results_path.exists():
        try:
            data = json.loads(filter_results_path.read_text())
            data = data if isinstance(data, list) else data.get("findings", [])
            by_verdict: dict[str, int] = {}
            for f in data:
                v = (f.get("filter") or {}).get("verdict", "—")
                by_verdict[v] = by_verdict.get(v, 0) + 1
            parts.append(f"Findings judged: {len(data)}")
            parts.append(f"  verdicts: {', '.join(f'{k}={v}' for k,v in by_verdict.items())}")
            parts.append("")
            accepts = [f for f in data if (f.get("filter") or {}).get("verdict") == "ACCEPT"]
            if accepts:
                parts.append("### Submission-ready (ACCEPT)")
                for f in accepts[:20]:
                    parts.append(f"- **[{f.get('severity')}] {f.get('title','')[:80]}**")
                    rationale = (f.get("filter") or {}).get("rationale", "")[:120]
                    if rationale:
                        parts.append(f"  - judge: {rationale}")
        except Exception as e:  # noqa: BLE001
            parts.append(f"_(filter summary failed: {e})_")
    else:
        parts.append("_(skipped)_")
    parts.append("")

    parts.append("## Next steps")
    parts.append("")
    parts.append("- Review the ACCEPT'd findings above and pick which to submit.")
    parts.append("- `w3s submit <run-dir> --candidate-id <id> --platforms c4 sherlock` to export per-platform templates.")
    parts.append("- Track submission outcomes via `w3s` submissions log.")

    out_path = scrutinize_dir / "scrutinize-report.md"
    out_path.write_text("\n".join(parts))
    return out_path


def estimate_plan(
    target_path: Path,
    scope: str | None,
    *,
    skip_audit: bool,
    skip_deep_dive: bool,
    skip_cross_fn: bool,
    skip_materialize: bool,
    skip_filter: bool,
    audit_multimodel: bool,
    audit_with_pocs: bool,
    deep_dive_max_functions: int | None,
) -> dict:
    """Decompose the target + estimate message count + wall time.

    Returns a dict suitable for human inspection or budget gating.
    """
    units = deep_dive.decompose(
        target_path,
        scope=Path(scope).resolve() if scope else None,
    ) if target_path.exists() else []
    if deep_dive_max_functions:
        units = units[:deep_dive_max_functions]

    n_fn = len(units)
    n_pairs = min(30, n_fn * (n_fn - 1) // 2)  # cap matches default max_cross_pairs

    audit_msgs = 0
    if not skip_audit:
        audit_msgs = 3 if audit_multimodel else 1  # claude + codex + reconciler vs single
        if audit_with_pocs:
            audit_msgs += 2  # PoC scaffolding pass

    dd_msgs = 0 if skip_deep_dive else n_fn
    cross_msgs = 0 if (skip_deep_dive or skip_cross_fn) else n_pairs
    mat_msgs = 0
    if not skip_materialize and not skip_deep_dive:
        # rough: 1 per High/Critical candidate; assume ~25% of functions have one
        mat_msgs = max(1, n_fn // 4)
    filter_msgs = 0
    if not skip_filter and not skip_audit:
        filter_msgs = max(2, audit_msgs * 2)  # ~one per finding; audit findings count

    total = audit_msgs + dd_msgs + cross_msgs + mat_msgs + filter_msgs

    # Rough wall-time estimate: Opus messages average 40-90s on Pro Max
    wall_s_low = total * 40
    wall_s_high = total * 90

    return {
        "function_count": n_fn,
        "pair_count": n_pairs,
        "messages": {
            "audit": audit_msgs,
            "deep_dive_per_fn": dd_msgs,
            "deep_dive_cross_fn": cross_msgs,
            "materialize": mat_msgs,
            "filter": filter_msgs,
            "total": total,
        },
        "wall_time_estimate_s": (wall_s_low, wall_s_high),
        "functions_preview": [
            {"id": u.fn_id, "vis": u.visibility, "lines": u.line_end - u.line_start + 1}
            for u in units[:25]
        ],
    }


def _print_plan(plan: dict) -> None:
    """Pretty-print the estimate_plan output for --dry-run."""
    n = plan["function_count"]
    p = plan["pair_count"]
    msgs = plan["messages"]
    lo, hi = plan["wall_time_estimate_s"]
    body = (
        f"Functions to analyze:    {n}\n"
        f"Cross-fn pairs:          {p}\n"
        f"\n"
        f"LLM message budget:\n"
        f"  audit:                 {msgs['audit']}\n"
        f"  deep-dive per-fn:      {msgs['deep_dive_per_fn']}\n"
        f"  deep-dive cross-fn:    {msgs['deep_dive_cross_fn']}\n"
        f"  materialize-pocs:      {msgs['materialize']}\n"
        f"  filter:                {msgs['filter']}\n"
        f"  ──────────────\n"
        f"  TOTAL:                 {msgs['total']}\n"
        f"\n"
        f"Wall time estimate: {lo // 60}–{hi // 60} min  ({lo}–{hi}s)\n"
    )
    console.print(Panel(body, title="scrutinize dry-run plan", border_style="cyan"))
    if plan["functions_preview"]:
        console.print("\n[cyan]First functions (preview):[/cyan]")
        for f in plan["functions_preview"]:
            console.print(f"  [dim]{f['vis']:>10}[/dim]  {f['id']}  [dim]({f['lines']}L)[/dim]")
        if n > len(plan["functions_preview"]):
            console.print(f"  ... and {n - len(plan['functions_preview'])} more")


def scrutinize(
    target: str,
    *,
    chain: str = "mainnet",
    scope: str | None = None,
    out_dir: Path | None = None,
    skip_audit: bool = False,
    skip_deep_dive: bool = False,
    skip_cross_fn: bool = False,
    skip_materialize: bool = False,
    skip_filter: bool = False,
    audit_multimodel: bool = True,
    audit_with_pocs: bool = True,
    deep_dive_max_functions: int | None = None,
    materialize_min_severity: str = "High",
    model: str = "opus",
    dry_run: bool = False,
) -> Path | None:
    """Run the maximum-depth pipeline on one target. Returns master report path
    (or None for dry-run)."""
    target_path = Path(target).expanduser().resolve()

    if dry_run:
        plan = estimate_plan(
            target_path, scope,
            skip_audit=skip_audit, skip_deep_dive=skip_deep_dive,
            skip_cross_fn=skip_cross_fn, skip_materialize=skip_materialize,
            skip_filter=skip_filter, audit_multimodel=audit_multimodel,
            audit_with_pocs=audit_with_pocs,
            deep_dive_max_functions=deep_dive_max_functions,
        )
        _print_plan(plan)
        return None

    started = time.monotonic()

    target_path = Path(target).expanduser().resolve()

    # If user passed --out pointing at an existing scrutinize dir, resume from it.
    # Otherwise create a fresh timestamped dir.
    if out_dir and out_dir.exists() and (out_dir / "state.json").exists():
        scrutinize_dir = out_dir
        prior_state = _load_state(scrutinize_dir)
        console.print(f"[cyan]Resuming scrutinize from {scrutinize_dir}[/cyan]")
    else:
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        name = target_path.name if target_path.exists() else target.replace("/", "_").replace(":", "_")[:50]
        scrutinize_dir = (out_dir or (REPO_ROOT / "audits" / f"scrutinize-{name}-{ts}"))
        scrutinize_dir.mkdir(parents=True, exist_ok=True)
        prior_state = {}

    total_phases = 4
    n = 0

    audit_run_dir: Path | None = (
        Path(prior_state["audit_run_dir"]) if prior_state.get("audit_run_dir") else None
    )
    deep_dive_run_dir: Path | None = (
        Path(prior_state["deep_dive_run_dir"]) if prior_state.get("deep_dive_run_dir") else None
    )
    filter_results_path: Path | None = (
        Path(prior_state["filter_results_path"]) if prior_state.get("filter_results_path") else None
    )
    materialized_path: Path | None = (
        Path(prior_state["materialized_path"]) if prior_state.get("materialized_path") else None
    )

    # === Phase 1: Audit ===
    audit_already_done = audit_run_dir and audit_run_dir.exists() and (audit_run_dir / "findings.json").exists()
    if not skip_audit and not audit_already_done:
        n += 1
        _section("MULTI-MODEL AUDIT", n, total_phases, int(time.monotonic() - started))
        opts = OrchestratorOptions(
            target=str(target_path),
            chain=chain,
            scope=scope,
            model=model,
            with_pocs=audit_with_pocs,
        )
        orch = Orchestrator(opts)
        if audit_multimodel:
            orch.run_multimodel()
        else:
            orch.run_single()
        if orch.run_dir:
            audit_run_dir = orch.run_dir
            _save_state(scrutinize_dir, {"audit_run_dir": str(audit_run_dir)})
    elif audit_already_done:
        _section("MULTI-MODEL AUDIT (cached)", 1, total_phases, int(time.monotonic() - started))
        console.print(f"[dim]Using prior audit: {audit_run_dir}[/dim]")

    # === Phase 2: Deep-dive (per-fn + cross-fn) ===
    dd_already_done = (
        deep_dive_run_dir and deep_dive_run_dir.exists()
        and (deep_dive_run_dir / "deep-dive-report.md").exists()
    )
    if not skip_deep_dive and not dd_already_done:
        n += 1
        _section("DEEP-DIVE (per-function + cross-function)", n, total_phases, int(time.monotonic() - started))

        def dd_progress(phase, idx, total, msg):
            console.print(f"[cyan][{phase} {idx + 1}/{total}][/cyan] {msg}")

        report_path = deep_dive.run_deep_dive(
            target_path,
            out_dir=scrutinize_dir / "deep-dive",
            scope=Path(scope).resolve() if scope else None,
            model=model,
            max_functions=deep_dive_max_functions,
            skip_cross=skip_cross_fn,
            progress_callback=dd_progress,
        )
        deep_dive_run_dir = report_path.parent
        _save_state(scrutinize_dir, {"deep_dive_run_dir": str(deep_dive_run_dir)})
    elif dd_already_done:
        _section("DEEP-DIVE (cached)", 2, total_phases, int(time.monotonic() - started))
        console.print(f"[dim]Using prior deep-dive: {deep_dive_run_dir}[/dim]")

    # === Phase 3: Materialize PoCs ===
    mat_already_done = materialized_path and materialized_path.exists()
    if not skip_materialize and deep_dive_run_dir and not mat_already_done:
        n += 1
        _section("MATERIALIZE POCS (deep-dive sketches → forge tests)", n, total_phases, int(time.monotonic() - started))

        def mat_progress(phase, idx, total, msg):
            console.print(f"[cyan][{phase} {idx}/{total}][/cyan] {msg}")

        try:
            materialized_path = deep_dive_poc.materialize_for_run(
                deep_dive_run_dir,
                target_path,
                min_severity=materialize_min_severity,
                model=model,
                progress_callback=mat_progress,
            )
            _save_state(scrutinize_dir, {"materialized_path": str(materialized_path)})
        except Exception as e:  # noqa: BLE001
            console.print(f"[yellow]Materialize failed: {e}[/yellow]")
    elif mat_already_done:
        _section("MATERIALIZE POCS (cached)", 3, total_phases, int(time.monotonic() - started))
        console.print(f"[dim]Using prior materialization: {materialized_path}[/dim]")

    # === Phase 4: Filter pass on combined audit + materialized findings ===
    if not skip_filter and audit_run_dir:
        n += 1
        _section("FILTER (Mythos-style ACCEPT/DOWNGRADE/REJECT)", n, total_phases, int(time.monotonic() - started))
        from harness import filter_agent

        # Read findings.json from audit; optionally merge materialized
        all_findings: list[dict] = []
        af = audit_run_dir / "findings.json"
        if af.exists():
            data = json.loads(af.read_text())
            all_findings.extend(data if isinstance(data, list) else data.get("findings", []))
        if materialized_path and materialized_path.exists():
            mat_data = json.loads(materialized_path.read_text())
            all_findings.extend(mat_data)

        # Also pull HIGH-severity deep-dive candidates that didn't materialize
        # — they represent the analyzer's best hits and the filter should judge
        # them too, not just the audit findings.
        if deep_dive_run_dir and (deep_dive_run_dir / "per-function.jsonl").exists():
            sev_rank = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Info": 4}
            min_rank = sev_rank.get("High", 1)
            for line in (deep_dive_run_dir / "per-function.jsonl").read_text().splitlines():
                if not line.strip():
                    continue
                try:
                    fn = json.loads(line)
                except json.JSONDecodeError:
                    continue
                fn_file = fn.get("function_id", "").split("::")[0] or "?"
                for v in (fn.get("candidate_vulnerabilities") or []):
                    if sev_rank.get(v.get("severity"), 99) > min_rank:
                        continue
                    # Shape it as a Finding-like dict so filter_agent treats it uniformly
                    all_findings.append({
                        "title": v.get("title", "?"),
                        "severity": v.get("severity"),
                        "location": [{"file": fn_file, "line_start": 1}],
                        "description": v.get("description", "") or v.get("title", "?"),
                        "impact": v.get("impact", "?"),
                        "recommendation": "(see deep-dive report)",
                        "citations": [],
                        "novel": True,
                        "confidence": v.get("confidence", "medium"),
                        "discovered_by": "claude-deep-dive",
                        "poc_status": "not-attempted",
                    })

        # Also pull CROSS-FUNCTION vulnerabilities — these are often the
        # highest-value bugs (multi-fn reentrancy, invariant violations) that
        # only emerge from the pair-wise pass.
        if deep_dive_run_dir and (deep_dive_run_dir / "cross-function.jsonl").exists():
            sev_rank = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Info": 4}
            for line in (deep_dive_run_dir / "cross-function.jsonl").read_text().splitlines():
                if not line.strip():
                    continue
                try:
                    pair = json.loads(line)
                except json.JSONDecodeError:
                    continue
                pair_id = pair.get("pair_id", "?+?")
                # Use the first function's file as the location anchor
                first_fn = pair_id.split("+")[0] if "+" in pair_id else pair_id
                pair_file = first_fn.split("::")[0] or "?"
                for v in (pair.get("vulnerabilities") or []):
                    if sev_rank.get(v.get("severity"), 99) > 1:  # High threshold
                        continue
                    all_findings.append({
                        "title": f"[Cross-fn] {v.get('title', '?')}",
                        "severity": v.get("severity"),
                        "location": [{"file": pair_file, "line_start": 1}],
                        "description": (
                            f"Pair: {pair_id}\n"
                            f"Sequence: {v.get('sequence', '?')}\n"
                            f"{v.get('description', '') or v.get('title', '?')}"
                        ),
                        "impact": v.get("impact", "?"),
                        "recommendation": "(see deep-dive report cross-fn section)",
                        "citations": [],
                        "novel": True,
                        "confidence": v.get("confidence", "medium"),
                        "discovered_by": "claude-deep-dive-cross-fn",
                        "poc_status": "not-attempted",
                    })
                # Also: each broken_invariant entry should be evaluated
                for bi in (pair.get("broken_invariants") or []):
                    all_findings.append({
                        "title": f"[Invariant break] {bi.get('invariant', '?')[:80]}",
                        "severity": "High",  # invariant breakage defaults High
                        "location": [{"file": pair_file, "line_start": 1}],
                        "description": (
                            f"Pair: {pair_id}\n"
                            f"Invariant: {bi.get('invariant', '?')}\n"
                            f"Broken by: {bi.get('broken_by', '?')}\n"
                            f"How: {bi.get('how', '?')}"
                        ),
                        "impact": "Invariant breakage — see broken_by + how fields.",
                        "recommendation": "(see deep-dive invariants.md)",
                        "citations": [],
                        "novel": True,
                        "confidence": "medium",
                        "discovered_by": "claude-deep-dive-invariants",
                        "poc_status": "not-attempted",
                    })

        # Dedup by title (loose)
        seen: set[str] = set()
        deduped = []
        for f in all_findings:
            title = f.get("title", "")
            if title in seen:
                continue
            seen.add(title)
            deduped.append(f)

        filter_results_path = scrutinize_dir / "filter-verdicts.json"
        filter_results_path.write_text(json.dumps(deduped, indent=2))

        target_root = audit_run_dir.parent / "onchain-source" if (audit_run_dir.parent / "onchain-source").exists() else target_path
        try:
            results = filter_agent.filter_findings(deduped, target_root, model=model)
            filter_results_path.write_text(json.dumps(deduped, indent=2))
            _save_state(scrutinize_dir, {"filter_results_path": str(filter_results_path)})
            for f, v in results:
                sym = {"ACCEPT": "✓", "DOWNGRADE": "↓", "REJECT": "✗", "ERROR": "!"}[v.verdict]
                console.print(f"  {sym} [{v.verdict:9s}] {v.finding_title[:60]:60s} — {v.rationale[:60]}")
        except Exception as e:  # noqa: BLE001
            console.print(f"[yellow]Filter failed: {e}[/yellow]")

    elapsed = int(time.monotonic() - started)
    report_path = _master_report(
        target=target_path,
        scrutinize_dir=scrutinize_dir,
        audit_run_dir=audit_run_dir,
        deep_dive_run_dir=deep_dive_run_dir,
        filter_results_path=filter_results_path,
        materialized_path=materialized_path,
        elapsed_s=elapsed,
    )

    console.print()
    console.print(Panel(
        f"Master report: {report_path}\n"
        f"Total wall time: {elapsed}s ({elapsed // 60}m {elapsed % 60}s)\n"
        f"Phases run: {n}",
        title="scrutinize complete",
        border_style="green",
    ))
    return report_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target")
    parser.add_argument("--chain", default="mainnet")
    parser.add_argument("--scope")
    parser.add_argument("--out")
    parser.add_argument("--skip-audit", action="store_true")
    parser.add_argument("--skip-deep-dive", action="store_true")
    parser.add_argument("--skip-cross-fn", action="store_true")
    parser.add_argument("--skip-materialize", action="store_true")
    parser.add_argument("--skip-filter", action="store_true")
    parser.add_argument("--single-model", action="store_true",
                        help="Audit phase uses single model only (no codex + reconciler).")
    parser.add_argument("--no-audit-pocs", action="store_true",
                        help="Audit phase skips its own foundry_poc scaffolding (deep-dive still does).")
    parser.add_argument("--max-functions", type=int, default=None)
    parser.add_argument("--materialize-min-severity", default="High",
                        choices=["Critical", "High", "Medium"])
    parser.add_argument("--model", default="opus")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print the decomposition + estimated message + wall-time budget. "
                             "No LLM calls. Use this to preview cost before committing.")
    args = parser.parse_args(argv)

    out_dir = Path(args.out).expanduser().resolve() if args.out else None

    scrutinize(
        args.target,
        chain=args.chain,
        scope=args.scope,
        out_dir=out_dir,
        skip_audit=args.skip_audit,
        skip_deep_dive=args.skip_deep_dive,
        skip_cross_fn=args.skip_cross_fn,
        skip_materialize=args.skip_materialize,
        skip_filter=args.skip_filter,
        audit_multimodel=not args.single_model,
        audit_with_pocs=not args.no_audit_pocs,
        deep_dive_max_functions=args.max_functions,
        materialize_min_severity=args.materialize_min_severity,
        model=args.model,
        dry_run=args.dry_run,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
