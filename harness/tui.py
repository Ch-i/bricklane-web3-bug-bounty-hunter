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


def render_show(run_dir: Path) -> Group:
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

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

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
