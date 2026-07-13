"""Per-platform submission template exporter + status log.

Each platform's portal expects markdown in a specific shape. We emit one
file per (finding, platform) pair so you can paste directly into the
submission form.

State is logged to `submissions/submissions.jsonl` (append-only):

    {finding_id, run_dir, candidate_id, platform, submitted_at,
     platform_submission_id, outcome, payout_usd, notes}

Outcomes are filled in by hand (or by `w3s submission update`) after the
platform's judging completes. Over time, this becomes calibration data
for the Stage 1 ranker and audit prompts.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from harness.corpus import REPO_ROOT
from harness.schema import Finding

SUBMISSIONS_DIR = REPO_ROOT / "submissions"
SUBMISSIONS_LOG = SUBMISSIONS_DIR / "submissions.jsonl"

Platform = Literal["c4", "sherlock", "cantina", "immunefi"]
Outcome = Literal["pending", "accepted", "duplicate", "rejected", "withdrawn"]


@dataclass
class SubmissionRecord:
    id: str                        # f"{candidate_id}--{finding_slug}--{platform}"
    candidate_id: str
    finding_title: str
    finding_severity: str
    run_dir: str
    platform: Platform
    template_path: str
    submitted_at: str | None = None
    platform_submission_id: str | None = None
    outcome: Outcome = "pending"
    payout_usd: int | None = None
    notes: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).replace(microsecond=0).isoformat())


# ---------------------------------------------------------------------------
# Per-platform templates
# ---------------------------------------------------------------------------


def _severity_letter(sev: str) -> str:
    return {"Critical": "H", "High": "H", "Medium": "M", "Low": "L", "Informational": "QA", "Gas": "G"}.get(sev, "?")


def _strip(s: str | None) -> str:
    return (s or "").strip()


def _format_loc(finding: Finding) -> str:
    out = []
    for loc in finding.location:
        line_end = f"-L{loc.line_end}" if loc.line_end else ""
        out.append(f"- `{loc.file}#L{loc.line_start}{line_end}`")
    return "\n".join(out) if out else "_(no locations)_"


def _format_filter_block(filter_info: dict | None) -> str:
    """If the finding went through the Mythos filter, surface the verdict
    in the submission template — helps the submitter know what was already
    checked (and gives the judge confidence)."""
    if not filter_info:
        return ""
    verdict = filter_info.get("verdict", "")
    rationale = filter_info.get("rationale", "")
    if not verdict:
        return ""
    sym = {"ACCEPT": "✅", "DOWNGRADE": "↓", "REJECT": "✗", "ERROR": "!"}.get(verdict, "·")
    return (
        f"\n> **Internal review:** {sym} `{verdict}` — {rationale}\n"
        f"> _(Verdict from Bricklane's filter agent — second-opinion pass.)_\n"
    )


def _format_foundry_poc(finding: Finding, run_dir: Path) -> str:
    if not finding.foundry_poc:
        return ""
    test_path = finding.poc_artifacts.get("test_path", "")
    poc = finding.foundry_poc
    body = (
        "```solidity\n"
        f"// {test_path or 'audits/<run>/poc/<file>.t.sol'}\n"
        f"// --- setUp() body ---\n{poc.setup}\n\n"
        f"// --- test body ---\n{poc.exploit}\n\n"
        f"// --- assertion (passes when bug is reproduced) ---\n{poc.assertion}\n"
        "```\n"
    )
    status = finding.poc_status
    sign = {"reproduced": "✅", "unconfirmed": "❓", "compile-error": "⚠️"}.get(status, "·")
    return (
        f"## Proof of Concept\n\n"
        f"_PoC status: {sign} **{status}**_\n\n"
        f"{body}\n"
    )


# -------- C4 template --------


def render_c4(finding: Finding, candidate_id: str, run_dir: Path, *,
              filter_info: dict | None = None) -> str:
    """Code4rena submission format. Markdown, with severity in title."""
    sev_letter = _severity_letter(finding.severity)
    poc_block = _format_foundry_poc(finding, run_dir)
    filter_block = _format_filter_block(filter_info)
    cites = ", ".join(f"`{c}`" for c in finding.citations) if finding.citations else "_(novel)_"
    return f"""\
# [{sev_letter}] {finding.title}
{filter_block}
## Lines of code

{_format_loc(finding)}

## Vulnerability details

{_strip(finding.description)}

## Impact

{_strip(finding.impact)}

{poc_block}
## Recommended mitigation steps

{_strip(finding.recommendation)}

## Tools used

