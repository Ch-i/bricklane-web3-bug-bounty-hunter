"""`w3s digest` — what the system did in the last N hours.

A time-windowed activity report. Designed for the user who runs an
overnight loop and wants a 5-second skim with breakfast.

Sections:
  * **Sweep delta** — new candidates ingested in the window
  * **Triage delta** — Stage 1 ranks computed in the window
  * **Audits** — new audit run dirs, with finding counts
  * **Scrutinize runs** — new scrutinize dirs + their master reports
  * **Submissions** — entries added to submissions.jsonl
  * **Corpus growth** — new synthesis notes + crawl ingests

The window is calculated from `now - <hours>` (default 24h).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from harness.corpus import REPO_ROOT

console = Console()


def _parse_iso(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


def _since(hours: float) -> datetime:
    return datetime.now(timezone.utc) - timedelta(hours=hours)


def _new_candidates(since: datetime) -> list[dict]:
    """Candidates whose sourced_at or last_triaged_at fall in window."""
    from harness import candidates as cand_store

    fresh = []
    for c in cand_store.load_all():
        sourced = _parse_iso(c.sourced_at)
        triaged = _parse_iso(c.last_triaged_at)
        is_new = sourced is not None and sourced >= since
        was_triaged = triaged is not None and triaged >= since
        if is_new or was_triaged:
            fresh.append({
                "id": c.id,
                "platform": c.platform,
                "title": c.title,
                "payout_max_usd": c.payout_max_usd,
                "triage_score": c.triage_score,
                "triage_status": c.triage_status,
                "is_new": is_new,
                "was_triaged": was_triaged,
                "local_path": c.local_path,
            })
    fresh.sort(key=lambda x: x.get("triage_score") or 0, reverse=True)
    return fresh


def _recent_audit_runs(since: datetime) -> list[dict]:
    """Audit runs whose dir mtime falls in window."""
    audits_root = REPO_ROOT / "audits"
    if not audits_root.exists():
        return []
    out = []
    for p in audits_root.iterdir():
        if not p.is_dir():
            continue
        try:
            mtime = datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc)
        except OSError:
            continue
        if mtime < since:
            continue

        # Distinguish kinds
        is_scrutinize = p.name.startswith("scrutinize-")
        is_deep_dive = p.name.startswith("deep-dive-")
        is_audit = (p / "prep.json").exists()
        if not (is_scrutinize or is_deep_dive or is_audit):
            continue

        meta = {
            "name": p.name,
            "kind": "scrutinize" if is_scrutinize else ("deep-dive" if is_deep_dive else "audit"),
            "mtime": mtime.isoformat(),
            "n_findings": None,
            "has_pocs": False,
            "has_master_report": False,
        }
        try:
            if (p / "findings.json").exists():
                fs = json.loads((p / "findings.json").read_text())
                fs_list = fs if isinstance(fs, list) else fs.get("findings", [])
                meta["n_findings"] = len(fs_list)
                meta["has_pocs"] = any(f.get("poc_status") == "reproduced" for f in fs_list)
            # Deep-dive runs surface per-function candidate counts
            if (p / "per-function.jsonl").exists():
                n_fn = 0
                total_vulns = 0
                high_crit = 0
                for line in (p / "per-function.jsonl").read_text().splitlines():
                    if not line.strip():
                        continue
                    try:
                        fn = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    n_fn += 1
                    for v in (fn.get("candidate_vulnerabilities") or []):
                        total_vulns += 1
                        if v.get("severity") in ("Critical", "High"):
                            high_crit += 1
                meta["n_functions"] = n_fn
                meta["n_candidates"] = total_vulns
                meta["n_high_crit"] = high_crit
                # If no findings.json, expose candidates as the headline number
                if meta["n_findings"] is None:
                    meta["n_findings"] = total_vulns
        except (json.JSONDecodeError, OSError):
            pass
        if (p / "scrutinize-report.md").exists():
            meta["has_master_report"] = True
        if (p / "invariants.md").exists():
            meta["has_invariants"] = True
        out.append(meta)
    out.sort(key=lambda m: m["mtime"], reverse=True)
    return out


def _new_submissions(since: datetime) -> list[dict]:
    """submissions.jsonl rows whose submitted_at falls in window."""
    log_path = REPO_ROOT / "submissions" / "submissions.jsonl"
    if not log_path.exists():
        return []
    out = []
    for line in log_path.read_text().splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        ts = _parse_iso(row.get("submitted_at") or row.get("timestamp"))
        if ts and ts >= since:
            out.append(row)
    return out


def _new_corpus_entries(since: datetime) -> dict:
    """Corpus entries (synthesis + ingests) added in window."""
    synth_dir = REPO_ROOT / "corpus" / "synthesis"
    synth_notes = []
    if synth_dir.exists():
        for p in synth_dir.glob("*.md"):
            try:
                mtime = datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc)
                if mtime >= since:
                    # Extract title from frontmatter
                    text = p.read_text()
                    title_match = re.search(r"^title:\s*\"?(.+?)\"?\s*$", text, re.MULTILINE)
                    title = title_match.group(1) if title_match else p.stem
                    synth_notes.append({"slug": p.stem, "title": title,
                                        "lines": len(text.splitlines())})
            except OSError:
                continue

    # Corpus ingests: count entries in by checking corpus.db's ingested_at
    ingested = 0
    by_source: dict[str, int] = {}
    try:
        from harness.corpus import connect
        with connect() as conn:
            rows = conn.execute(
                "SELECT source, ingested_at FROM entries WHERE ingested_at >= ?",
                (since.isoformat(),),
            ).fetchall()
        for r in rows:
            ingested += 1
            by_source[r["source"]] = by_source.get(r["source"], 0) + 1
    except Exception:  # noqa: BLE001
        pass

    return {"synthesis_notes": synth_notes, "ingested_count": ingested, "by_source": by_source}


def generate_digest(hours: float = 24) -> dict:
    """Return a JSON-shaped dict summarizing all activity in the window."""
    since = _since(hours)
    return {
        "window_hours": hours,
        "since": since.isoformat(),
        "now": datetime.now(timezone.utc).isoformat(),
        "candidates": _new_candidates(since),
        "audit_runs": _recent_audit_runs(since),
        "submissions": _new_submissions(since),
        "corpus": _new_corpus_entries(since),
    }


def render_digest(digest: dict) -> None:
    h = digest["window_hours"]
    console.print(Panel(
        f"Activity in the last [bold]{h}[/bold] hours\n"
        f"Window: {digest['since']}  →  {digest['now']}",
        title=f"w3s digest", border_style="cyan",
    ))

    # === Candidates ===
    cands = digest["candidates"]
    new_count = sum(1 for c in cands if c["is_new"])
    triaged_count = sum(1 for c in cands if c["was_triaged"])
    console.print(f"\n[bold cyan]Candidates[/bold cyan]: {new_count} new ingested, "
                  f"{triaged_count} Stage-1 triaged ({len(cands)} touched total)")
    if cands:
        ct = Table(show_header=True, header_style="bold")
        ct.add_column("Δ", width=3)
        ct.add_column("Stage1", justify="right")
        ct.add_column("ID", style="cyan")
        ct.add_column("Platform", style="dim")
        ct.add_column("Title", overflow="fold", max_width=40)
        ct.add_column("Payout", justify="right")
        for c in cands[:15]:
            delta = ("[green]+[/green]" if c["is_new"] else "") + ("[yellow]△[/yellow]" if c["was_triaged"] else "")
            s1 = f"{c['triage_score']:.1f}" if c["triage_score"] else "—"
            payout = f"${c['payout_max_usd']:,}" if c["payout_max_usd"] else "—"
            ct.add_row(delta, s1, c["id"][:35], c["platform"], c["title"][:40], payout)
        console.print(ct)
        if len(cands) > 15:
            console.print(f"[dim]  … and {len(cands) - 15} more[/dim]")

    # === Audit runs ===
    runs = digest["audit_runs"]
    if runs:
        console.print(f"\n[bold cyan]Audit runs[/bold cyan]: {len(runs)} new")
        rt = Table(show_header=True, header_style="bold")
        rt.add_column("Kind", style="dim")
        rt.add_column("Run", style="cyan", overflow="fold", max_width=46)
        rt.add_column("#Fn/Findings", justify="right")
        rt.add_column("H/C", justify="right")
        rt.add_column("PoCs?", justify="center")
        rt.add_column("Report?", justify="center")
        for r in runs[:10]:
            # For deep-dive, show "N fn → M cand"; for audit, show "M findings"
            if r["kind"] == "deep-dive" and r.get("n_functions") is not None:
                count_cell = f"{r['n_functions']}fn→{r.get('n_candidates', 0)}"
            else:
                count_cell = str(r["n_findings"] if r["n_findings"] is not None else "—")
            hc = str(r.get("n_high_crit", "")) if r.get("n_high_crit") is not None else ""
            rt.add_row(
                r["kind"],
                r["name"],
                count_cell,
                hc,
                "✓" if r["has_pocs"] else "—",
                "✓" if r["has_master_report"] or r.get("has_invariants") else "—",
            )
        console.print(rt)

    # === Submissions ===
    subs = digest["submissions"]
    if subs:
        console.print(f"\n[bold cyan]Submissions[/bold cyan]: {len(subs)} filed")
        st = Table(show_header=True, header_style="bold")
        st.add_column("Platform")
        st.add_column("Title", overflow="fold", max_width=40)
        st.add_column("Severity")
        st.add_column("Outcome")
        for s in subs:
            st.add_row(
                s.get("platform", "?"),
                s.get("title", "?")[:50],
                s.get("severity", "?"),
                s.get("outcome", "?"),
            )
        console.print(st)

    # === Corpus ===
    corpus = digest["corpus"]
    synth_n = len(corpus["synthesis_notes"])
    ing_n = corpus["ingested_count"]
    if synth_n or ing_n:
        console.print(f"\n[bold cyan]Corpus growth[/bold cyan]: "
                      f"{synth_n} new synthesis notes, {ing_n} ingested entries")
        if corpus["synthesis_notes"]:
            for n in corpus["synthesis_notes"]:
                console.print(f"  [green]+[/green] {n['title']} [dim]({n['lines']}L)[/dim]")
        if corpus["by_source"]:
            sources = ", ".join(f"{k}={v}" for k, v in sorted(corpus["by_source"].items()))
            console.print(f"  Sources: {sources}")

    # === Nothing happened ===
    nothing = (not cands and not runs and not subs and not synth_n and not ing_n)
    if nothing:
        console.print(f"\n[dim]No activity in the last {h} hours. "
                      f"Run `w3s sweep` to ingest, then `w3s suggest` to pick a target.[/dim]")
        return

    # === Next steps — actionable hints based on the digest ===
    actions = []
    # Unranked candidates → suggest Stage 1 ranking
    unranked = sum(1 for c in cands if c["is_new"] and c["triage_score"] is None)
    if unranked >= 5:
        actions.append(
            f"[yellow]{unranked} new candidates have no Stage-1 rank.[/yellow] "
            f"Run [cyan]w3s sweep --max-new {min(unranked, 30)}[/cyan] to score them, "
            f"or [cyan]w3s suggest[/cyan] to pick from current queue."
        )
    # Deep-dive runs without scrutinize wrap → suggest scrutinize
    dd_only = [r for r in runs if r["kind"] == "deep-dive" and not r.get("has_master_report")]
    if dd_only:
        actions.append(
            f"[yellow]{len(dd_only)} deep-dive run(s) lack a master scrutinize report.[/yellow] "
            f"Run [cyan]w3s scrutinize --from-candidate <id>[/cyan] for the full pipeline."
        )
    # Scrutinize runs without submissions
    scrut_runs = [r for r in runs if r["kind"] == "scrutinize"]
    if scrut_runs and not subs:
        actions.append(
            f"[yellow]{len(scrut_runs)} scrutinize run(s) completed but 0 submissions filed.[/yellow] "
            f"Review [cyan]$(w3s latest --kind scrutinize)/scrutinize-report.md[/cyan] and "
            f"[cyan]w3s submit[/cyan] the ACCEPT'd findings."
        )
    if actions:
        console.print("\n[bold cyan]Next steps[/bold cyan]")
        for a in actions:
            console.print(f"  • {a}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hours", type=float, default=24,
                        help="Window size (default: 24h).")
    parser.add_argument("--json", action="store_true",
                        help="Emit JSON instead of the rendered table.")
    args = parser.parse_args(argv)

    digest = generate_digest(hours=args.hours)
    if args.json:
        print(json.dumps(digest, indent=2))
    else:
        render_digest(digest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
