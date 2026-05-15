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


def run_one(entry_dir: Path, model: str = "opus", multimodel: bool = False) -> dict:
    expected_path = entry_dir / "expected-finding.md"
    expected = load_expected(expected_path)

    source_dir = entry_dir / "source"
    if not source_dir.is_dir():
        raise SystemExit(f"{entry_dir}: missing source/ directory")

    started = datetime.now(timezone.utc).isoformat()
    if multimodel:
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

    mode = "MULTIMODEL (claude+codex+reconciler)" if args.multimodel else "single-model (claude)"
    print(f"Running {len(entries)} eval entries — mode={mode}, model={args.model}\n")
    rows = []
    for e in entries:
        print(f"=== {e.name} ===")
        try:
            row = run_one(e, model=args.model, multimodel=args.multimodel)
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
