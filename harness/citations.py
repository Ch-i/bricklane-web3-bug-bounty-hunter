"""Citation validation — every finding must cite real corpus entries or claim novelty."""

from __future__ import annotations

from dataclasses import dataclass

from harness import corpus
from harness.schema import Finding


@dataclass
class CitationCheck:
    valid: list[Finding]
    rejected: list[tuple[Finding, str]]  # (finding, reason)


def validate_findings(findings: list[Finding]) -> CitationCheck:
    """Reject findings whose citations point to nonexistent corpus entries.

    Findings marked ``novel: true`` are accepted with no citation check, but
    the auditor must not also pass invented IDs in ``citations``.
    """
    valid: list[Finding] = []
    rejected: list[tuple[Finding, str]] = []

    # Single sqlite roundtrip to fetch all referenced IDs.
    all_ids: set[str] = set()
    for f in findings:
        for cid in f.citations:
            all_ids.add(cid)

    existing: set[str] = set()
    if all_ids:
        with corpus.connect() as conn:
            placeholders = ",".join("?" * len(all_ids))
            rows = conn.execute(
                f"SELECT id FROM corpus_entries WHERE id IN ({placeholders})",
                tuple(all_ids),
            ).fetchall()
            existing = {r["id"] for r in rows}

    for f in findings:
        missing = [c for c in f.citations if c not in existing]
        if missing:
            rejected.append(
                (
                    f,
                    f"citations point to nonexistent corpus entries: {missing}",
                )
            )
            continue
        if not f.citations and not f.novel:
            rejected.append((f, "no citations and not flagged novel"))
            continue
        valid.append(f)

    return CitationCheck(valid=valid, rejected=rejected)
