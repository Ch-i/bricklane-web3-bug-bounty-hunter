"""Contract scanner — scans Solidity source against all pattern signatures.

Given raw Solidity code, returns a ranked list of matched patterns with
severity, confidence scores, matched code lines, and audit checklists.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from harness.signatures import SIGNATURES, PatternSignature


@dataclass
class MatchedLine:
    line_number: int
    content: str
    detector: str  # which regex matched


@dataclass
class ScanMatch:
    slug: str
    title: str
    severity: str
    confidence: float          # 0.0 – 1.0
    matched_lines: list[MatchedLine]
    checklist: list[str]
    detector_hits: int         # how many distinct detectors fired
    total_hits: int            # total line matches


# Severity ordering for sorting
_SEV_ORDER = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}


def scan_source(source_code: str) -> list[ScanMatch]:
    """Scan Solidity source code against all pattern signatures.

    Returns matches sorted by severity (Critical first), then by confidence.
    """
    lines = source_code.splitlines()
    matches: list[ScanMatch] = []

    for sig in SIGNATURES:
        matched_lines: list[MatchedLine] = []
        detectors_hit: set[str] = set()

        for detector_pattern in sig.detectors:
            try:
                regex = re.compile(detector_pattern, re.IGNORECASE)
            except re.error:
                continue

            for i, line in enumerate(lines, 1):
                # Skip comments
                stripped = line.strip()
                if stripped.startswith("//") or stripped.startswith("*") or stripped.startswith("/*"):
                    continue

                if regex.search(line):
                    # Avoid duplicate line entries for same detector
                    already = any(m.line_number == i and m.detector == detector_pattern for m in matched_lines)
                    if not already:
                        matched_lines.append(MatchedLine(
                            line_number=i,
                            content=line.rstrip(),
                            detector=detector_pattern,
                        ))
                        detectors_hit.add(detector_pattern)

        if not matched_lines:
            continue

        # Calculate confidence score
        detector_ratio = len(detectors_hit) / len(sig.detectors)

        # Boost if confidence_boost_keywords appear in source
        boost = 0.0
        source_lower = source_code.lower()
        for kw in sig.confidence_boost_keywords:
            if kw.lower() in source_lower:
                boost += 0.05

        # Confidence: base from detector ratio + keyword boost, capped at 1.0
        confidence = min(1.0, round(detector_ratio * 0.7 + boost + 0.1, 2))

        # Deduplicate matched lines by line number (keep first)
        seen_lines: set[int] = set()
        deduped: list[MatchedLine] = []
        for ml in sorted(matched_lines, key=lambda m: m.line_number):
            if ml.line_number not in seen_lines:
                deduped.append(ml)
                seen_lines.add(ml.line_number)

        matches.append(ScanMatch(
            slug=sig.slug,
            title=sig.title,
            severity=sig.severity,
            confidence=confidence,
            matched_lines=deduped[:20],  # cap at 20 lines per pattern
            checklist=sig.checklist,
            detector_hits=len(detectors_hit),
            total_hits=len(deduped),
        ))

    # Sort: severity first, then confidence descending
    matches.sort(key=lambda m: (_SEV_ORDER.get(m.severity, 99), -m.confidence))

    return matches


def scan_file(file_path: str | Path) -> list[ScanMatch]:
    """Scan a Solidity file."""
    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {p}")
    return scan_source(p.read_text())


def format_report(matches: list[ScanMatch], source_name: str = "contract") -> str:
    """Format scan results as a readable markdown report."""
    if not matches:
        return f"# Scan Report: {source_name}\n\nNo patterns detected. ✓\n"

    lines = [f"# Scan Report: {source_name}\n"]
    lines.append(f"**{len(matches)} patterns detected**\n")

    crit = sum(1 for m in matches if m.severity == "Critical")
    high = sum(1 for m in matches if m.severity == "High")
    if crit:
        lines.append(f"🔴 **{crit} Critical** patterns found\n")
    if high:
        lines.append(f"🟠 **{high} High** severity patterns found\n")
    lines.append("---\n")

    for m in matches:
        sev_icon = "🔴" if m.severity == "Critical" else "🟠" if m.severity == "High" else "🟡"
        lines.append(f"## {sev_icon} {m.title} ({m.severity})")
        lines.append(f"*Confidence: {int(m.confidence * 100)}% · {m.detector_hits} detectors · {m.total_hits} matches*\n")

        lines.append("### Matched Lines")
        for ml in m.matched_lines[:10]:
            lines.append(f"- **L{ml.line_number}**: `{ml.content.strip()}`")
        lines.append("")

        lines.append("### Audit Checklist")
        for item in m.checklist:
            lines.append(f"- [ ] {item}")
        lines.append("")

    return "\n".join(lines)
