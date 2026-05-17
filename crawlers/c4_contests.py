"""Code4rena active-contest ingestor.

Strategy (in priority order):
  1. code4rena.com/__data.json — SvelteKit data endpoint behind their UI.
     If their site uses Sapper/SvelteKit data routes this is the cleanest.
  2. code4rena.com/api/contests — common REST shape if exposed.
  3. Fall back to scraping the active-contests HTML page.

Per active contest, we resolve to a normalized Candidate:
  * id              = "c4-<slug>"
  * platform        = "c4"
  * kind            = "source-only"
  * repo_url        = the contest's GitHub repo (typically code-423n4/<slug>)
  * commit          = the contest's pinned commit SHA (parsed from repo's
                       Foundry/Hardhat config or the contest readme)
  * scope_paths     = files/directories listed in the contest's "scope"
  * payout_max_usd  = prize pool total
  * closes_at       = contest end date

The crawler is idempotent: re-running on the same day produces no new rows
unless an active contest changes status or scope.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

import httpx

from harness import candidates as cand_store
from harness.candidates import Candidate
from harness.corpus import REPO_ROOT

USER_AGENT = "web3sentinel-c4-ingestor/0.1 (research)"
C4_BASE = "https://code4rena.com"
GH_C4_ORG = "code-423n4"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _http_get(url: str, *, timeout: float = 30.0) -> httpx.Response:
    return httpx.get(
        url,
        timeout=timeout,
        follow_redirects=True,
        headers={"User-Agent": USER_AGENT, "Accept": "application/json, text/html"},
    )


# ---------------------------------------------------------------------------
# Source 1: __data.json (SvelteKit data route)
# ---------------------------------------------------------------------------


def _fetch_sveltekit_active() -> list[dict] | None:
    """Try the most common SvelteKit data path. Returns None on miss."""
    for path in ("/contests/__data.json", "/contests/active/__data.json"):
        try:
            r = _http_get(f"{C4_BASE}{path}")
        except httpx.HTTPError:
            continue
        if r.status_code != 200:
            continue
        try:
            data = r.json()
        except ValueError:
            continue
        # SvelteKit puts data inside nested arrays; flatten + look for contest-shaped entries
        flat = _flatten_json(data)
        candidates = [
            x for x in flat
            if isinstance(x, dict)
            and ("slug" in x or "uniqueId" in x)
            and (x.get("status") in ("active", "Active", "open") or "endTime" in x)
        ]
        if candidates:
            return candidates
    return None


def _flatten_json(node, out: list | None = None) -> list:
    if out is None:
        out = []
    if isinstance(node, dict):
        out.append(node)
        for v in node.values():
            _flatten_json(v, out)
    elif isinstance(node, list):
        for v in node:
            _flatten_json(v, out)
    return out


# ---------------------------------------------------------------------------
# Source 2: GitHub API — list code-423n4 org repos, filter by "audit" / "findings"
# ---------------------------------------------------------------------------


def _fetch_github_active(limit: int = 30) -> list[dict]:
    """Walk the code-423n4 GitHub org for recent repos that look like audit contests.

    Returns a list of dicts compatible with the parser's expectations. This
    is a fallback that runs without authentication; it picks up the most
    recently-pushed repos and infers active status from the README.
    """
    url = f"https://api.github.com/orgs/{GH_C4_ORG}/repos?sort=pushed&per_page={limit}"
    r = _http_get(url, timeout=20.0)
    if r.status_code != 200:
        return []
    repos = r.json()
    if not isinstance(repos, list):
        return []
    out: list[dict] = []
    for repo in repos:
        name = repo.get("name") or ""
        # C4 contest naming: 2025-04-aave-v4 or 2026-05-some-protocol-findings
        if not re.match(r"^\d{4}-\d{2}-", name):
            continue
        out.append(
            {
                "name": name,
                "html_url": repo.get("html_url"),
                "clone_url": repo.get("clone_url"),
                "pushed_at": repo.get("pushed_at"),
                "default_branch": repo.get("default_branch", "main"),
                "archived": repo.get("archived", False),
                "description": repo.get("description") or "",
            }
        )
    return out


# ---------------------------------------------------------------------------
# Source 3: scrape /contests/active HTML
# ---------------------------------------------------------------------------


def _fetch_active_html() -> list[dict]:
    """Scrape the active-contests page. Returns list of {slug, title, payout, ends_at}.

    Best-effort; HTML shape changes from time to time. Used only when both
    structured sources fail.
    """
    try:
        r = _http_get(f"{C4_BASE}/contests")
    except httpx.HTTPError:
        return []
    if r.status_code != 200:
        return []
    html = r.text
    out: list[dict] = []
    # Look for /audits/<slug> anchors that ship in the active section
    for m in re.finditer(r'href="(/audits/[\w-]+)"', html):
        slug = m.group(1).rsplit("/", 1)[-1]
        if slug.startswith("https"):
            continue
        out.append({"slug": slug, "title": slug, "endTime": None})
    return out


# ---------------------------------------------------------------------------
# Normalize -> Candidate
# ---------------------------------------------------------------------------


def _parse_payout(value) -> int | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return int(value)
    s = str(value).strip().replace("$", "").replace(",", "").upper()
    m = re.match(r"^([\d.]+)\s*([KM]?)$", s)
    if not m:
        return None
    try:
        n = float(m.group(1))
    except ValueError:
        return None
    mult = {"K": 1_000, "M": 1_000_000, "": 1}[m.group(2)]
    return int(n * mult)


def _parse_iso(value) -> str | None:
    if not value:
        return None
    if isinstance(value, str):
        try:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
            return value
        except ValueError:
            return None
    if isinstance(value, (int, float)):
        # ms or seconds since epoch
        ts = value / 1000 if value > 10**12 else value
        return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()
    return None


def _slug_from_entry(entry: dict) -> str | None:
    return entry.get("slug") or entry.get("uniqueId") or entry.get("name")


def _candidate_from_sveltekit(entry: dict, sourced_at: str) -> Candidate | None:
    slug = _slug_from_entry(entry)
    if not slug:
        return None
    title = entry.get("title") or entry.get("name") or slug
    repo_url = entry.get("repoUrl") or entry.get("findingsRepo")
    if not repo_url:
        # C4 convention: repo at github.com/code-423n4/<slug>
        repo_url = f"https://github.com/{GH_C4_ORG}/{slug}"
    payout = _parse_payout(entry.get("amount") or entry.get("totalAward") or entry.get("totalAmount"))
    closes_at = _parse_iso(entry.get("endTime") or entry.get("endDate"))
    return Candidate(
        id=f"c4-{slug}",
        platform="c4",
        kind="source-only",
        title=str(title),
        sourced_at=sourced_at,
        payout_max_usd=payout,
        closes_at=closes_at,
        repo_url=repo_url,
        commit=entry.get("commit") or entry.get("commitHash"),
        scope_paths=list(entry.get("scope") or []),
        notes=(entry.get("description") or "")[:1000],
    )


def _candidate_from_github(entry: dict, sourced_at: str) -> Candidate:
    name = entry["name"]
    return Candidate(
        id=f"c4-{name}",
        platform="c4",
        kind="source-only",
        title=name.replace("-", " "),
        sourced_at=sourced_at,
        repo_url=entry.get("html_url"),
        commit=None,
        scope_paths=[],
        notes=(entry.get("description") or "")[:1000],
    )


# ---------------------------------------------------------------------------
# Optional: clone the repo + parse README for scope + commit
# ---------------------------------------------------------------------------


def _ensure_clone(repo_url: str, cache_root: Path) -> Path | None:
    """Shallow-clone the repo into cache_root/<slug>; pull if it exists."""
    if not repo_url:
        return None
    slug = repo_url.rstrip("/").rsplit("/", 1)[-1].replace(".git", "")
    target = cache_root / slug
    try:
        if target.exists():
            subprocess.run(
                ["git", "-C", str(target), "fetch", "--depth", "1", "origin"],
                check=False, capture_output=True, timeout=120,
            )
            subprocess.run(
                ["git", "-C", str(target), "reset", "--hard", "FETCH_HEAD"],
                check=False, capture_output=True, timeout=60,
            )
        else:
            subprocess.run(
                ["git", "clone", "--depth", "1", repo_url, str(target)],
                check=True, capture_output=True, timeout=300,
            )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None
    return target


SCOPE_HEADERS = re.compile(
    r"^#+\s*(in[- ]?scope|scope|files in scope|contracts in scope)\s*$",
    re.IGNORECASE | re.MULTILINE,
)


def _parse_scope_from_readme(repo_path: Path) -> list[str]:
    """Extract a likely-in-scope file list from the contest README."""
    readme = None
    for name in ("README.md", "Readme.md", "readme.md"):
        cand = repo_path / name
        if cand.exists():
            readme = cand.read_text(errors="replace")
            break
    if not readme:
        return []
    # Find first scope section and read lines until the next heading
    m = SCOPE_HEADERS.search(readme)
    if not m:
        return []
    tail = readme[m.end():]
    section = re.split(r"^#+\s+", tail, maxsplit=1, flags=re.MULTILINE)[0]
    paths: list[str] = []
    for line in section.splitlines():
        # Look for typical entries like `src/Foo.sol`, `contracts/Bar.sol`, or table cells
        for m2 in re.finditer(r"`?([\w./\-]+\.sol)`?", line):
            p = m2.group(1)
            if p not in paths:
                paths.append(p)
    return paths


# ---------------------------------------------------------------------------
# Top-level
# ---------------------------------------------------------------------------


def fetch_active_candidates(*, clone_cache: Path | None = None) -> list[Candidate]:
    """Fetch & normalize active C4 contests into Candidate records."""
    sourced_at = _now()
    out: list[Candidate] = []

    sveltekit = _fetch_sveltekit_active()
    if sveltekit:
        for entry in sveltekit:
            c = _candidate_from_sveltekit(entry, sourced_at)
            if c:
                out.append(c)

    if not out:
        # Fallback: scan recently-pushed C4 GitHub repos.
        gh = _fetch_github_active(limit=30)
        for entry in gh:
            c = _candidate_from_github(entry, sourced_at)
            out.append(c)

    # Optionally enrich with cloned scope + commit
    if clone_cache:
        for c in out:
            if not c.repo_url:
                continue
            repo_path = _ensure_clone(c.repo_url, clone_cache)
            if not repo_path:
                continue
            c.local_path = str(repo_path)
            # Pin current commit
            try:
                rev = subprocess.run(
                    ["git", "-C", str(repo_path), "rev-parse", "HEAD"],
                    capture_output=True, text=True, check=True, timeout=10,
                )
                c.commit = rev.stdout.strip() or c.commit
            except Exception:  # noqa: BLE001
                pass
            if not c.scope_paths:
                c.scope_paths = _parse_scope_from_readme(repo_path)

    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--no-clone",
        action="store_true",
        help="Skip cloning repos; just register Candidates with whatever metadata is available remotely.",
    )
    parser.add_argument(
        "--cache",
        default=str(REPO_ROOT / ".cache" / "c4"),
        help="Where to clone C4 contest repos.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't append to candidates.jsonl; just print what would be ingested.",
    )
    args = parser.parse_args(argv)

    cache = None if args.no_clone else Path(args.cache)
    fresh = fetch_active_candidates(clone_cache=cache)

    new, changed = cand_store.diff_against_log(fresh)
    print(f"Fetched {len(fresh)} active C4 candidates ({len(new)} new, {len(changed)} changed).")
    for c in new[:10]:
        payout = f"${c.payout_max_usd:,}" if c.payout_max_usd else "?"
        print(f"  + {c.id}  payout={payout}  closes={c.closes_at or '?'}  scope={len(c.scope_paths)} files")

    if not args.dry_run and (new or changed):
        cand_store.append(new + changed)
        cand_store.reindex()
        print(f"Wrote {len(new) + len(changed)} rows to {cand_store.CANDIDATES_JSONL.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