* Bricklane Web3 Bug Bounty Hunter multi-model audit harness (Claude + Codex + reconciler)
* Slither, Aderyn, Foundry
* Grounded against corpus entries: {cites}

---

_Auto-generated from `{run_dir.name}/findings.json`; manually edit before submission._
"""


# -------- Sherlock template --------


def render_sherlock(finding: Finding, candidate_id: str, run_dir: Path, *,
                    filter_info: dict | None = None) -> str:
    """Sherlock submission shape."""
    poc_block = _format_foundry_poc(finding, run_dir)
    filter_block = _format_filter_block(filter_info)
    return f"""\
# {finding.title}

**Severity:** {finding.severity}
{filter_block}

## Summary

{_strip(finding.description)}

## Vulnerability Detail

{_strip(finding.description)}

## Impact

{_strip(finding.impact)}

## Code Snippet

{_format_loc(finding)}

{poc_block}
## Tool used

Bricklane + Foundry

## Recommendation

{_strip(finding.recommendation)}
"""


# -------- Cantina template --------


def render_cantina(finding: Finding, candidate_id: str, run_dir: Path, *,
                   filter_info: dict | None = None) -> str:
    """Cantina prefers structured markdown; close to Sherlock's shape."""
    poc_block = _format_foundry_poc(finding, run_dir)
    filter_block = _format_filter_block(filter_info)
    return f"""\
---
title: "{finding.title}"
severity: {finding.severity}
---
{filter_block}

## Description

{_strip(finding.description)}

## Impact

{_strip(finding.impact)}

## Affected Code

{_format_loc(finding)}

{poc_block}
## Recommendation

{_strip(finding.recommendation)}
"""


# -------- Immunefi template --------


def render_immunefi(finding: Finding, candidate_id: str, run_dir: Path, *,
                    filter_info: dict | None = None) -> str:
    """Immunefi requires PoC for High/Critical; their portal has its own template
    but markdown lifts cleanly."""
    poc_block = _format_foundry_poc(finding, run_dir)
    filter_block = _format_filter_block(filter_info)
    return f"""\
# {finding.title}

**Severity:** {finding.severity}
**Target:** {candidate_id}
{filter_block}

## Brief / Intro

{_strip(finding.description)}

## Vulnerability Details

{_strip(finding.description)}

## Impact Details

{_strip(finding.impact)}

## Recommendation

{_strip(finding.recommendation)}

{poc_block}

## References

{', '.join(finding.citations) if finding.citations else '(none)'}
"""


_RENDERERS = {
    "c4": render_c4,
    "sherlock": render_sherlock,
    "cantina": render_cantina,
    "immunefi": render_immunefi,
}


# ---------------------------------------------------------------------------
# Log
# ---------------------------------------------------------------------------


def _slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60] or "finding"


def load_log() -> list[SubmissionRecord]:
    if not SUBMISSIONS_LOG.exists():
        return []
    by_id: dict[str, SubmissionRecord] = {}
    with SUBMISSIONS_LOG.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            r = SubmissionRecord(**d)
            by_id[r.id] = r
    return list(by_id.values())


def append_log(records: list[SubmissionRecord]) -> None:
    SUBMISSIONS_LOG.parent.mkdir(parents=True, exist_ok=True)
    with SUBMISSIONS_LOG.open("a") as f:
        for r in records:
            f.write(json.dumps(asdict(r)) + "\n")


# ---------------------------------------------------------------------------
# Top-level: emit submission templates for one audit run
# ---------------------------------------------------------------------------


