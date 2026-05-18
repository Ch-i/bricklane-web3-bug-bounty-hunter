"""Run the eval benchmark over one or more entries.

Usage:
    uv run python -m eval.run                            # all entries under eval/historical/
    uv run python -m eval.run --entry euler-donate-2023  # one entry
    uv run python -m eval.run --root eval/c4-public      # different benchmark root
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from eval.driver import drive_audit, drive_audit_multimodel
from eval.scoring import load_expected, load_findings, score_entry
from harness.corpus import REPO_ROOT

DEFAULT_ROOT = REPO_ROOT / "eval" / "historical"
SCORES_PATH = REPO_ROOT / "eval" / "scores.jsonl"


def list_entries(root: Path) -> list[Path]:
    return sorted(p for p in root.iterdir() if p.is_dir() and (p / "expected-finding.md").exists())


def _merge_dd_into_findings(audit_run_dir: Path, dd_dir: Path) -> None:
    """For eval scrutinize mode: pull deep-dive High/Critical candidates into
    the audit's findings.json so the scorer sees the full set."""
    pf = dd_dir / "per-function.jsonl"
    findings_path = audit_run_dir / "findings.json"
    if not pf.exists() or not findings_path.exists():
        return
    data = json.loads(findings_path.read_text())
    findings = data if isinstance(data, list) else data.get("findings", [])
    seen = {f.get("title") for f in findings}
    sev_rank = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Info": 4}
    for line in pf.read_text().splitlines():
        if not line.strip():
            continue
        try:
            fn = json.loads(line)
        except json.JSONDecodeError:
            continue
        file_path = fn.get("function_id", "").split("::")[0] or "?"
        for v in (fn.get("candidate_vulnerabilities") or []):
            if sev_rank.get(v.get("severity"), 99) > 1:  # High threshold
                continue
            title = v.get("title", "?")
            if title in seen:
                continue
            seen.add(title)
            findings.append({
                "title": title,
                "severity": v.get("severity"),
                "location": [{"file": file_path, "line_start": 1}],
                "description": v.get("description", "") or title,
                "impact": v.get("impact", "?"),
                "recommendation": "(see deep-dive)",
                "citations": [],
                "novel": True,
                "confidence": v.get("confidence", "medium"),
                "discovered_by": "claude-deep-dive",
                "poc_status": "not-attempted",
            })
    findings_path.write_text(json.dumps(findings, indent=2))


def run_one(entry_dir: Path, model: str = "opus", multimodel: bool = False,
            scrutinize_mode: bool = False) -> dict:
    expected_path = entry_dir / "expected-finding.md"
    expected = load_expected(expected_path)

    source_dir = entry_dir / "source"
    if not source_dir.is_dir():
        raise SystemExit(f"{entry_dir}: missing source/ directory")

    started = datetime.now(timezone.utc).isoformat()
    if scrutinize_mode:
        # Scrutinize mode: run full audit + deep-dive + filter pipeline,
        # then aggregate findings into a single list for scoring.
        # Wraps drive_audit_multimodel + deep_dive for the harshest test.
        from harness import scrutinize as _scrut
        from harness import deep_dive as _dd

        # Drive the audit phase first to get a real run_dir
        drive = drive_audit_multimodel(
            target=source_dir,
            exclude_ids=expected.exclude_corpus_ids,
            claude_model=model,
        )
        if drive.run_dir and drive.run_dir.exists():
            # Run deep-dive on the same source — outputs to a sibling dir
            dd_out = drive.run_dir.parent / f"{drive.run_dir.name}-deep-dive"
            try:
                _dd.run_deep_dive(
                    source_dir, out_dir=dd_out, model=model,
                    skip_cross=True,  # skip cross-pair to keep eval cheap
                    progress_callback=None,
                )
                # Merge deep-dive high-sev candidates into findings.json
                _merge_dd_into_findings(drive.run_dir, dd_out)
            except Exception:  # noqa: BLE001
                pass  # deep-dive failure shouldn't break the audit scoring
    elif multimodel:
        drive = drive_audit_multimodel(
            target=source_dir,
            exclude_ids=expected.exclude_corpus_ids,
            claude_model=model,
        )
    else:
        drive = drive_audit(
            target=source_dir,
            exclude_ids=expected.exclude_corpus_ids,
            model=model,
        )

    # If drive_audit failed to produce findings, still record the attempt.
    if not (drive.run_dir / "findings.json").exists():
        return {
            "entry_id": expected.id,
            "timestamp": started,
            "run_dir": str(drive.run_dir),
            "passed": False,
            "reasoning": f"DRIVER ERROR — {drive.parse_error or 'no findings.json produced'}",
            "matched_findings": [],
            "all_finding_titles": [],
            "total_findings": 0,
            "disqualifying_hit": False,
            "corpus_snapshot": "unknown",
        }

    findings = load_findings(drive.run_dir)
    prep = json.loads((drive.run_dir / "prep.json").read_text())
    corpus_sha = prep.get("corpus_snapshot", "untracked")

    result = score_entry(expected, findings, drive.run_dir, corpus_sha)
    if scrutinize_mode:
        result.mode = "scrutinize"
    elif multimodel:
        result.mode = "multimodel"
    else:
        result.mode = "single"
    return result.model_dump()


