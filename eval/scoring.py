"""Keyword-based scorer for eval entries.

Pure-Python: walks the findings JSON produced by ``harness.audit_runner
finalize`` and matches against ``ExpectedFinding`` constraints. No LLM
calls — the recall metric is deterministic and replayable.

Future: optional ``llm-judge`` grading mode that calls ``claude -p`` to
resolve ambiguous cases. Defer until keyword scoring is shown insufficient.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import frontmatter

from eval.schema import EvalResult, ExpectedFinding
from harness.schema import Finding

SEVERITY_RANK = {
    "Critical": 5,
    "High": 4,
    "Medium": 3,
    "Low": 2,
    "Informational": 1,
    "Gas": 0,
}


def load_expected(path: Path) -> ExpectedFinding:
    post = frontmatter.load(path)
    return ExpectedFinding.model_validate(post.metadata)


def load_findings(run_dir: Path) -> list[Finding]:
    payload = json.loads((run_dir / "findings.json").read_text())
    return [Finding.model_validate(item) for item in payload]


def _finding_haystack(f: Finding) -> str:
    parts = [f.title, f.description, f.impact, f.recommendation]
    if f.proof_of_concept:
        parts.append(f.proof_of_concept)
    return "\n".join(parts).lower()


def _location_hit(f: Finding, expected_locations: list[dict]) -> bool:
    if not expected_locations:
        return True
    for loc in f.location:
        for exp in expected_locations:
            file_hint = exp.get("file", "").lower()
            fn_hint = exp.get("function", "").lower()
            if file_hint and file_hint not in loc.file.lower():
                continue
            # function hint is matched against description/title (no AST awareness)
            haystack = _finding_haystack(f)
            if fn_hint and fn_hint.lower() not in haystack:
                continue
            return True
    return False


def score_entry(
    expected: ExpectedFinding,
    findings: list[Finding],
    run_dir: Path,
    corpus_snapshot: str,
) -> EvalResult:
    """Return one EvalResult row for the given audit run."""

    all_titles = [f.title for f in findings]

    # Memorization warning (informational; does not affect pass/fail).
    joined = "\n".join(_finding_haystack(f) for f in findings)
    memorization_hits = [
        k for k in expected.memorization_signals if k.lower() in joined
    ]

    min_rank = SEVERITY_RANK[expected.expected_severity]
    matched = []

    for f in findings:
        if SEVERITY_RANK[f.severity] < min_rank:
            continue

        haystack = _finding_haystack(f)
        matched_kw = [k for k in expected.required_keywords if k.lower() in haystack]

        # All required keywords must be present (AND, not OR) — that's what
        # "understands the bug" looks like.
        if expected.required_keywords and len(matched_kw) < len(expected.required_keywords):
            continue

        if not _location_hit(f, expected.expected_locations):
            continue

        matched.append(
            {
                "finding_title": f.title,
                "severity": f.severity,
                "matched_keywords": matched_kw,
                "location_hit": True,
                "citations": f.citations,
                "novel": f.novel,
            }
        )

    passed = len(matched) >= 1
    warning_suffix = (
        f" [memorization warning: {memorization_hits}]"
        if memorization_hits
        else ""
    )
    if passed:
        reasoning = (
            f"PASS — {len(matched)} finding(s) match the expected bug "
            f"(severity≥{expected.expected_severity}, all required keywords "
            f"present, location consistent).{warning_suffix}"
        )
    else:
        present = sorted(
            {k for k in expected.required_keywords for f in findings if k.lower() in _finding_haystack(f)}
        )
        missing = sorted(set(expected.required_keywords) - set(present))
        reasoning = (
            f"FAIL — no finding satisfies all criteria. "
            f"keywords present: {present or '[]'}, "
            f"keywords missing: {missing or '[]'}, "
            f"total findings: {len(findings)}.{warning_suffix}"
        )

    return EvalResult(
        entry_id=expected.id,
        timestamp=datetime.now(timezone.utc).isoformat(),
        run_dir=str(run_dir),
        corpus_snapshot=corpus_snapshot,
        passed=passed,
        reasoning=reasoning,
        matched_findings=matched,
        all_finding_titles=all_titles,
        total_findings=len(findings),
        memorization_signals_hit=memorization_hits,
    )
