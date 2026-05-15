"""Ingest the Solodit corpus from solodit/solodit_content on GitHub.

No scraping required — Solodit publishes their audit-report markdown on
GitHub. We git-clone (or pull) the repo, parse each report into per-finding
markdown files with our frontmatter format, and write to corpus/solodit/.

Usage:
    python -m crawlers.solodit                     # full ingest
    python -m crawlers.solodit --firm Cyfrin       # one firm
    python -m crawlers.solodit --no-reindex        # skip sqlite reindex
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from crawlers.common import git_clone_or_pull, slugify, write_corpus_entry
from harness.corpus import REPO_ROOT, corpus_dir, reindex
from harness.schema import CorpusEntryFrontmatter

REPO_URL = "https://github.com/solodit/solodit_content.git"
DEFAULT_CACHE = Path("/tmp/solodit_content")

# Maps the Solodit section-header conventions to our Severity literal.
# Section names that don't match are skipped (e.g. "Vulnerability Details",
# typo headers — these are usually empty stubs or non-finding sections).
SEVERITY_MAP = {
    "critical risk": "Critical",
    "critical": "Critical",
    "high risk": "High",
    "high": "High",
    "medium risk": "Medium",
    "medium": "Medium",
    "low risk": "Low",
    "low": "Low",
    "informational": "Informational",
    "info": "Informational",
    "gas optimizations": "Gas",
    "gas optimization": "Gas",
    "gas": "Gas",
}

# Section headers we never want to treat as a severity bucket.
NON_FINDING_HEADERS = {
    "findings",
    "summary",
    "executive summary",
    "scope",
    "introduction",
    "appendix",
    "audit information",
    "recommendation",
    "vulnerability details",
}

ISO_DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-")


@dataclass
class ParsedFinding:
    severity: str
    title: str
    body: str
    section_idx: int
    finding_idx: int


def _normalize_header(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def parse_report(md_path: Path) -> Iterator[ParsedFinding]:
    """Split a Solodit report markdown into individual findings.

    Looks for top-level ``## <severity>`` sections, then ``### <title>``
    findings inside each. Sections whose header doesn't map to a known
    severity are skipped.
    """
    text = md_path.read_text(errors="replace")
    section_iter = re.finditer(
        r"^##\s+([^\n]+)\n(.*?)(?=^##\s|\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    for section_idx, section in enumerate(section_iter):
        header = _normalize_header(section.group(1))
        severity = SEVERITY_MAP.get(header)
        if not severity:
            if header in NON_FINDING_HEADERS:
                continue
            # Sometimes the actual finding is at ## level (e.g. one-shot
            # reports). Treat the whole section as a single Medium-severity
            # finding only if its body looks substantive (>200 chars) and
            # the header isn't a non-finding keyword.
            body = section.group(2).strip()
            if len(body) > 200 and not any(k in header for k in NON_FINDING_HEADERS):
                yield ParsedFinding(
                    severity="Medium",
                    title=section.group(1).strip(),
                    body=body,
                    section_idx=section_idx,
                    finding_idx=0,
                )
            continue

        body = section.group(2)
        finding_iter = re.finditer(
            r"^###\s+([^\n]+)\n(.*?)(?=^###\s|\Z)",
            body,
            flags=re.MULTILINE | re.DOTALL,
        )
        for finding_idx, finding in enumerate(finding_iter):
            title = finding.group(1).strip()
            fbody = finding.group(2).strip()
            if not fbody or len(fbody) < 40:
                continue  # empty or stub finding
            yield ParsedFinding(
                severity=severity,
                title=title,
                body=fbody,
                section_idx=section_idx,
                finding_idx=finding_idx,
            )


def _date_from_filename(name: str) -> datetime | None:
    m = ISO_DATE_RE.match(name)
    if not m:
        return None
    try:
        return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), tzinfo=timezone.utc)
    except ValueError:
        return None


def _entry_id(firm_slug: str, report_stem_slug: str, section_idx: int, finding_idx: int) -> str:
    # `^[a-z][a-z0-9-]*-[A-Za-z0-9._-]+$` per CorpusEntryFrontmatter.id
    return f"solodit-{firm_slug}-{report_stem_slug}-{section_idx}-{finding_idx}"


def _source_url(firm: str, report_filename: str) -> str:
    # GitHub renders the canonical view of the source file.
    from urllib.parse import quote
    return (
        "https://github.com/solodit/solodit_content/blob/main/reports/"
        f"{quote(firm)}/{quote(report_filename)}"
    )


def ingest_report(
    md_path: Path,
    firm: str,
    *,
    out_root: Path,
    ingested_at: datetime,
) -> int:
    """Convert one Solodit report to N per-finding corpus entries."""
    firm_slug = slugify(firm)
    report_stem_slug = slugify(md_path.stem)
    published = _date_from_filename(md_path.name)

    written = 0
    for pf in parse_report(md_path):
        entry_id = _entry_id(firm_slug, report_stem_slug, pf.section_idx, pf.finding_idx)
        fm = CorpusEntryFrontmatter(
            id=entry_id,
            source="solodit",
            source_url=_source_url(firm, md_path.name),
            title=pf.title[:240],
            ingested_at=ingested_at,
            published_at=published,
            severity=pf.severity,
            tags=[f"firm:{firm_slug}", f"report:{report_stem_slug}"],
        )

        # Body: our own metadata header (clearly labeled "section severity"
        # so it doesn't collide with the report's per-finding "Severity"
        # line), then the original finding text verbatim.
        body = (
            f"# {pf.title}\n\n"
            f"_Section severity (from Solodit section header): {pf.severity}_  \n"
            f"_Audit firm: {firm}_  \n"
            f"_Source report: [{md_path.name}]({_source_url(firm, md_path.name)})_\n\n"
            f"---\n\n"
            f"{pf.body.strip()}\n"
        )

        out_path = out_root / "solodit" / firm_slug / f"{report_stem_slug}-{pf.section_idx}-{pf.finding_idx}.md"
        write_corpus_entry(out_path, fm, body)
        written += 1

    return written


def crawl(
    cache: Path = DEFAULT_CACHE,
    firm: str | None = None,
    reindex_after: bool = True,
    out_root: Path | None = None,
) -> dict:
    """Top-level crawl: clone/pull, parse, write corpus entries, optionally reindex."""
    cache = git_clone_or_pull(REPO_URL, cache)
    reports_root = cache / "reports"
    if not reports_root.is_dir():
        raise FileNotFoundError(f"expected {reports_root} after clone")

    target_root = out_root or corpus_dir()
    ingested_at = datetime.now(timezone.utc).replace(microsecond=0)

    stats: dict = {"firms": {}, "total_findings": 0, "total_reports": 0}
    for firm_dir in sorted(reports_root.iterdir()):
        if not firm_dir.is_dir():
            continue
        if firm and firm_dir.name != firm:
            continue
        firm_stats = {"reports": 0, "findings": 0, "errors": 0}
        for md_path in sorted(firm_dir.rglob("*.md")):
            if md_path.name.upper() == "README.MD":
                continue
            try:
                n = ingest_report(md_path, firm_dir.name, out_root=target_root, ingested_at=ingested_at)
            except Exception as e:  # noqa: BLE001
                firm_stats["errors"] += 1
                print(f"error: {md_path}: {e}", file=sys.stderr)
                continue
            firm_stats["reports"] += 1
            firm_stats["findings"] += n
        stats["firms"][firm_dir.name] = firm_stats
        stats["total_reports"] += firm_stats["reports"]
        stats["total_findings"] += firm_stats["findings"]

    if reindex_after:
        print(f"\nreindexing sqlite (this can take a moment with {stats['total_findings']} entries)…")
        result = reindex()
        stats["reindex"] = {
            "inserted": result.inserted,
            "updated": result.updated,
            "errors": len(result.errors),
        }
        if result.errors:
            print("  first 10 errors:")
            for path, err in result.errors[:10]:
                print(f"    {path}: {err}")

    return stats


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", default=str(DEFAULT_CACHE))
    parser.add_argument("--firm", help="Ingest only this firm (exact dir name).")
    parser.add_argument("--no-reindex", action="store_true")
    args = parser.parse_args(argv)

    stats = crawl(
        cache=Path(args.cache),
        firm=args.firm,
        reindex_after=not args.no_reindex,
    )

    print(f"\n=== solodit crawl summary ===")
    print(f"reports: {stats['total_reports']}  findings: {stats['total_findings']}")
    for firm_name, fs in stats["firms"].items():
        if fs["reports"]:
            print(f"  {firm_name:30s} {fs['reports']:>4} reports  {fs['findings']:>5} findings")
    if "reindex" in stats:
        r = stats["reindex"]
        print(f"reindex: inserted={r['inserted']} updated={r['updated']} errors={r['errors']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