def append_scores(rows: list[dict]) -> None:
    SCORES_PATH.parent.mkdir(parents=True, exist_ok=True)
    with SCORES_PATH.open("a") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(DEFAULT_ROOT))
    parser.add_argument("--entry", help="Run only the named entry (directory name).")
    parser.add_argument("--model", default="opus", help="Model for the Claude auditor CLI.")
    parser.add_argument(
        "--multimodel",
        action="store_true",
        help="Run Claude + Codex auditors in parallel then reconcile. ~2x cost.",
    )
    parser.add_argument(
        "--scrutinize",
        action="store_true",
        help="Scrutinize mode: full audit + deep-dive pipeline, merging deep-dive "
             "High/Critical candidates into findings.json before scoring. The harshest "
             "recall test of the system. Implies --multimodel for the audit phase.",
    )
    parser.add_argument(
        "--no-append",
        action="store_true",
        help="Don't write to scores.jsonl (useful for dev runs).",
    )
    args = parser.parse_args(argv)

    root = Path(args.root)
    if not root.exists():
        raise SystemExit(f"eval root does not exist: {root}")

    entries = list_entries(root)
    if args.entry:
        entries = [e for e in entries if e.name == args.entry]
        if not entries:
            raise SystemExit(f"no entry named {args.entry} under {root}")

    if not entries:
        print(f"no eval entries found under {root}", file=sys.stderr)
        return 1

    if args.scrutinize:
        mode = "SCRUTINIZE (audit + deep-dive merged)"
    elif args.multimodel:
        mode = "MULTIMODEL (claude+codex+reconciler)"
    else:
        mode = "single-model (claude)"
    print(f"Running {len(entries)} eval entries — mode={mode}, model={args.model}\n")
    rows = []
    for e in entries:
        print(f"=== {e.name} ===")
        try:
            row = run_one(e, model=args.model, multimodel=args.multimodel,
                          scrutinize_mode=args.scrutinize)
        except Exception as ex:  # noqa: BLE001
            row = {
                "entry_id": e.name,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "passed": False,
                "reasoning": f"FATAL — {type(ex).__name__}: {ex}",
                "run_dir": None,
                "matched_findings": [],
                "all_finding_titles": [],
                "total_findings": 0,
                "disqualifying_hit": False,
                "corpus_snapshot": "unknown",
            }
        rows.append(row)
        status = "PASS" if row["passed"] else "FAIL"
        print(f"  [{status}] {row['reasoning']}\n")

    passed = sum(1 for r in rows if r["passed"])
    print(f"Recall: {passed}/{len(rows)} ({passed / len(rows):.0%})")

    if not args.no_append:
        append_scores(rows)
        print(f"Appended {len(rows)} rows to {SCORES_PATH.relative_to(REPO_ROOT)}")

    # Exit non-zero if anything failed — useful for CI.
    return 0 if passed == len(rows) else 2


if __name__ == "__main__":
    sys.exit(main())
