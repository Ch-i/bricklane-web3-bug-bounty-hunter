"""Rich-based terminal UI for browsing web3Sentinel audit runs.

Like AFL's status display or IDA's listing window: an at-a-glance view of
what the harness has discovered, with deep-dive panels for individual
findings.

Commands:
    python -m harness.tui list                  # table of recent audit runs
    python -m harness.tui show <run-dir>        # detailed view of one audit
    python -m harness.tui findings <run-dir>    # findings table only
    python -m harness.tui status <run-dir>      # live view (polls run dir)

Or via the installed entry point (post-`uv sync`):
    w3s list
    w3s show audits/dvd-...

All views are pure rich rendering — no curses, no event loop. The status
view does a poll-redraw cycle via rich.live.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

from rich.columns import Columns
from rich.console import Console, Group
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from harness.corpus import REPO_ROOT

console = Console()

SEVERITY_STYLE = {
    "Critical": "bold red",
    "High": "red",
    "Medium": "yellow",
    "Low": "blue",
    "Informational": "cyan",
    "Gas": "dim",
}

POC_STYLE = {
    "reproduced": ("✓", "bold green"),
    "unconfirmed": ("?", "yellow"),
    "compile-error": ("!", "red"),
    "not-applicable": ("·", "dim"),
    "not-attempted": ("·", "dim"),
}


# ---------------------------------------------------------------------------
# Run summary helpers
# ---------------------------------------------------------------------------


def _list_run_dirs(audits_root: Path) -> list[Path]:
    if not audits_root.exists():
        return []
    return sorted(
        (p for p in audits_root.iterdir() if p.is_dir() and (p / "prep.json").exists()),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )


def _load_prep(run_dir: Path) -> dict:
    try:
        return json.loads((run_dir / "prep.json").read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _load_findings(run_dir: Path) -> list[dict]:
    fp = run_dir / "findings.json"
    if not fp.exists():
        return []
    try:
        data = json.loads(fp.read_text())
        return data if isinstance(data, list) else data.get("findings", [])
    except json.JSONDecodeError:
        return []


def _load_static_tools(run_dir: Path) -> list[dict]:
    fp = run_dir / "static-tools.json"
    if not fp.exists():
        return []
    try:
        return json.loads(fp.read_text())
    except json.JSONDecodeError:
        return []


def _coverage_pct(static: list[dict]) -> str:
    for tool in static:
        if tool.get("tool") != "foundry" or not tool.get("succeeded"):
            continue
        cov = (tool.get("output") or {}).get("coverage") or {}
        if cov.get("status") == "ok":
            return f"{cov.get('function_pct', 0):.0f}% fn / {cov.get('line_pct', 0):.0f}% ln"
    return "—"


def _summary_row(run_dir: Path) -> dict:
    prep = _load_prep(run_dir)
    findings = _load_findings(run_dir)
    static = _load_static_tools(run_dir)
    by_sev: dict[str, int] = {}
    by_poc: dict[str, int] = {}
    for f in findings:
        by_sev[f.get("severity", "?")] = by_sev.get(f.get("severity", "?"), 0) + 1
        by_poc[f.get("poc_status", "not-attempted")] = (
            by_poc.get(f.get("poc_status", "not-attempted"), 0) + 1
        )
    target = prep.get("target", str(run_dir))
    tm = prep.get("target_metadata") or {}
    if prep.get("target_kind") == "deployed-address" and tm.get("address"):
        target = f"{tm['contract_name'] or tm['address']} @ {tm.get('chain') or tm.get('chain_id')}"
    return {
        "run_dir": run_dir,
        "name": run_dir.name,
        "target": target,
        "timestamp": prep.get("timestamp", "?"),
        "kind": prep.get("target_kind", "?"),
        "n_findings": len(findings),
        "by_sev": by_sev,
        "by_poc": by_poc,
        "coverage": _coverage_pct(static),
        "reconciled": (run_dir / "reconciled.json").exists(),
    }


# ---------------------------------------------------------------------------
# Renderers
# ---------------------------------------------------------------------------


def _sev_text(sev: str) -> Text:
    style = SEVERITY_STYLE.get(sev, "white")
    return Text(sev, style=style)


def _poc_text(status: str) -> Text:
    sym, style = POC_STYLE.get(status, ("·", "dim"))
    return Text(f"{sym} {status}", style=style)


def _sev_breakdown(by_sev: dict) -> Text:
    """Compact severity badge string for the list view."""
    parts: list[Text] = []
    for sev in ("Critical", "High", "Medium", "Low", "Informational", "Gas"):
        if by_sev.get(sev):
            parts.append(Text(f"{by_sev[sev]}{sev[0]}", style=SEVERITY_STYLE[sev]))
    if not parts:
        return Text("—", style="dim")
    out = Text()
    for i, p in enumerate(parts):
        if i:
            out.append(" ")
        out.append(p)
    return out


def _poc_breakdown(by_poc: dict) -> Text:
    n_ok = by_poc.get("reproduced", 0)
    n_un = by_poc.get("unconfirmed", 0)
    n_err = by_poc.get("compile-error", 0)
    n_na = by_poc.get("not-applicable", 0) + by_poc.get("not-attempted", 0)
    if n_ok + n_un + n_err == 0:
        return Text(f"{n_na} n/a", style="dim")
    out = Text()
    if n_ok:
        out.append(f"{n_ok}✓ ", style="bold green")
    if n_un:
        out.append(f"{n_un}? ", style="yellow")
    if n_err:
        out.append(f"{n_err}! ", style="red")
    if n_na:
        out.append(f"{n_na}·", style="dim")
    return out


def render_list(audits_root: Path) -> Table:
    """One row per audit run, most recent first."""
    table = Table(
        title=f"web3Sentinel audit history ({audits_root.relative_to(REPO_ROOT) if audits_root.is_relative_to(REPO_ROOT) else audits_root})",
        show_lines=False,
        border_style="dim",
    )
    table.add_column("Run", style="cyan", no_wrap=False)
    table.add_column("Target", style="white", max_width=42)
    table.add_column("Kind", style="dim")
    table.add_column("Findings", justify="right")
    table.add_column("Severities", justify="left")
    table.add_column("PoC", justify="left")
    table.add_column("Coverage", justify="right", style="cyan")
    table.add_column("Modes", style="dim")

    runs = _list_run_dirs(audits_root)
    if not runs:
        table.add_row("(no audit runs found)", "", "", "", "", "", "", "")
        return table

    for r in runs[:40]:
        s = _summary_row(r)
        modes = "M" if s["reconciled"] else "S"  # multimodel vs single
        table.add_row(
            s["name"],
            s["target"],
            s["kind"],
            str(s["n_findings"]),
            _sev_breakdown(s["by_sev"]),
            _poc_breakdown(s["by_poc"]),
            s["coverage"],
            modes,
        )
    return table


def _finding_panel(idx: int, f: dict, *, target_root: Path | None = None) -> Panel:
    """One Panel per finding for the show view."""
    sev = f.get("severity", "?")
    title = f.get("title", "(no title)")
    novel = " [novel]" if f.get("novel") else ""
    header = Text()
    header.append(f"#{idx} ", style="dim")
    header.append(f"[{sev}]", style=SEVERITY_STYLE.get(sev, "white"))
    header.append(f"{novel} ", style="dim italic")
    header.append(title, style="bold")

    discovered = f.get("discovered_by", "?")
    confidence = f.get("confidence", "?")
    status_line = Text()
    status_line.append(f"by {discovered}", style="dim")
    status_line.append(" | conf=", style="dim")
    status_line.append(confidence)
    status_line.append(" | poc=", style="dim")
    status_line.append(_poc_text(f.get("poc_status", "not-attempted")))
    if f.get("citations"):
        status_line.append("\nciting: ", style="dim")
        status_line.append(", ".join(f["citations"]), style="cyan")

    location_lines = []
    for loc in f.get("location", []):
        line_end = f"-{loc['line_end']}" if loc.get("line_end") else ""
        location_lines.append(f"{loc['file']}:{loc['line_start']}{line_end}")
    locations = Text("\n".join(location_lines) if location_lines else "(no location)", style="green")

    body = Group(
        status_line,
        Text(""),
        Text("Description:", style="bold dim"),
        Markdown(f.get("description", "")[:1500]),
        Text(""),
        Text("Impact:", style="bold dim"),
        Markdown(f.get("impact", "")[:800]),
        Text(""),
        Text("Recommendation:", style="bold dim"),
        Markdown(f.get("recommendation", "")[:800]),
        Text(""),
        Text("Location:", style="bold dim"),
        locations,
    )
    if f.get("foundry_poc"):
        body = Group(
            body,
            Text(""),
            Text("Foundry PoC artifacts:", style="bold dim"),
            Text(json.dumps(f.get("poc_artifacts") or {}, indent=2), style="dim"),
        )
    return Panel(body, title=header, border_style=SEVERITY_STYLE.get(sev, "white"))


def _render_deep_dive_show(run_dir: Path) -> Group:
    """Specialized view for deep-dive run dirs — counts + invariants + report path."""
    pf_path = run_dir / "per-function.jsonl"
    n_fn = 0
    n_vulns = 0
    n_high = 0
    n_critical = 0
    n_invariants_est = 0
    n_invariants_ass = 0
    if pf_path.exists():
        import json as _json
        for line in pf_path.read_text().splitlines():
            if not line.strip():
                continue
            try:
                fn = _json.loads(line)
            except _json.JSONDecodeError:
                continue
            n_fn += 1
            n_invariants_est += len(fn.get("invariants_established") or [])
            n_invariants_ass += len(fn.get("invariants_assumed") or [])
            for v in (fn.get("candidate_vulnerabilities") or []):
                n_vulns += 1
                if v.get("severity") == "High":
                    n_high += 1
                elif v.get("severity") == "Critical":
                    n_critical += 1
    cross_vulns = 0
    cross_breakages = 0
    cf_path = run_dir / "cross-function.jsonl"
    if cf_path.exists():
        import json as _json
        for line in cf_path.read_text().splitlines():
            if not line.strip():
                continue
            try:
                c = _json.loads(line)
            except _json.JSONDecodeError:
                continue
            cross_vulns += len(c.get("vulnerabilities") or [])
            cross_breakages += len(c.get("broken_invariants") or [])

    banner = Panel(
        Group(
            Text(f"Run:               {run_dir.name}", style="cyan"),
            Text(f"Functions:         {n_fn}"),
            Text(f"Candidate vulns:   {n_vulns}  (Critical: {n_critical}, High: {n_high})"),
            Text(f"Cross-fn vulns:    {cross_vulns}"),
            Text(f"Invariants:        {n_invariants_est} established, "
                 f"{n_invariants_ass} assumed"),
            Text(f"Invariant breaks:  {cross_breakages}"),
            Text(""),
            Text("See:", style="dim"),
            Text(f"  {run_dir / 'deep-dive-report.md'}", style="cyan"),
            Text(f"  {run_dir / 'invariants.md'}", style="cyan"),
        ),
        title=Text("deep-dive run", style="bold"),
        border_style="cyan",
    )
    return Group(banner)


def render_show(run_dir: Path) -> Group:
    # Route to specialized renderer for deep-dive dirs
    if run_dir.name.startswith("deep-dive-") or (run_dir / "deep-dive-report.md").exists():
        return _render_deep_dive_show(run_dir)
    # Scrutinize dirs surface the master report path + per-phase pointers
    if run_dir.name.startswith("scrutinize-") or (run_dir / "scrutinize-report.md").exists():
        return Group(Panel(
            Group(
                Text(f"Run:               {run_dir.name}", style="cyan"),
                Text(""),
                Text(f"Master report:     {run_dir / 'scrutinize-report.md'}", style="cyan"),
                Text(f"State:             {run_dir / 'state.json'}", style="dim"),
                Text(""),
                Text("To see the master report:", style="dim"),
                Text(f"  cat {run_dir / 'scrutinize-report.md'}", style="cyan"),
            ),
            title=Text("scrutinize run", style="bold"),
            border_style="cyan",
        ))

    prep = _load_prep(run_dir)
    findings = _load_findings(run_dir)
    static = _load_static_tools(run_dir)
    s = _summary_row(run_dir)

    # Header banner
    title = Text()
    title.append("web3Sentinel audit  ", style="bold")
    title.append(f"{run_dir.name}", style="cyan")
    if s["reconciled"]:
        title.append("  (multimodel)", style="dim")
    banner = Panel(
        Group(
            Text(f"Target:    {s['target']}", style="white"),
            Text(f"Kind:      {s['kind']}", style="dim"),
            Text(f"Time:      {s['timestamp']}", style="dim"),
            Text(f"Findings:  {s['n_findings']}  ({_sev_breakdown(s['by_sev']).plain})"),
            Text(f"PoC:       {_poc_breakdown(s['by_poc']).plain}"),
            Text(f"Coverage:  {s['coverage']}"),
        ),
        title=title,
        border_style="cyan",
    )

    # Static tool quick-summary
    static_rows = Table(show_header=True, header_style="bold", border_style="dim")
    static_rows.add_column("Tool")
    static_rows.add_column("Status")
    static_rows.add_column("Version", style="dim")
    static_rows.add_column("Detail")
    for t in static:
        if t.get("succeeded"):
            detail = ""
            if t["tool"] == "slither":
                detail = f"{(t.get('output') or {}).get('detector_count', 0)} detectors"
            elif t["tool"] == "aderyn":
                detail = f"{(t.get('output') or {}).get('issue_count', 0)} issues"
            elif t["tool"] == "foundry":
                cov = (t.get("output") or {}).get("coverage") or {}
                if cov.get("status") == "ok":
                    detail = f"build ok; coverage {cov.get('function_pct', 0):.0f}% fn"
                else:
                    detail = "build ok; coverage n/a"
            static_rows.add_row(t["tool"], Text("ok", style="green"), t.get("version") or "—", detail)
        else:
            static_rows.add_row(t["tool"], Text("fail", style="red"), "—", (t.get("error") or "")[:50])

    static_panel = Panel(static_rows, title="Static analyzers", border_style="dim")

    if not findings:
        findings_block: Group | Panel = Panel(
            Text("No findings produced for this run.", style="dim"),
            title="Findings",
            border_style="dim",
        )
    else:
        sev_order = {sev: i for i, sev in enumerate(["Critical", "High", "Medium", "Low", "Informational", "Gas"])}
        findings_sorted = sorted(findings, key=lambda f: (sev_order.get(f.get("severity"), 99), f.get("title", "")))
        findings_block = Group(*[_finding_panel(i + 1, f) for i, f in enumerate(findings_sorted)])

    return Group(banner, static_panel, Rule("Findings", style="dim"), findings_block)


def render_findings_table(run_dir: Path) -> Table:
    findings = _load_findings(run_dir)
    table = Table(title=f"Findings — {run_dir.name}", show_lines=False)
    table.add_column("#", justify="right")
    table.add_column("Severity")
    table.add_column("PoC")
    table.add_column("Title")
    table.add_column("By", style="dim")
    table.add_column("Citations", style="cyan")

    sev_order = {sev: i for i, sev in enumerate(["Critical", "High", "Medium", "Low", "Informational", "Gas"])}
    findings_sorted = sorted(findings, key=lambda f: (sev_order.get(f.get("severity"), 99), f.get("title", "")))
    for i, f in enumerate(findings_sorted, start=1):
        cites = ", ".join(f.get("citations") or []) or ("—" if not f.get("novel") else "[novel]")
        table.add_row(
            str(i),
            _sev_text(f.get("severity", "?")),
            _poc_text(f.get("poc_status", "not-attempted")),
            f.get("title", "")[:80],
            f.get("discovered_by", "?"),
            cites,
        )
    return table


# ---------------------------------------------------------------------------
# Status (live view)
# ---------------------------------------------------------------------------


def render_status(run_dir: Path) -> Group:
    """Live status banner — for an in-progress run."""
    prep = _load_prep(run_dir)
    findings = _load_findings(run_dir)
    auditor_out = (run_dir / "auditor-output.json").exists()
    codex_out = (run_dir / "codex-output.json").exists()
    reconciled = (run_dir / "reconciled.json").exists()
    static_ok = (run_dir / "static-tools.json").exists()
    report = (run_dir / "report.md").exists()

    s = _summary_row(run_dir)

    state_table = Table(show_header=False, box=None, padding=(0, 1))
    state_table.add_column("flag", style="dim")
    state_table.add_column("value")
    for label, ok in [
        ("prep.json", bool(prep)),
        ("static-tools.json", static_ok),
        ("auditor-output.json", auditor_out),
        ("codex-output.json", codex_out),
        ("reconciled.json", reconciled),
        ("findings.json", bool(findings)),
        ("report.md", report),
    ]:
        state_table.add_row(label, Text("✓" if ok else "·", style="green" if ok else "dim"))

    summary = Text()
    summary.append(f"target  ", style="dim")
    summary.append(f"{s['target']}\n")
    summary.append("status  ", style="dim")
    summary.append(_sev_breakdown(s["by_sev"]).plain or "(no findings yet)")
    summary.append("\npoc     ", style="dim")
    summary.append(_poc_breakdown(s["by_poc"]).plain or "(no pocs yet)")
    summary.append(f"\nnow     {datetime.now().strftime('%H:%M:%S')}", style="dim")

    return Group(
        Panel(state_table, title=f"pipeline state — {run_dir.name}", border_style="cyan"),
        Panel(summary, title="run summary", border_style="cyan"),
    )


def cmd_status(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir)
    interval = args.interval
    if not args.follow:
        console.print(render_status(run_dir))
        return 0
    try:
        with Live(render_status(run_dir), refresh_per_second=4) as live:
            while True:
                time.sleep(interval)
                live.update(render_status(run_dir))
    except KeyboardInterrupt:
        return 0


def cmd_latest(args: argparse.Namespace) -> int:
    """Print the path to the most recent run (audit / scrutinize / deep-dive).

    Useful for shell pipelines: `cat $(w3s latest)/report.md`
    """
    audits_root = REPO_ROOT / "audits"
    if not audits_root.exists():
        return 1

    def is_audit(p: Path) -> bool:
        return (p / "prep.json").exists()

    def is_scrutinize(p: Path) -> bool:
        return p.name.startswith("scrutinize-") or (p / "scrutinize-report.md").exists()

    def is_deep_dive(p: Path) -> bool:
        return p.name.startswith("deep-dive-") or (p / "deep-dive-report.md").exists()

    candidates = []
    for p in audits_root.iterdir():
        if not p.is_dir():
            continue
        a, s, d = is_audit(p), is_scrutinize(p), is_deep_dive(p)
        if args.kind == "audit" and not a:
            continue
        if args.kind == "scrutinize" and not s:
            continue
        if args.kind == "deep-dive" and not d:
            continue
        if args.kind == "any" and not (a or s or d):
            # Skip stray side-effect dirs like synthesize-*
            continue
        candidates.append(p)
    if not candidates:
        return 1
    latest = max(candidates, key=lambda p: p.stat().st_mtime)
    print(latest)
    return 0


def cmd_overview(args: argparse.Namespace) -> int:
    """At-a-glance dashboard: corpus + queue + recent audits + submissions."""
    from harness import candidates as cand_store
    from harness import corpus as corpus_mod
    from harness import submissions as sub_mod

    # Corpus stats
    try:
        c_stats = corpus_mod.stats()
        corpus_table = Table(show_header=False, box=None)
        corpus_table.add_column(style="cyan")
        corpus_table.add_column()
        corpus_table.add_row("total entries", str(c_stats["total"]))
        sources = ", ".join(f"{k}={v}" for k, v in sorted(c_stats["by_source"].items()))
        corpus_table.add_row("by source", sources)
        synth_n = c_stats["by_source"].get("synthesis", 0)
        corpus_table.add_row("synthesis notes", str(synth_n))
        # List synthesis note titles — the densest knowledge in the corpus
        synth_dir = REPO_ROOT / "corpus" / "synthesis"
        if synth_dir.exists():
            notes = sorted(synth_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)[:8]
            if notes:
                import re as _re
                lines = []
                for n in notes:
                    text = n.read_text()
                    tmatch = _re.search(r'^title:\s*"?([^"\n]+)"?', text, _re.MULTILINE)
                    title = tmatch.group(1)[:60] if tmatch else n.stem[:60]
                    lines.append(f"  • {title}")
                corpus_table.add_row("recent synthesis", "\n".join(lines))
        console.print(Panel(corpus_table, title="Corpus", border_style="cyan"))
    except Exception as e:  # noqa: BLE001
        console.print(f"[dim]corpus stats unavailable: {e}[/dim]")

    # Candidate queue
    try:
        queue = cand_store.query_queue(limit=10)
        all_cands = cand_store.load_all()
        by_status = {}
        by_platform = {}
        for c in all_cands:
            by_status[c.triage_status] = by_status.get(c.triage_status, 0) + 1
            by_platform[c.platform] = by_platform.get(c.platform, 0) + 1
        cand_table = Table(show_header=False, box=None)
        cand_table.add_column(style="cyan")
        cand_table.add_column()
        cand_table.add_row("total candidates", str(len(all_cands)))
        cand_table.add_row("by platform", ", ".join(f"{k}={v}" for k, v in sorted(by_platform.items())))
        cand_table.add_row("by status", ", ".join(f"{k}={v}" for k, v in sorted(by_status.items())))
        cand_table.add_row("top in queue", str(len([c for c in queue if c.triage_score])))
        console.print(Panel(cand_table, title="Candidate queue", border_style="cyan"))

        if queue and any(c.triage_score for c in queue):
            top_table = Table(title="Top 10 by Stage 1 score", show_lines=False)
            top_table.add_column("Score", justify="right", style="bold")
            top_table.add_column("ID", style="cyan")
            top_table.add_column("Platform", style="dim")
            top_table.add_column("Rationale")
            for c in queue:
                if c.triage_score:
                    color = "green" if c.triage_score >= 7 else ("yellow" if c.triage_score >= 4 else "dim")
                    top_table.add_row(
                        Text(f"{c.triage_score:.0f}", style=color),
                        c.id, c.platform,
                        (c.triage_rationale or "")[:80],
                    )
            console.print(top_table)
    except Exception as e:  # noqa: BLE001
        console.print(f"[dim]queue stats unavailable: {e}[/dim]")

    # Recent audits
    try:
        audits_root = REPO_ROOT / "audits"
        if audits_root.exists():
            runs = sorted(
                (p for p in audits_root.iterdir() if p.is_dir() and (p / "prep.json").exists()),
                key=lambda p: p.stat().st_mtime, reverse=True,
            )[:5]
            audit_table = Table(title="Recent audits", show_lines=False)
            audit_table.add_column("Run", style="cyan")
            audit_table.add_column("Target", max_width=40)
            audit_table.add_column("Findings", justify="right")
            audit_table.add_column("Has PoCs", justify="center")
            for r in runs:
                try:
                    import json as _json
                    prep = _json.loads((r / "prep.json").read_text())
                    n = 0
                    has_poc = False
                    if (r / "findings.json").exists():
                        fs = _json.loads((r / "findings.json").read_text())
                        fs_list = fs if isinstance(fs, list) else fs.get("findings", [])
                        n = len(fs_list)
                        has_poc = any(f.get("poc_status") == "reproduced" for f in fs_list)
                    audit_table.add_row(
                        r.name[:40],
                        str(prep.get("target", ""))[-40:],
                        str(n),
                        "✓" if has_poc else "—",
                    )
                except Exception:  # noqa: BLE001
                    continue
            console.print(audit_table)
    except Exception as e:  # noqa: BLE001
        console.print(f"[dim]audits unavailable: {e}[/dim]")

    # Submissions
    try:
        log = sub_mod.load_log()
        if log:
            by_outcome = {}
            total_paid = 0
            for r in log:
                by_outcome[r.outcome] = by_outcome.get(r.outcome, 0) + 1
                if r.payout_usd:
                    total_paid += r.payout_usd
            sub_table = Table(show_header=False, box=None)
            sub_table.add_column(style="cyan")
            sub_table.add_column()
            sub_table.add_row("total submissions", str(len(log)))
            sub_table.add_row("by outcome", ", ".join(f"{k}={v}" for k, v in sorted(by_outcome.items())))
            sub_table.add_row("payout accrued", f"${total_paid:,}")
            console.print(Panel(sub_table, title="Submissions", border_style="cyan"))
    except Exception as e:  # noqa: BLE001
        console.print(f"[dim]submissions unavailable: {e}[/dim]")

    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def cmd_list(args: argparse.Namespace) -> int:
    root = Path(args.root) if args.root else REPO_ROOT / "audits"
    console.print(render_list(root))
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir)
    if not run_dir.exists():
        # Maybe they passed just the run name; resolve under audits/.
        cand = REPO_ROOT / "audits" / args.run_dir
        if cand.exists():
            run_dir = cand
        else:
            console.print(f"[red]run dir not found: {args.run_dir}[/red]")
            return 1
    console.print(render_show(run_dir))
    return 0


def cmd_findings(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir)
    if not run_dir.exists():
        cand = REPO_ROOT / "audits" / args.run_dir
        if cand.exists():
            run_dir = cand
        else:
            console.print(f"[red]run dir not found: {args.run_dir}[/red]")
            return 1
    console.print(render_findings_table(run_dir))
    return 0


def cmd_pocs(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir)
    if not run_dir.exists():
        cand = REPO_ROOT / "audits" / args.run_dir
        if cand.exists():
            run_dir = cand
        else:
            console.print(f"[red]run dir not found: {args.run_dir}[/red]")
            return 1
    findings = _load_findings(run_dir)
    poc_findings = [f for f in findings if f.get("foundry_poc")]

    table = Table(title=f"PoCs — {run_dir.name}", show_lines=False)
    table.add_column("#", justify="right")
    table.add_column("Status")
    table.add_column("Severity")
    table.add_column("Title")
    table.add_column("Test", style="dim")
    table.add_column("Logs", style="dim")

    if not poc_findings:
        console.print(f"[dim]No structured foundry_poc on any finding in {run_dir.name}.[/dim]")
        return 0

    for i, f in enumerate(poc_findings, start=1):
        art = f.get("poc_artifacts") or {}
        table.add_row(
            str(i),
            _poc_text(f.get("poc_status", "not-attempted")),
            _sev_text(f.get("severity", "?")),
            f.get("title", "")[:60],
            Path(art.get("test_path", "?")).name if art.get("test_path") else "—",
            "stdout/stderr in poc/" if art.get("stdout_log") else "—",
        )
    console.print(table)

    if args.verbose:
        for i, f in enumerate(poc_findings, start=1):
            console.print()
            console.print(Rule(f"#{i}: {f.get('title', '')[:80]}", style="dim"))
            console.print(
                Panel(
                    f.get("foundry_poc", {}).get("exploit", "(empty)"),
                    title="exploit",
                    border_style="dim",
                )
            )
    return 0


def cmd_replay(args: argparse.Namespace) -> int:
    from harness.trace import replay_tx

    try:
        result = replay_tx(args.tx_hash, args.chain)
    except (FileNotFoundError, ValueError) as e:
        console.print(f"[red]{e}[/red]")
        return 1

    if args.out:
        Path(args.out).write_text(result.trace_text)
        console.print(
            f"trace written to {args.out} "
            f"(rc={result.rc}, success={result.success}, gas_used={result.gas_used})"
        )
    else:
        console.print(result.trace_text)
    return 0 if result.rc == 0 else 1


def cmd_synthesize(args: argparse.Namespace) -> int:
    from harness.synthesize import synthesize

    console.print(
        f"[cyan]Synthesizing[/cyan] [bold]{args.topic}[/bold]  "
        f"[dim](this spawns claude-synthesizer headlessly, ~3-5 min, ~$1-2)[/dim]"
    )
    try:
        result = synthesize(
            topic=args.topic,
            seed_query=args.seed_query,
            slug=args.slug,
            model=args.model,
            reindex_after=not args.no_reindex,
            timeout_seconds=args.timeout,
        )
    except FileNotFoundError as e:
        console.print(f"[red]{e}[/red]")
        return 1
    if result.error:
        console.print(f"[yellow]warning:[/yellow] {result.error}")
    console.print(
        f"\n[green]synthesis note written[/green]: {result.note_path}"
    )
    if result.derives_count is not None:
        console.print(f"derives_from: {result.derives_count} corpus entries")
    return 1 if result.error else 0


def cmd_deep_dive(args: argparse.Namespace) -> int:
    """Exhaustively analyze ONE target — every function gets its own Opus call."""
    from harness import deep_dive

    target_str, scope_str = _resolve_target_args(args)
    if not target_str:
        raise SystemExit("provide a target path or --from-candidate")
    target = Path(target_str).expanduser().resolve()
    scope = Path(scope_str).expanduser().resolve() if scope_str else None
    out_dir = Path(args.out).expanduser().resolve() if args.out else None

    # Quick decomposition preview so the user sees scale before LLM spend
    units = deep_dive.decompose(target, scope=scope)
    if args.max_functions:
        units = units[: args.max_functions]
    console.print(
        f"[cyan]Decomposed[/cyan] target into [bold]{len(units)}[/bold] functions. "
        f"Will spend ~{len(units)} Opus messages per-fn, plus up to {args.max_cross_pairs} cross-fn."
    )
    if args.dry_run:
        # Print the decomposition only
        for u in units[:30]:
            dangers = ", ".join(f"{k}={v}" for k, v in u.danger_grep.items() if v)
            console.print(
                f"  [{u.visibility:>10}/{u.mutability:>10}] {u.fn_id}  "
                f"lines={u.line_start}-{u.line_end}  dangers=[{dangers}]"
            )
        if len(units) > 30:
            console.print(f"  ... and {len(units) - 30} more")
        return 0

    started = time.monotonic()

    def progress(phase, idx, total, msg):
        elapsed = int(time.monotonic() - started)
        color = "cyan" if "cached" not in msg else "dim"
        console.print(f"[{color}][{phase} {idx + 1}/{total} · {elapsed}s][/{color}] {msg}")

    report_path = deep_dive.run_deep_dive(
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

    elapsed = int(time.monotonic() - started)

    # Optional: materialize PoCs for High/Critical candidates (slice 11/deep-dive bridge)
    materialized_summary = ""
    if args.materialize_pocs and report_path.parent.exists():
        from harness import deep_dive_poc

        def mat_progress(phase, idx, total, msg):
            console.print(f"[cyan][materialize {phase} {idx}/{total}][/cyan] {msg}")

        try:
            mat_path = deep_dive_poc.materialize_for_run(
                report_path.parent,
                target,
                min_severity=args.materialize_min_severity,
                model=args.model,
                progress_callback=mat_progress,
            )
            materialized_summary = "\n\n" + deep_dive_poc.render_materialization_summary(mat_path)
        except Exception as e:  # noqa: BLE001
            materialized_summary = f"\n\nmaterialize failed: {e}"

    console.print()
    console.print(
        Panel(
            f"Report: {report_path}\nTime: {elapsed}s ({elapsed // 60}m {elapsed % 60}s)"
            + materialized_summary,
            title="deep-dive complete",
            border_style="green",
        )
    )
    return 0


def _resolve_candidate_target(candidate_id: str) -> tuple[str, str | None]:
    """Look up a candidate by id, return (target_path, scope_subpath_or_None)."""
    from harness import candidates as cand_store

    cand = cand_store.get(candidate_id)
    if not cand:
        raise SystemExit(f"candidate {candidate_id!r} not found in queue")
    if not cand.local_path:
        raise SystemExit(
            f"candidate {candidate_id!r} has no local_path — run `w3s sweep` "
            f"or clone manually first."
        )
    # If scope_paths is set, use the first as the scope hint
    scope = cand.scope_paths[0] if cand.scope_paths else None
    return cand.local_path, scope


def cmd_scrutinize(args: argparse.Namespace) -> int:
    """Maximum-depth pipeline: audit + deep-dive + materialize-pocs + filter on one target."""
    from harness import scrutinize

    target = args.target
    scope = args.scope
    if getattr(args, "from_candidate", None):
        target, cand_scope = _resolve_candidate_target(args.from_candidate)
        if scope is None and cand_scope:
            scope = cand_scope
        console.print(f"[cyan]Resolved candidate[/cyan] {args.from_candidate} → {target}"
                      + (f" (scope: {scope})" if scope else ""))

    out_dir = Path(args.out).expanduser().resolve() if args.out else None
    if not target:
        raise SystemExit("provide a target path or --from-candidate")
    scrutinize.scrutinize(
        target,
        chain=args.chain,
        scope=scope,
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


def _resolve_target_args(args: argparse.Namespace) -> tuple[str, str | None]:
    """For cmd_deep_dive: resolve --from-candidate → (target, scope)."""
    target = args.target
    scope = args.scope
    if getattr(args, "from_candidate", None):
        target, cand_scope = _resolve_candidate_target(args.from_candidate)
        if scope is None and cand_scope:
            scope = cand_scope
        console.print(f"[cyan]Resolved candidate[/cyan] {args.from_candidate} → {target}"
                      + (f" (scope: {scope})" if scope else ""))
    return target, scope


def cmd_sweep(args: argparse.Namespace) -> int:
    """Run all enabled platform ingestors, write Candidates, optionally Stage-1 rank."""
    from crawlers import c4_contests, sherlock_audits, cantina_audits, immunefi_programs
    from harness import candidates as cand_store
    from harness import stage1

    cache_root = Path(args.cache or (REPO_ROOT / ".cache" / "sweep"))
    sourced: list = []

    if "c4" in args.platforms:
        console.print(f"[cyan]→ fetching Code4rena active contests...[/cyan]")
        try:
            c4 = c4_contests.fetch_active_candidates(clone_cache=None if args.no_clone else cache_root / "c4")
        except Exception as e:  # noqa: BLE001
            console.print(f"  [red]C4 fetch failed: {e}[/red]")
            c4 = []
        console.print(f"  {len(c4)} contest(s)")
        sourced.extend(c4)

    if "sherlock" in args.platforms:
        console.print(f"[cyan]→ fetching Sherlock active audits...[/cyan]")
        try:
            sh = sherlock_audits.fetch_active_candidates(clone_cache=None if args.no_clone else cache_root / "sherlock")
        except Exception as e:  # noqa: BLE001
            console.print(f"  [red]Sherlock fetch failed: {e}[/red]")
            sh = []
        console.print(f"  {len(sh)} audit(s)")
        sourced.extend(sh)

    if "cantina" in args.platforms:
        console.print(f"[cyan]→ fetching Cantina active competitions...[/cyan]")
        try:
            ca = cantina_audits.fetch_active_candidates(clone_cache=None if args.no_clone else cache_root / "cantina")
        except Exception as e:  # noqa: BLE001
            console.print(f"  [red]Cantina fetch failed: {e}[/red]")
            ca = []
        console.print(f"  {len(ca)} competition(s)")
        sourced.extend(ca)

    if "immunefi" in args.platforms:
        console.print(f"[cyan]→ fetching Immunefi active programs...[/cyan]")
        try:
            im = immunefi_programs.fetch_active_candidates()
        except Exception as e:  # noqa: BLE001
            console.print(f"  [red]Immunefi fetch failed: {e}[/red]")
            im = []
        console.print(f"  {len(im)} program(s)")
        sourced.extend(im)

    new, changed = cand_store.diff_against_log(sourced)
    if new or changed:
        cand_store.append(new + changed)
        cand_store.reindex()
    console.print(
        f"[green]Sweep complete:[/green] {len(sourced)} active, "
        f"{len(new)} new, {len(changed)} changed in queue."
    )

    if not args.no_stage1 and new:
        to_rank = new
        if args.max_new and len(to_rank) > args.max_new:
            console.print(
                f"[yellow]Capping Stage 1 ranking at {args.max_new} of {len(new)} new candidates "
                f"(--max-new). Remaining stay status=new, rank them later with `w3s queue --status new`.[/yellow]"
            )
            to_rank = new[: args.max_new]
        console.print(f"\n[cyan]→ Stage 1 ranking {len(to_rank)} new candidate(s) (model={args.model})[/cyan]")
        for cand in to_rank:
            if not cand.local_path or not Path(cand.local_path).exists():
                console.print(f"  [dim]skip {cand.id}: no local source[/dim]")
                continue
            with console.status(f"[cyan]ranking {cand.id}...[/cyan]", spinner="dots"):
                result = stage1.rank_candidate(cand, Path(cand.local_path), model=args.model)
            stage1.apply_to_candidate(cand, result)
            cand_store.upsert(cand)
            score_str = f"[bold]{result.score}/10[/bold]"
            color = "green" if result.score >= 7 else ("yellow" if result.score >= 4 else "dim")
            console.print(f"  [{color}]{score_str}[/{color}] {cand.id}  ::  {result.rationale[:100]}")
        cand_store.reindex()

    return 0


def cmd_queue(args: argparse.Namespace) -> int:
    """Show the ranked candidate queue."""
    from harness import candidates as cand_store

    queue = cand_store.query_queue(
        platform=args.platform,
        status=args.status,
        min_score=args.min_score,
        limit=args.limit,
    )

    table = Table(title=f"Candidate queue ({len(queue)} of top {args.limit})", show_lines=False)
    table.add_column("Score", justify="right", style="bold")
    table.add_column("ID", style="cyan")
    table.add_column("Platform", style="dim")
    table.add_column("Status", style="dim")
    table.add_column("Payout", justify="right")
    table.add_column("Closes")
    table.add_column("Rationale")
    for c in queue:
        score = f"{c.triage_score:.0f}" if c.triage_score is not None else "—"
        color = "green" if (c.triage_score or 0) >= 7 else ("yellow" if (c.triage_score or 0) >= 4 else "dim")
        payout = f"${c.payout_max_usd:,}" if c.payout_max_usd else "—"
        closes = (c.closes_at or "—")[:16]
        rat = (c.triage_rationale or "—")[:90]
        table.add_row(Text(score, style=color), c.id, c.platform, c.triage_status, payout, closes, rat)
    console.print(table)

    if args.detail and queue:
        for c in queue[: args.detail]:
            console.print()
            console.print(Rule(c.id, style="cyan"))
            if c.triage_top_suspects:
                console.print("[bold]Top suspects:[/bold]")
                for s in c.triage_top_suspects:
                    console.print(f"  • {s.get('file')}::{s.get('function')}  --  {s.get('why')}")
            if c.triage_skip_reasons:
                console.print("[bold yellow]Skip reasons:[/bold yellow]")
                for r in c.triage_skip_reasons:
                    console.print(f"  • {r}")
            if c.local_path:
                console.print(f"[dim]local source: {c.local_path}[/dim]")
            if c.repo_url:
                console.print(f"[dim]repo: {c.repo_url}[/dim]")
    return 0


def cmd_submit(args: argparse.Namespace) -> int:
    """Emit per-platform submission templates for a completed audit run."""
    from harness.submissions import export_run

    run_dir = Path(args.run_dir)
    if not run_dir.exists():
        cand = REPO_ROOT / "audits" / args.run_dir
        if cand.exists():
            run_dir = cand
        else:
            console.print(f"[red]no run dir {args.run_dir}[/red]")
            return 1
    records = export_run(
        run_dir,
        candidate_id=args.candidate_id,
        platforms=args.platforms,
        min_severity=args.min_severity,
        only_reproduced=args.only_reproduced,
    )
    console.print(f"[green]Exported {len(records)} submission template(s):[/green]")
    for r in records:
        console.print(f"  [{r.finding_severity}] {r.platform}  ::  {r.template_path}")
    return 0


def cmd_submissions(args: argparse.Namespace) -> int:
    """Show the submissions log as a table; filter by candidate or outcome."""
    from harness import submissions as sub

    log = sub.load_log()
    if args.candidate_id:
        log = [r for r in log if r.candidate_id == args.candidate_id]
    if args.outcome:
        log = [r for r in log if r.outcome == args.outcome]
    if args.platform:
        log = [r for r in log if r.platform == args.platform]
    log.sort(key=lambda r: r.created_at, reverse=True)
    log = log[:args.limit]

    if not log:
        console.print("[dim]No submissions match the filters. Run `w3s submit` to start logging.[/dim]")
        return 0

    t = Table(show_header=True, header_style="bold", title="Submissions")
    t.add_column("Created", style="dim")
    t.add_column("Candidate", style="cyan")
    t.add_column("Platform")
    t.add_column("Sev")
    t.add_column("Title", overflow="fold", max_width=50)
    t.add_column("Outcome")
    t.add_column("Payout", justify="right")
    for r in log:
        outcome_color = {"accepted": "green", "duplicate": "yellow",
                         "rejected": "red", "pending": "dim",
                         "withdrawn": "dim"}.get(r.outcome, "")
        payout_str = f"${r.payout_usd:,}" if r.payout_usd else "—"
        t.add_row(
            r.created_at[:10],
            r.candidate_id[:30],
            r.platform,
            r.finding_severity,
            r.finding_title[:50],
            Text(r.outcome, style=outcome_color),
            payout_str,
        )
    console.print(t)

    # Aggregate stats
    by_outcome: dict[str, int] = {}
    total_paid = 0
    for r in log:
        by_outcome[r.outcome] = by_outcome.get(r.outcome, 0) + 1
        if r.payout_usd:
            total_paid += r.payout_usd
    console.print()
    console.print(f"[dim]Total: {len(log)}  | "
                  f"By outcome: {', '.join(f'{k}={v}' for k, v in by_outcome.items())}  | "
                  f"Payout: ${total_paid:,}[/dim]")
    return 0


def cmd_autoscrutinize(args: argparse.Namespace) -> int:
    """Pick the top suggested candidate + scrutinize it. End-to-end autonomy."""
    from harness import scrutinize, suggest

    # Step 1: pick a candidate
    suggestions = suggest.suggest_top_n(
        n=max(args.top, 1),
        platform=args.platform,
        min_stage1=args.min_stage1,
        include_audited=False,
        include_closed=False,
    )
    if not suggestions:
        console.print("[yellow]No candidates available. Run `w3s sweep` first.[/yellow]")
        return 1
    picked = suggestions[0]
    console.print(f"[bold cyan]Picked:[/bold cyan] {picked.candidate.id}  "
                  f"(score={picked.score:.3f})  {picked.reasoning}")

    cand = picked.candidate
    if not cand.local_path:
        console.print(f"[yellow]Candidate has no local_path — needs clone. Skipping.[/yellow]")
        return 1

    # Step 2: dry-run first (always — cheap, informs the user)
    scope = cand.scope_paths[0] if cand.scope_paths else None
    if args.dry_run_first or args.dry_run:
        console.print("\n[bold]Dry-run preview:[/bold]")
        scrutinize.scrutinize(
            cand.local_path, scope=scope, model=args.model,
            deep_dive_max_functions=args.max_functions,
            dry_run=True,
        )
        if args.dry_run:
            return 0

    # Step 3: actual scrutinize
    out_dir = Path(args.out).expanduser().resolve() if args.out else None
    scrutinize.scrutinize(
        cand.local_path,
        scope=scope,
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
    )
    return 0


def cmd_digest(args: argparse.Namespace) -> int:
    """What did the system do in the last N hours?"""
    from harness import digest

    d = digest.generate_digest(hours=args.hours)
    if args.json:
        import json as _json
        print(_json.dumps(d, indent=2))
    else:
        digest.render_digest(d)
    return 0


def cmd_suggest(args: argparse.Namespace) -> int:
    """Pick the best candidate(s) to scrutinize next, ranked by composite score."""
    from harness import suggest

    suggestions = suggest.suggest_top_n(
        args.top,
        platform=args.platform,
        min_stage1=args.min_stage1,
        include_audited=args.include_audited,
        include_closed=args.include_closed,
    )
    suggest.render_suggestions(suggestions)
    return 0


def cmd_corpus(args: argparse.Namespace) -> int:
    from harness import corpus as corpus_mod

    if args.corpus_cmd == "stats":
        stats = corpus_mod.stats()
        table = Table(title="Corpus stats", show_header=False, box=None)
        table.add_column("metric", style="cyan")
        table.add_column("value")
        table.add_row("total entries", str(stats["total"]))
        table.add_row("by source", ", ".join(f"{k}={v}" for k, v in sorted(stats["by_source"].items())))
        table.add_row("by severity", ", ".join(f"{k}={v}" for k, v in sorted(stats["by_severity"].items())))
        console.print(table)
        if stats.get("top_vuln_classes"):
            t2 = Table(title="Top vuln_class tags", show_header=True, header_style="dim")
            t2.add_column("class", style="cyan")
            t2.add_column("count", justify="right")
            for row in stats["top_vuln_classes"][:15]:
                t2.add_row(row["vuln_class"], str(row["count"]))
            console.print(t2)
        return 0

    if args.corpus_cmd == "search":
        hits = corpus_mod.search(
            query=args.query,
            vuln_class=args.vuln_class,
            severity=args.severity,
            source=args.source,
            top_k=args.top_k,
        )
        table = Table(title=f"Corpus search: {args.query!r}", show_lines=False)
        table.add_column("#", justify="right")
        table.add_column("Score", justify="right", style="dim")
        table.add_column("Source", style="cyan")
        table.add_column("Severity")
        table.add_column("ID", style="cyan")
        table.add_column("Title")
        for i, h in enumerate(hits, 1):
            table.add_row(
                str(i),
                f"{h.score:.2f}",
                h.source,
                _sev_text(h.severity or "?") if h.severity else Text("—", style="dim"),
                h.id[:55],
                h.title[:60],
            )
        console.print(table)
        return 0

    if args.corpus_cmd == "read":
        entry = corpus_mod.get_entry(args.entry_id)
        if entry is None:
            console.print(f"[red]no such entry: {args.entry_id}[/red]")
            return 1
        meta_table = Table(show_header=False, box=None)
        meta_table.add_column(style="cyan")
        meta_table.add_column()
        for k in ("id", "source", "title", "severity", "ingested_at", "published_at", "source_url"):
            if entry.get(k) is not None:
                meta_table.add_row(k, str(entry[k]))
        if entry.get("vuln_class"):
            meta_table.add_row("vuln_class", ", ".join(entry["vuln_class"]))
        if entry.get("tags"):
            meta_table.add_row("tags", ", ".join(entry["tags"][:6]))
        console.print(Panel(meta_table, title=entry.get("id", "?"), border_style="cyan"))
        if not args.meta_only:
            console.print()
            console.print(Markdown(entry.get("body", "")[:6000]))
        return 0
    return 1


def cmd_audit(args: argparse.Namespace) -> int:
    from harness.orchestrator import Orchestrator, OrchestratorOptions

    opts = OrchestratorOptions(
        target=args.target,
        chain=args.chain,
        scope=args.scope,
        model=args.model,
        codex_model=args.codex_model,
        codex_reasoning_effort=args.codex_effort,
        deep=args.deep,
        with_pocs=not args.no_pocs,
        verbose=args.verbose,
        dry_run=args.dry_run,
    )
    orch = Orchestrator(opts)
    if args.multimodel:
        return orch.run_multimodel()
    return orch.run_single()


def cmd_doctor(args: argparse.Namespace) -> int:
    from harness.doctor import run_doctor

    return run_doctor(skip_auth=args.skip_auth)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_audit = sub.add_parser(
        "audit",
        help="Run an end-to-end audit with live progress (the user-facing entrypoint).",
    )
    p_audit.add_argument("target", help="Path to .sol / project dir, or 0x-address for on-chain.")
    p_audit.add_argument("--chain", default="mainnet", help="Chain name for deployed-address mode.")
    p_audit.add_argument("--scope", help="Restrict auditor reading to .sol files under this path.")
    p_audit.add_argument("--multimodel", action="store_true", help="Run Claude + Codex in parallel then reconcile.")
    p_audit.add_argument("--model", default="opus", help="Claude model.")
    p_audit.add_argument("--codex-model", default="gpt-5.5")
    p_audit.add_argument("--codex-effort", default="high", help="Codex reasoning effort.")
    p_audit.add_argument("--deep", action="store_true", help="Also run Halmos/Mythril.")
    p_audit.add_argument("--no-pocs", action="store_true", help="Skip PoC scaffolding + execution.")
    p_audit.add_argument("--verbose", action="store_true", help="Stream subprocess stderr to terminal.")
    p_audit.add_argument(
        "--dry-run",
        action="store_true",
        help="Run prep only (static tools + materialize source). Skip the LLM calls — useful "
        "for verifying every tool fires and the brief is shaped right before spending on Opus.",
    )
    p_audit.set_defaults(func=cmd_audit)

    p_doctor = sub.add_parser(
        "doctor",
        help="Verify all tools, claude/codex auth, corpus, and MCP config.",
    )
    p_doctor.add_argument("--skip-auth", action="store_true", help="Skip the live claude auth check.")
    p_doctor.set_defaults(func=cmd_doctor)

    p_list = sub.add_parser("list", help="Table of audit runs.")
    p_list.add_argument("--root", help="Override audits dir (default: ./audits).")
    p_list.set_defaults(func=cmd_list)

    p_show = sub.add_parser("show", help="Full layout view of one audit run.")
    p_show.add_argument("run_dir")
    p_show.set_defaults(func=cmd_show)

    p_find = sub.add_parser("findings", help="Findings table for one audit run.")
    p_find.add_argument("run_dir")
    p_find.set_defaults(func=cmd_findings)

    p_stat = sub.add_parser("status", help="Live pipeline status for an in-progress run.")
    p_stat.add_argument("run_dir")
    p_stat.add_argument("--follow", "-f", action="store_true", help="Continuous live update.")
    p_stat.add_argument("--interval", type=float, default=1.0, help="Refresh interval seconds.")
    p_stat.set_defaults(func=cmd_status)

    p_pocs = sub.add_parser(
        "pocs",
        help="Show findings with structured foundry_poc + their execution status.",
    )
    p_pocs.add_argument("run_dir")
    p_pocs.add_argument("--verbose", "-v", action="store_true", help="Also print each exploit body.")
    p_pocs.set_defaults(func=cmd_pocs)

    p_replay = sub.add_parser(
        "replay",
        help="Re-execute an on-chain tx in an Anvil sandbox with full call trace.",
    )
    p_replay.add_argument("tx_hash")
    p_replay.add_argument("--chain", default="mainnet")
    p_replay.add_argument("--out", help="Write trace to file instead of stdout.")
    p_replay.set_defaults(func=cmd_replay)

    p_latest = sub.add_parser(
        "latest",
        help="Print path to the latest run dir (for shell pipelines).",
    )
    p_latest.add_argument("--kind", choices=["audit", "scrutinize", "deep-dive", "any"],
                          default="any")
    p_latest.set_defaults(func=cmd_latest)

    p_over = sub.add_parser(
        "overview",
        help="At-a-glance dashboard: corpus + candidate queue + recent audits + submissions.",
    )
    p_over.set_defaults(func=cmd_overview)

    p_dd = sub.add_parser(
        "deep-dive",
        help="Exhaustively analyze ONE target: every function gets its own Opus pass.",
    )
    p_dd.add_argument("target", nargs="?",
                      help="Path to a Solidity project (or single file). Omit if using --from-candidate.")
    p_dd.add_argument("--from-candidate", help="Candidate id from `w3s queue` (resolves "
                                                "to its local_path + scope automatically).")
    p_dd.add_argument("--scope", help="Restrict to .sol files under this subpath.")
    p_dd.add_argument("--out", help="Output dir (default: audits/deep-dive-<name>-<ts>).")
    p_dd.add_argument("--model", default="opus")
    p_dd.add_argument("--max-functions", type=int, default=None,
                      help="Cap the per-function pass (useful for cost-bounded runs).")
    p_dd.add_argument("--skip-cross", action="store_true",
                      help="Skip the cross-function pair-wise analysis.")
    p_dd.add_argument("--max-cross-pairs", type=int, default=30)
    p_dd.add_argument("--no-resume", action="store_true",
                      help="Ignore prior state; start fresh.")
    p_dd.add_argument("--dry-run", action="store_true",
                      help="Decompose + print function list only; no LLM calls.")
    p_dd.add_argument("--materialize-pocs", action="store_true",
                      help="After per-fn pass, convert High/Critical candidate poc_sketches "
                           "into runnable Foundry tests + forge test execute them.")
    p_dd.add_argument("--materialize-min-severity", default="High",
                      choices=["Critical", "High", "Medium"])
    p_dd.set_defaults(func=cmd_deep_dive)

    p_sweep = sub.add_parser(
        "sweep",
        help="Bounty-hunt daily sweep: ingest active contests + Stage-1 rank new candidates.",
    )
    p_sweep.add_argument("--platforms", nargs="+", default=["c4"], help="Platforms to ingest.")
    p_sweep.add_argument("--cache", help="Where to clone repos (default .cache/sweep/).")
    p_sweep.add_argument("--no-clone", action="store_true", help="Skip cloning; register Candidates only.")
    p_sweep.add_argument("--no-stage1", action="store_true", help="Skip the Opus ranking pass.")
    p_sweep.add_argument("--max-new", type=int, default=30,
                         help="Cap how many newly-discovered candidates get Stage-1 ranked per sweep (cost guard).")
    p_sweep.add_argument("--model", default="opus", help="Stage-1 model.")
    p_sweep.set_defaults(func=cmd_sweep)

    p_queue = sub.add_parser("queue", help="Show ranked candidate queue.")
    p_queue.add_argument("--platform", help="Filter to one platform.")
    p_queue.add_argument("--status", help="Filter to one triage_status.")
    p_queue.add_argument("--min-score", type=float, default=None)
    p_queue.add_argument("--limit", type=int, default=30)
    p_queue.add_argument("--detail", type=int, default=0, help="Show top_suspects + skip_reasons for top N.")
    p_queue.set_defaults(func=cmd_queue)

    p_submit = sub.add_parser(
        "submit",
        help="Export per-platform submission templates for an audit run.",
    )
    p_submit.add_argument("run_dir")
    p_submit.add_argument("--candidate-id", required=True)
    p_submit.add_argument("--platforms", nargs="+", default=["c4"])
    p_submit.add_argument("--min-severity", default="Medium")
    p_submit.add_argument("--only-reproduced", action="store_true")
    p_submit.set_defaults(func=cmd_submit)

    p_scr = sub.add_parser(
        "scrutinize",
        help="Maximum-depth pipeline: audit + deep-dive + materialize-pocs + filter on one target.",
    )
    p_scr.add_argument("target", nargs="?",
                       help="Path to .sol / project dir, or 0x-address. "
                            "Omit if using --from-candidate.")
    p_scr.add_argument("--from-candidate", help="Candidate id from `w3s queue` (resolves "
                                                 "to its local_path + scope automatically).")
    p_scr.add_argument("--chain", default="mainnet")
    p_scr.add_argument("--scope")
    p_scr.add_argument("--out", help="Override scrutinize run dir.")
    p_scr.add_argument("--skip-audit", action="store_true")
    p_scr.add_argument("--skip-deep-dive", action="store_true")
    p_scr.add_argument("--skip-cross-fn", action="store_true")
    p_scr.add_argument("--skip-materialize", action="store_true")
    p_scr.add_argument("--skip-filter", action="store_true")
    p_scr.add_argument("--single-model", action="store_true",
                       help="Audit phase uses single model only (skip codex + reconciler).")
    p_scr.add_argument("--no-audit-pocs", action="store_true",
                       help="Skip foundry_poc scaffolding in the audit phase (deep-dive still does).")
    p_scr.add_argument("--max-functions", type=int, default=None)
    p_scr.add_argument("--materialize-min-severity", default="High",
                       choices=["Critical", "High", "Medium"])
    p_scr.add_argument("--model", default="opus")
    p_scr.add_argument("--dry-run", action="store_true",
                       help="Print decomposition + estimated LLM message budget + wall time, "
                            "without spending anything. Run this first to size up cost.")
    p_scr.set_defaults(func=cmd_scrutinize)

    p_syn = sub.add_parser(
        "synthesize",
        help="Distill a cluster of corpus entries on TOPIC into one dense synthesis note.",
    )
    p_syn.add_argument("topic", help='e.g. "flash loan oracle manipulation"')
    p_syn.add_argument("--seed-query", help="Override corpus search query (defaults to topic).")
    p_syn.add_argument("--slug", help="Override filename slug.")
    p_syn.add_argument("--model", default="opus")
    p_syn.add_argument("--no-reindex", action="store_true")
    p_syn.add_argument("--timeout", type=int, default=1800)
    p_syn.set_defaults(func=cmd_synthesize)

    p_subs = sub.add_parser(
        "submissions",
        help="Show the submissions log as a filtered table.",
    )
    p_subs.add_argument("--candidate-id", help="Filter to one candidate.")
    p_subs.add_argument("--outcome", choices=["pending", "accepted", "duplicate", "rejected", "withdrawn"])
    p_subs.add_argument("--platform", choices=["c4", "sherlock", "cantina", "immunefi"])
    p_subs.add_argument("--limit", type=int, default=30)
    p_subs.set_defaults(func=cmd_submissions)

    p_auto = sub.add_parser(
        "autoscrutinize",
        help="Pick the top suggested candidate + scrutinize it. One-command bounty hunt.",
    )
    p_auto.add_argument("--top", type=int, default=1, help="Pool size to pick from (default 1=greedy).")
    p_auto.add_argument("--platform")
    p_auto.add_argument("--min-stage1", type=float, default=None)
    p_auto.add_argument("--out", help="Override scrutinize run dir.")
    p_auto.add_argument("--model", default="opus")
    p_auto.add_argument("--max-functions", type=int, default=None)
    p_auto.add_argument("--materialize-min-severity", default="High",
                        choices=["Critical", "High", "Medium"])
    p_auto.add_argument("--single-model", action="store_true")
    p_auto.add_argument("--no-audit-pocs", action="store_true")
    p_auto.add_argument("--skip-audit", action="store_true")
    p_auto.add_argument("--skip-deep-dive", action="store_true")
    p_auto.add_argument("--skip-cross-fn", action="store_true")
    p_auto.add_argument("--skip-materialize", action="store_true")
    p_auto.add_argument("--skip-filter", action="store_true")
    p_auto.add_argument("--dry-run-first", action="store_true",
                        help="Print plan BEFORE running for real.")
    p_auto.add_argument("--dry-run", action="store_true",
                        help="Print plan and exit (no LLM calls).")
    p_auto.set_defaults(func=cmd_autoscrutinize)

    p_digest = sub.add_parser(
        "digest",
        help="What did the system do in the last N hours? (overnight activity summary)",
    )
    p_digest.add_argument("--hours", type=float, default=24, help="Window size (default 24h).")
    p_digest.add_argument("--json", action="store_true", help="Emit JSON instead of rendered tables.")
    p_digest.set_defaults(func=cmd_digest)

    p_suggest = sub.add_parser(
        "suggest",
        help="Pick the best candidate(s) to scrutinize next, ranked by composite score.",
    )
    p_suggest.add_argument("-n", "--top", type=int, default=5)
    p_suggest.add_argument("--platform")
    p_suggest.add_argument("--min-stage1", type=float, default=None)
    p_suggest.add_argument("--include-audited", action="store_true")
    p_suggest.add_argument("--include-closed", action="store_true")
    p_suggest.set_defaults(func=cmd_suggest)

    p_corpus = sub.add_parser("corpus", help="Browse the corpus (search / read / stats).")
    corpus_sub = p_corpus.add_subparsers(dest="corpus_cmd", required=True)
    p_cs = corpus_sub.add_parser("stats", help="Counts by source / severity / vuln_class.")
    p_cs.set_defaults(func=cmd_corpus)
    p_cq = corpus_sub.add_parser("search", help="Full-text search across corpus.")
    p_cq.add_argument("query")
    p_cq.add_argument("--vuln-class", action="append")
    p_cq.add_argument("--severity", action="append")
    p_cq.add_argument("--source", action="append")
    p_cq.add_argument("--top-k", type=int, default=10)
    p_cq.set_defaults(func=cmd_corpus)
    p_cr = corpus_sub.add_parser("read", help="Read a single corpus entry.")
    p_cr.add_argument("entry_id")
    p_cr.add_argument("--meta-only", action="store_true", help="Skip the body, show only frontmatter.")
    p_cr.set_defaults(func=cmd_corpus)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
