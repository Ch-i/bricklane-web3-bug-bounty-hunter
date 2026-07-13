# Contributing to Bricklane Web3 Bug Bounty Hunter

Welcome, and thank you for considering a contribution to Bricklane! 🛡️

This project sits at the intersection of smart-contract security and automated research — a space where every contribution makes the ecosystem safer. Whether you're fixing a typo in the corpus, writing a new crawler, or adding an entirely new logic pattern, your work is valued.

This guide will walk you through everything you need to get up and running.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development Setup](#development-setup)
3. [How to Add a New Crawler](#how-to-add-a-new-crawler)
4. [How to Add a Content Pattern](#how-to-add-a-content-pattern)
5. [How to Add Corpus Entries](#how-to-add-corpus-entries)
6. [UI Development](#ui-development)
7. [Code Style](#code-style)
8. [Pull Request Process](#pull-request-process)
9. [Reporting Bugs](#reporting-bugs)

---

## Getting Started

### 1. Fork and clone

```bash
# Fork on GitHub, then:
git clone https://github.com/<your-username>/bricklane-web3-bug-bounty-hunter.git
cd bricklane-web3-bug-bounty-hunter
```

### 2. Install dependencies

Bricklane uses [uv](https://docs.astral.sh/uv/) for fast, reproducible Python package management.

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync the base environment (Python ≥ 3.11)
uv sync
```

### 3. Run the test suite

```bash
uv run pytest
```

All 38 test files should pass. If anything fails on a fresh clone, please [open an issue](#reporting-bugs) — that's a bug on our end, not yours.

---

## Development Setup

Install the project with the `dev` extra to pull in testing and linting tools:

```bash
uv sync --extra dev
```

This gives you:

| Tool | Version | Purpose |
|------|---------|---------|
| **pytest** | ≥ 8.0 | Test runner |
| **pytest-asyncio** | ≥ 0.23 | Async test support |
| **ruff** | ≥ 0.4 | Linter and formatter |

### Running the linter

```bash
uv run ruff check .          # lint
uv run ruff format --check . # format check (no changes)
uv run ruff format .         # auto-format
```

### Running tests

```bash
uv run pytest                     # full suite
uv run pytest tests/test_corpus_reindex.py  # single file
uv run pytest -k "test_arxiv"     # by keyword
```

### Optional extras

Depending on what you're working on, you may want additional extras:

```bash
uv sync --extra dev --extra scrape   # Playwright for browser-based crawlers
uv sync --extra dev --extra embed    # sentence-transformers + torch for embeddings
uv sync --extra dev --extra static   # slither-analyzer for static analysis
uv sync --extra dev --extra ui       # FastAPI + uvicorn for the API server
uv sync --extra dev --extra mcp      # MCP server runtime
```

---

## How to Add a New Crawler

Crawlers live in `crawlers/` and are responsible for ingesting security-relevant data from a single external source into the corpus. Each crawler is a self-contained Python module.

### Step 1 — Create the module

Create a new file in `crawlers/`, e.g. `crawlers/my_source.py`:

```python
"""Ingest findings from MySource into the Bricklane corpus.

Usage:
    python -m crawlers.my_source
    python -m crawlers.my_source --limit 50
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from crawlers.common import slugify, write_corpus_entry
from harness.corpus import corpus_dir, reindex
from harness.schema import CorpusEntryFrontmatter


def fetch_entries(*, limit: int = 100) -> list[dict]:
    """Fetch raw entries from the upstream source.

    Implement pagination, rate-limiting, and retry logic here.
    Return a list of dicts with at least: id, title, url, body.
    """
    # TODO: implement source-specific fetching
    raise NotImplementedError


def ingest_entry(raw: dict, *, out_root: Path, ingested_at: datetime) -> bool:
    """Transform a raw entry into a corpus markdown file.

    Returns True if a new file was written, False if skipped (duplicate).
    """
    entry_id = f"mysource-{slugify(raw['id'])}"
    fm = CorpusEntryFrontmatter(
        id=entry_id,
        source="mysource",                     # register in harness/schema.py SourceKind
        source_url=raw["url"],
        title=raw["title"][:240],
        ingested_at=ingested_at,
        tags=["mysource"],
    )

    body = f"# {fm.title}\n\n{raw['body']}\n"

    out_path = out_root / "mysource" / f"{slugify(raw['id'])}.md"
    if out_path.exists():
        return False
    write_corpus_entry(out_path, fm, body)
    return True


def crawl(*, limit: int = 100, reindex_after: bool = True) -> dict:
    """Main crawl loop."""
    out_root = corpus_dir()
    ingested_at = datetime.now(timezone.utc).replace(microsecond=0)

    raw_entries = fetch_entries(limit=limit)
    stats = {"fetched": len(raw_entries), "written": 0, "duplicates": 0}

    for raw in raw_entries:
        if ingest_entry(raw, out_root=out_root, ingested_at=ingested_at):
            stats["written"] += 1
        else:
            stats["duplicates"] += 1

    if reindex_after and stats["written"]:
        reindex()

    return stats


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--no-reindex", action="store_true")
    args = parser.parse_args(argv)

    stats = crawl(limit=args.limit, reindex_after=not args.no_reindex)
    print(f"fetched={stats['fetched']}  written={stats['written']}  "
          f"duplicates={stats['duplicates']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

### Step 2 — Register the source kind

Add your source name to the `SourceKind` literal in `harness/schema.py`:

```python
SourceKind = Literal[
    "swc",
    "solodit",
    "arxiv",
    "audit-report",
    "rekt",
    "dasp",
    "synthesis",
    "mysource",        # ← add your source here
]
```

### Step 3 — Write tests

Create `tests/test_my_source_crawler.py` and test at minimum:

- **Parsing**: does `ingest_entry()` produce valid frontmatter?
- **Deduplication**: does a second call skip already-written entries?
- **Edge cases**: empty responses, malformed data, rate-limit handling.

```bash
uv run pytest tests/test_my_source_crawler.py -v
```

### Step 4 — Respect rate limits

All crawlers must be polite to upstream APIs. Use `time.sleep()` between paginated requests and respect `Retry-After` headers. Document the rate-limit policy in your module docstring.

---

## How to Add a Content Pattern

Content patterns live in `content/` and represent a specific smart-contract security or DeFi logic pattern. The project currently contains 28 patterns (e.g. `checks-effects-interactions`, `flash-loan-mechanics`, `oracle-aggregation-staleness`).

### Directory structure

Create a new directory under `content/` with a kebab-case name:

```
content/your-pattern-name/
├── diagrams.json        # Visual diagrams describing the pattern
├── simulation.json      # Interactive simulation data
└── video_script.py      # Manim video script for animated explanations
```

### Required files

#### `diagrams.json`

A JSON file containing diagram definitions for the pattern. This drives visual representations in the UI and content pipeline.

#### `simulation.json`

Structured simulation data that models the pattern's behavior — state transitions, invariant violations, or attack sequences. This file powers interactive visualizations.

#### `video_script.py`

A Python script (typically using Manim or similar) that generates animated video explanations of the pattern.

### Naming convention

Use descriptive kebab-case names that capture the core concept:

```
✅  integer-overflow-precision-loss
✅  cross-chain-message-passing
✅  erc4626-tokenized-vault-standard
❌  overflow
❌  my_new_pattern
```

---

## How to Add Corpus Entries

The corpus is the knowledge base that grounds every audit finding. It contains 8,400+ markdown files with structured YAML frontmatter, organized by source in subdirectories under `corpus/`.

### Frontmatter schema

Every corpus entry must begin with YAML frontmatter matching the `CorpusEntryFrontmatter` Pydantic model in `harness/schema.py`:

```yaml
---
id: mysource-unique-slug          # required — pattern: ^[a-z][a-z0-9-]*-[A-Za-z0-9._-]+$
source: arxiv                     # required — one of: swc, solodit, arxiv, audit-report, rekt, dasp, synthesis
source_url: https://example.com   # optional — canonical link to the original
title: "Short descriptive title"  # required — max ~240 chars
ingested_at: "2026-01-15T12:00:00Z" # required — ISO 8601 UTC timestamp
published_at: "2025-12-01T00:00:00Z" # optional — original publication date

vuln_class: []                    # optional — e.g. ["reentrancy", "oracle-manipulation"]
severity: High                    # optional — Critical | High | Medium | Low | Informational | Gas
protocol_category: []             # optional — e.g. ["lending", "dex"]
tags: ["arxiv", "category:cs.CR"] # optional — freeform tags
related_swc: ["SWC-107"]          # optional — related SWC registry IDs
derives_from: []                  # optional — IDs of parent corpus entries
cve: null                         # optional — CVE identifier
affected_contracts: []            # optional — e.g. [{"address": "0x...", "chain": "mainnet"}]
---

# Your Entry Title

Markdown body goes here...
```

### Key rules

- **`id` must be globally unique.** The pattern is `<source>-<slug>`, e.g. `arxiv-2401.12345`, `solodit-42`, `rekt-euler-finance`.
- **`id` must match the regex** `^[a-z][a-z0-9-]*-[A-Za-z0-9._-]+$` — lowercase start, alphanumeric with hyphens, at least one hyphen.
- **`ingested_at` is always UTC.** Use `datetime.now(timezone.utc)`.
- **After adding entries, reindex the SQLite database:**

```bash
uv run python -c "from harness.corpus import reindex; reindex()"
```

### File placement

Place your markdown file in the appropriate subdirectory of `corpus/`:

```
corpus/
├── arxiv/          # arXiv papers
├── solodit/        # Solodit findings
├── rekt/           # Rekt.news post-mortems
├── sherlock/       # Sherlock audit findings
├── c4/             # Code4rena contest findings
├── cantina/        # Cantina audit findings
└── immunefi/       # Immunefi bug bounty programs
```

If your source doesn't have a subdirectory yet, create one.

---

## UI Development

The frontend is a React + Vite application in the `ui/` directory.

### Setup

```bash
cd ui
npm install
npm run dev
```

The dev server will start at `http://localhost:5173` by default.

### Running the API backend

The UI talks to a FastAPI backend. Start it in a separate terminal:

```bash
uv sync --extra ui
uv run uvicorn api:app --reload --port 8000
```

### UI conventions

- Components go in `ui/src/components/`
- Use existing patterns for API calls
- All new UI features should work without authentication (the project is local-first)

---

## Code Style

Bricklane uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting. The configuration lives in `pyproject.toml`:

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "SIM"]
ignore = ["E501"]
```

### What this means in practice

| Rule set | What it catches |
|----------|-----------------|
| **E** | pycodestyle errors |
| **F** | pyflakes (unused imports, undefined names) |
| **I** | isort-style import ordering |
| **B** | flake8-bugbear (common pitfalls) |
| **UP** | pyupgrade (modernize syntax for Python 3.11+) |
| **SIM** | flake8-simplify (unnecessary complexity) |

### Line length

Target is **100 characters**. The `E501` (line-too-long) rule is ignored to avoid noisy warnings on long strings, but please keep code readable and break lines naturally.

### Before committing

```bash
uv run ruff check .          # catch lint issues
uv run ruff format .         # auto-format
uv run pytest                # make sure nothing is broken
```

---

## Pull Request Process

### 1. Branch from `main`

```bash
git checkout -b feat/my-feature main
```

Use a descriptive branch name: `feat/`, `fix/`, `crawler/`, `corpus/`, `docs/`.

### 2. Make focused commits

Each commit should do one thing. Write clear commit messages:

```
feat(crawler): add immunefi bug bounty crawler

Ingests active Immunefi programs with reward tiers and scope data.
Respects their API rate limit of 1 req/sec. Deduplicates by program slug.
```

### 3. Run the full check

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

All three must pass before opening a PR.

### 4. Open the pull request

- Fill in the PR template (if present)
- Describe **what** changed and **why**
- Link to any related issues
- If you added a crawler, include sample output (a few corpus entries)
- If you modified the schema, explain the migration impact

### 5. Review

A maintainer will review your PR. We may ask for changes — that's normal and collaborative, not adversarial. Security projects benefit from careful review.

### What we look for

- ✅ Tests pass
- ✅ Ruff is clean
- ✅ New code has tests
- ✅ Crawlers respect upstream rate limits
- ✅ Corpus entries have valid frontmatter
- ✅ Commit history is clean and readable

---

## Reporting Bugs

Found a bug? That's a contribution too — and an important one.

### Where to report

Open an issue on GitHub with the **Bug Report** label.

### What to include

1. **What you were doing** — the command you ran or the UI action you took
2. **What you expected** — the correct behavior
3. **What actually happened** — error messages, stack traces, wrong output
4. **Environment** — Python version, OS, `uv --version`
5. **Reproducibility** — can you reproduce it consistently?

### Security vulnerabilities

> [!IMPORTANT]
> If you've found a **security vulnerability** in Bricklane itself (not in a contract being audited), please **do not** open a public issue. Instead, reach out privately to the maintainers. We'll coordinate a fix and disclosure timeline.

---

## Project Structure at a Glance

```
bricklane-web3-bug-bounty-hunter/
├── harness/             # Core Python modules
│   ├── audit_runner.py  #   Orchestrates audit passes
│   ├── corpus.py        #   Corpus indexing & search
│   ├── citations.py     #   Citation enforcement
│   ├── scanner.py       #   Contract scanning
│   ├── compositions.py  #   Cross-finding composition
│   ├── deep_dive.py     #   Deep vulnerability analysis
│   ├── poc.py           #   Proof-of-concept generation
│   ├── schema.py        #   Pydantic models (frontmatter, findings)
│   └── ...              #   ~30 modules total
├── crawlers/            # Source-specific ingestion
│   ├── common.py        #   Shared utilities (slugify, write_corpus_entry)
│   ├── arxiv.py         #   arXiv paper crawler
│   ├── solodit.py       #   Solodit findings
│   ├── rekt.py          #   Rekt.news post-mortems
│   ├── sherlock_audits.py
│   ├── c4_contests.py
│   ├── cantina_audits.py
│   └── immunefi_programs.py
├── content/             # 28 logic pattern directories
│   ├── checks-effects-interactions/
│   ├── flash-loan-mechanics/
│   ├── oracle-aggregation-staleness/
│   └── ...
├── corpus/              # 8,400+ markdown entries with YAML frontmatter
├── ui/                  # React + Vite frontend
├── api.py               # FastAPI backend
├── tests/               # 38 test files (pytest)
└── pyproject.toml       # Project metadata, extras, tool config
```

---

## Thank You

Smart-contract security is a team sport. Every crawler that catches a new post-mortem, every corpus entry that documents a novel attack pattern, and every test that prevents a regression makes DeFi safer for everyone.

We're glad you're here. Happy hacking! 🔐