def export_run(
    run_dir: Path,
    *,
    candidate_id: str,
    platforms: list[Platform],
    min_severity: str = "Medium",
    only_reproduced: bool = False,
) -> list[SubmissionRecord]:
    """Read findings.json from the run dir; emit per-platform templates.

    Returns the new SubmissionRecords; caller appends to the log.
    """
    findings_path = run_dir / "findings.json"
    if not findings_path.exists():
        raise FileNotFoundError(f"no findings.json in {run_dir}")
    data = json.loads(findings_path.read_text())
    if isinstance(data, dict) and "findings" in data:
        data = data["findings"]
    # Parse Finding objects but ALSO keep the raw dict so we can surface
    # filter verdicts + extras the schema doesn't store (set by scrutinize).
    findings_pairs: list[tuple[Finding, dict]] = []
    for raw in data:
        try:
            findings_pairs.append((Finding.model_validate(raw), raw))
        except Exception:  # noqa: BLE001
            continue

    sev_rank = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Informational": 4, "Gas": 5}
    min_rank = sev_rank.get(min_severity, 99)

    exported: list[SubmissionRecord] = []
    out_root = SUBMISSIONS_DIR / datetime.now(timezone.utc).strftime("%Y-%m-%d") / candidate_id
    out_root.mkdir(parents=True, exist_ok=True)

    for finding, raw in findings_pairs:
        if sev_rank.get(finding.severity, 99) > min_rank:
            continue
        if only_reproduced and finding.poc_status not in ("reproduced",):
            continue
        filter_info = raw.get("filter") or {}
        slug = _slugify(finding.title)
        for platform in platforms:
            renderer = _RENDERERS.get(platform)
            if not renderer:
                continue
            out_path = out_root / f"{slug}--{platform}.md"
            out_path.write_text(renderer(finding, candidate_id, run_dir, filter_info=filter_info))
            try:
                template_path_str = str(out_path.relative_to(REPO_ROOT))
            except ValueError:
                template_path_str = str(out_path)
            try:
                run_dir_str = str(run_dir.relative_to(REPO_ROOT))
            except ValueError:
                run_dir_str = str(run_dir)
            rec = SubmissionRecord(
                id=f"{candidate_id}--{slug}--{platform}",
                candidate_id=candidate_id,
                finding_title=finding.title,
                finding_severity=finding.severity,
                run_dir=run_dir_str,
                platform=platform,
                template_path=template_path_str,
            )
            exported.append(rec)

    if exported:
        append_log(exported)
    return exported


def update_outcome(
    submission_id: str,
    *,
    outcome: Outcome,
    payout_usd: int | None = None,
    notes: str = "",
    platform_submission_id: str | None = None,
) -> SubmissionRecord | None:
    """Append a new row reflecting the updated outcome."""
    by_id = {r.id: r for r in load_log()}
    rec = by_id.get(submission_id)
    if not rec:
        return None
    rec.outcome = outcome
    if payout_usd is not None:
        rec.payout_usd = payout_usd
    if notes:
        rec.notes = (rec.notes + " | " + notes).strip(" |")
    if platform_submission_id:
        rec.platform_submission_id = platform_submission_id
    if outcome != "pending" and not rec.submitted_at:
        rec.submitted_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    append_log([rec])
    return rec


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_export = sub.add_parser("export", help="Emit per-platform submission templates for a run.")
    p_export.add_argument("run_dir")
    p_export.add_argument("--candidate-id", required=True)
    p_export.add_argument("--platforms", nargs="+", default=["c4"])
    p_export.add_argument("--min-severity", default="Medium")
    p_export.add_argument("--only-reproduced", action="store_true")

    p_update = sub.add_parser("update", help="Update an outcome on a submitted record.")
    p_update.add_argument("submission_id")
    p_update.add_argument("--outcome", choices=["pending", "accepted", "duplicate", "rejected", "withdrawn"], required=True)
    p_update.add_argument("--payout-usd", type=int, default=None)
    p_update.add_argument("--platform-id", default=None)
    p_update.add_argument("--note", default="")

    p_ls = sub.add_parser("ls", help="List submissions log.")
    p_ls.add_argument("--outcome", default=None)

    args = parser.parse_args(argv)

    if args.cmd == "export":
        run_dir = Path(args.run_dir)
        if not run_dir.exists():
            cand = REPO_ROOT / "audits" / args.run_dir
            if cand.exists():
                run_dir = cand
            else:
                print(f"error: no run dir {args.run_dir}", file=sys.stderr)
                return 1
        records = export_run(
            run_dir,
            candidate_id=args.candidate_id,
            platforms=args.platforms,
            min_severity=args.min_severity,
            only_reproduced=args.only_reproduced,
        )
        print(f"Exported {len(records)} submission template(s):")
        for r in records:
            print(f"  [{r.finding_severity}] {r.platform}  ::  {r.template_path}")
        return 0

    if args.cmd == "update":
        rec = update_outcome(
            args.submission_id,
            outcome=args.outcome,
            payout_usd=args.payout_usd,
            notes=args.note,
            platform_submission_id=args.platform_id,
        )
        if not rec:
            print(f"error: no submission {args.submission_id}", file=sys.stderr)
            return 1
        print(f"Updated {rec.id}: outcome={rec.outcome} payout={rec.payout_usd}")
        return 0

    if args.cmd == "ls":
        for r in load_log():
            if args.outcome and r.outcome != args.outcome:
                continue
            print(f"  [{r.outcome:9s}] [{r.platform:8s}] [{r.finding_severity:4s}] {r.finding_title[:60]}")
            print(f"      {r.template_path}")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
