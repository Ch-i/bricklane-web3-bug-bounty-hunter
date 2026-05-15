"""Seed the corpus with curated SWC Registry entries.

Idempotent: re-running re-writes the same files. The SWC Registry is
archived/deprecated upstream, so the source is a frozen snapshot of value.

Usage:
    python -m scripts.seed_swc                 # default cache dir + curated list
    python -m scripts.seed_swc --all           # all SWC entries
    python -m scripts.seed_swc --cache /path   # override clone location
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from harness.corpus import REPO_ROOT, corpus_dir, reindex
from harness.schema import CorpusEntryFrontmatter

SWC_REPO = "https://github.com/SmartContractSecurity/SWC-registry.git"
DEFAULT_CACHE = Path("/tmp/swc-registry")

CURATED: dict[str, dict] = {
    "SWC-100": {"vuln_class": ["visibility", "access-control"], "tags": ["fundamentals"]},
    "SWC-101": {"vuln_class": ["arithmetic", "integer-overflow", "integer-underflow"], "tags": ["fundamentals", "pre-solc-0.8"]},
    "SWC-104": {"vuln_class": ["unchecked-call", "error-handling"], "tags": ["external-call"]},
    "SWC-105": {"vuln_class": ["access-control", "ether-withdrawal"], "tags": ["access-control"]},
    "SWC-106": {"vuln_class": ["access-control", "selfdestruct"], "tags": ["access-control", "destructive"]},
    "SWC-107": {"vuln_class": ["reentrancy", "external-call", "cei-violation"], "tags": ["fundamentals", "high-impact"]},
    "SWC-108": {"vuln_class": ["visibility"], "tags": ["fundamentals"]},
    "SWC-112": {"vuln_class": ["delegatecall", "code-injection", "upgradeable-proxy"], "tags": ["high-impact", "proxy-pattern"]},
    "SWC-114": {"vuln_class": ["front-running", "mev", "transaction-ordering"], "tags": ["mev", "economic"]},
    "SWC-115": {"vuln_class": ["tx-origin", "authentication", "access-control"], "tags": ["fundamentals"]},
    "SWC-116": {"vuln_class": ["timestamp-dependence", "time-manipulation"], "tags": ["miner-influence"]},
    "SWC-120": {"vuln_class": ["weak-randomness", "predictable-randomness"], "tags": ["randomness", "miner-influence"]},
    "SWC-124": {"vuln_class": ["storage-corruption", "arbitrary-write"], "tags": ["high-impact", "low-level"]},
    "SWC-128": {"vuln_class": ["dos", "gas-limit", "unbounded-loop"], "tags": ["denial-of-service"]},
    "SWC-133": {"vuln_class": ["hash-collision", "abi-encoding", "signature-replay"], "tags": ["cryptography", "abi-encoding"]},
}


def ensure_clone(cache: Path) -> Path:
    if not cache.exists():
        subprocess.run(
            ["git", "clone", "--depth", "1", SWC_REPO, str(cache)],
            check=True,
        )
    else:
        subprocess.run(
            ["git", "-C", str(cache), "pull", "--ff-only"],
            check=False,  # may fail in offline runs; existing snapshot is fine
            capture_output=True,
        )
    entries = cache / "entries" / "docs"
    if not entries.is_dir():
        raise FileNotFoundError(f"expected SWC entries at {entries}")
    return entries


@dataclass
class ParsedSWC:
    swc_id: str          # "SWC-107"
    title: str           # "Reentrancy"
    description: str
    remediation: str
    references: list[str]
    samples: list[tuple[str, str]]  # (name, code)
    cwe: str | None = None


def parse_swc_file(path: Path) -> ParsedSWC:
    """Best-effort parser for the SWC Registry markdown format."""
    text = path.read_text()
    swc_id = path.stem  # "SWC-107"

    # Strip deprecation notice (everything before "# Title").
    title_match = re.search(r"^# Title\s*\n+(.+?)\n", text, flags=re.MULTILINE)
    if not title_match:
        raise ValueError(f"{swc_id}: no Title section")
    title = title_match.group(1).strip()

    def section(name: str) -> str:
        m = re.search(
            rf"^##\s+{re.escape(name)}\s*\n+(.*?)(?=^##\s|\Z)",
            text,
            flags=re.MULTILINE | re.DOTALL,
        )
        return m.group(1).strip() if m else ""

    description = section("Description")
    remediation = section("Remediation")
    refs_block = section("References")
    samples_block = section("Samples")

    references = re.findall(r"\[[^\]]+\]\((https?://[^)]+)\)", refs_block)

    cwe = None
    rel_block = section("Relationships")
    cwe_match = re.search(r"\[(CWE-\d+):", rel_block)
    if cwe_match:
        cwe = cwe_match.group(1)

    # Each sample is "### name\n\n```solidity\n...\n```"
    samples = []
    for sm in re.finditer(
        r"^###\s+(.+?)\n+```(?:solidity|sol)?\n(.*?)```",
        samples_block,
        flags=re.MULTILINE | re.DOTALL,
    ):
        samples.append((sm.group(1).strip(), sm.group(2).rstrip()))

    return ParsedSWC(
        swc_id=swc_id,
        title=title,
        description=description,
        remediation=remediation,
        references=references,
        samples=samples,
        cwe=cwe,
    )


def render_corpus_entry(parsed: ParsedSWC, extra: dict, ingested_at: datetime) -> str:
    """Build the markdown content (frontmatter + body) for a corpus entry."""
    swc_num = parsed.swc_id.split("-", 1)[1]
    entry_id = f"swc-{swc_num}"

    fm = CorpusEntryFrontmatter(
        id=entry_id,
        source="swc",
        source_url=f"https://swcregistry.io/docs/{parsed.swc_id}/",
        title=f"{parsed.swc_id}: {parsed.title}",
        ingested_at=ingested_at,
        vuln_class=extra.get("vuln_class", []),
        tags=extra.get("tags", []),
        related_swc=[parsed.swc_id],
    )

    # Build body
    parts = [
        f"# {parsed.title}",
        "",
    ]
    if parsed.cwe:
        parts += [f"**Related CWE:** {parsed.cwe}", ""]
    parts += [
        "## Description",
        "",
        parsed.description,
        "",
        "## Remediation",
        "",
        parsed.remediation,
        "",
    ]
    if parsed.references:
        parts += ["## References", ""]
        parts += [f"- {ref}" for ref in parsed.references]
        parts += [""]
    if parsed.samples:
        parts += ["## Samples", ""]
        for name, code in parsed.samples:
            parts += [
                f"### {name}",
                "",
                "```solidity",
                code,
                "```",
                "",
            ]
    body = "\n".join(parts).rstrip() + "\n"

    # YAML frontmatter via the same dumper used in upsert_entry for consistency.
    import yaml

    data = fm.model_dump(mode="json", exclude_none=True)
    fm_yaml = yaml.safe_dump(data, sort_keys=True, allow_unicode=True)

    return f"---\n{fm_yaml}---\n\n{body}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", default=str(DEFAULT_CACHE), help="SWC repo clone path")
    parser.add_argument("--all", action="store_true", help="Seed every SWC entry, not just the curated list")
    parser.add_argument("--no-reindex", action="store_true", help="Skip sqlite reindex after writing files")
    args = parser.parse_args(argv)

    entries_dir = ensure_clone(Path(args.cache))
    out_dir = corpus_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc).replace(microsecond=0)

    if args.all:
        targets = sorted(entries_dir.glob("SWC-*.md"))
        extras = {p.stem: {} for p in targets}
    else:
        targets = []
        for swc_id in CURATED:
            p = entries_dir / f"{swc_id}.md"
            if not p.is_file():
                print(f"skip: {swc_id} not found at {p}", file=sys.stderr)
                continue
            targets.append(p)
        extras = CURATED

    written = 0
    for src_path in targets:
        try:
            parsed = parse_swc_file(src_path)
        except Exception as e:  # noqa: BLE001
            print(f"parse error {src_path.name}: {e}", file=sys.stderr)
            continue
        content = render_corpus_entry(parsed, extras.get(parsed.swc_id, {}), now)
        swc_num = parsed.swc_id.split("-", 1)[1]
        out_path = out_dir / f"swc-{swc_num}.md"
        out_path.write_text(content)
        written += 1
        print(f"wrote {out_path.relative_to(REPO_ROOT)} ({parsed.title})")

    print(f"\nwrote {written} corpus entries to {out_dir}")

    if not args.no_reindex:
        print("\nreindexing sqlite…")
        result = reindex()
        print(f"  inserted={result.inserted} updated={result.updated} skipped={result.skipped}")
        if result.errors:
            print("  errors:")
            for path, err in result.errors:
                print(f"    {path}: {err}")
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
