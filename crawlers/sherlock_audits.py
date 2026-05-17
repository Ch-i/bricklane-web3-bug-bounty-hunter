"""Sherlock active-audit ingestor.

Sherlock contests resemble C4: time-boxed source-only audits with a
GitHub repo + scope. We pull from (in priority order):

  1. audits.sherlock.xyz/api/audits — JSON; the platform exposes its
     contest list via a public endpoint used by their own SPA.
  2. github.com/sherlock-protocol — fallback for recently-pushed contest
     repos when the API is unreachable.
  3. The audits.sherlock.xyz HTML page — last-resort scrape.

Output: normalized Candidate records (platform="sherlock").
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import httpx

from harness import candidates as cand_store
from harness.candidates import Candidate
from harness.corpus import REPO_ROOT

SHERLOCK_BASE = "https://audits.sherlock.xyz"
GH_SHERLOCK_ORG = "sherlock-protocol"
USER_AGENT = "web3sentinel-sherlock-ingestor/0.1 (research)"


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
# Sources
# ---------------------------------------------------------------------------


def _fetch_api() -> list[dict] | None:
    """Try Sherlock's API directly. Returns None on miss."""
    for path in ("/api/audits", "/api/audits?status=ongoing", "/api/contests"):
        try:
            r = _http_get(f"{SHERLOCK_BASE}{path}")
        except httpx.HTTPError:
            continue
        if r.status_code != 200:
            continue
        try:
            data = r.json()
        except ValueError:
            continue
        # API shapes vary; flatten to a list of contest-like dicts
        candidates: list[dict] = []
        if isinstance(data, list):
            candidates = data
        elif isinstance(data, dict):
            for key in ("audits", "contests", "results", "data"):
                if isinstance(data.get(key), list):
                    candidates.extend(data[key])
        # Filter to only those that look ongoing / open
        active = [
            c for c in candidates
            if isinstance(c, dict)
            and (c.get("status") in ("ongoing", "active", "open", "Ongoing", "Active")
                 or c.get("ends_at") or c.get("end_date"))
        ]
        if active:
            return active
    return None


def _fetch_github(limit: int = 30) -> list[dict]:
    url = f"https://api.github.com/orgs/{GH_SHERLOCK_ORG}/repos?sort=pushed&per_page={limit}"
    try:
        r = _http_get(url, timeout=20.0)
    except httpx.HTTPError:
        return []
    if r.status_code != 200:
        return []
    repos = r.json()
    if not isinstance(repos, list):
        return []
    out: list[dict] = []
    for repo in repos:
        name = repo.get("name") or ""
        # Sherlock contest repos vary in naming; common patterns:
        #   <year>-<month>-<protocol>-judging, <protocol>-contest, ...
        if not name or repo.get("archived"):
            continue
        # Heuristic: contest-shaped repos
        if not re.search(r"(audit|contest|judging)", name, re.IGNORECASE):
            continue
        out.append({
            "name": name,
            "html_url": repo.get("html_url"),
            "clone_url": repo.get("clone_url"),
            "pushed_at": repo.get("pushed_at"),
            "default_branch": repo.get("default_branch", "main"),
            "description": repo.get("description") or "",
        })
    return out


# ---------------------------------------------------------------------------
# Normalize
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
        ts = value / 1000 if value > 10**12 else value
        return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()
    return None


def _slug(entry: dict) -> str | None:
    for k in ("slug", "name", "id", "uniqueId", "title"):
        v = entry.get(k)
        if isinstance(v, str) and v:
            return re.sub(r"[^a-z0-9-]+", "-", v.lower()).strip("-")
    return None


def _candidate_from_api(entry: dict, sourced_at: str) -> Candidate | None:
    s = _slug(entry)
    if not s:
        return None
    title = entry.get("title") or entry.get("name") or s
    payout = _parse_payout(
        entry.get("rewards") or entry.get("amount")
        or entry.get("totalReward") or entry.get("prize_pool")
    )
    closes_at = _parse_iso(entry.get("ends_at") or entry.get("end_date") or entry.get("endTime"))
    repo_url = entry.get("repo") or entry.get("repository") or entry.get("github_url")
    return Candidate(
        id=f"sherlock-{s}",
        platform="sherlock",
        kind="source-only",
        title=str(title),
        sourced_at=sourced_at,
        payout_max_usd=payout,
        closes_at=closes_at,
        repo_url=repo_url,
        commit=entry.get("commit") or entry.get("commit_hash"),
        scope_paths=list(entry.get("scope") or entry.get("in_scope") or []),
        notes=(entry.get("description") or entry.get("summary") or "")[:1000],
    )


def _candidate_from_github(entry: dict, sourced_at: str) -> Candidate:
    name = entry["name"]
    return Candidate(
        id=f"sherlock-{name}",
        platform="sherlock",
        kind="source-only",
        title=name.replace("-", " "),
        sourced_at=sourced_at,
        repo_url=entry.get("html_url"),
        commit=None,
        scope_paths=[],
        notes=(entry.get("description") or "")[:1000],
    )


# Reuse the clone/scope helpers from the C4 module — they're generic.
from crawlers.c4_contests import _ensure_clone, _parse_scope_from_readme  # noqa: E402


def fetch_active_candidates(*, clone_cache: Path | None = None) -> list[Candidate]:
    sourced_at = _now()
    out: list[Candidate] = []

    api = _fetch_api()
    if api:
        for entry in api:
            c = _candidate_from_api(entry, sourced_at)
            if c:
                out.append(c)

    if not out:
        gh = _fetch_github(limit=30)
        for entry in gh:
            out.append(_candidate_from_github(entry, sourced_at))

    if clone_cache:
        for c in out:
            if not c.repo_url:
                continue
            repo_path = _ensure_clone(c.repo_url, clone_cache)
            if not repo_path:
                continue
            c.local_path = str(repo_path)
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
    parser.add_argument("--no-clone", action="store_true")
    parser.add_argument("--cache", default=str(REPO_ROOT / ".cache" / "sherlock"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    cache = None if args.no_clone else Path(args.cache)
    fresh = fetch_active_candidates(clone_cache=cache)

    new, changed = cand_store.diff_against_log(fresh)
    print(f"Fetched {len(fresh)} active Sherlock candidates ({len(new)} new, {len(changed)} changed).")
    for c in new[:10]:
        payout = f"${c.payout_max_usd:,}" if c.payout_max_usd else "?"
        print(f"  + {c.id}  payout={payout}  closes={c.closes_at or '?'}")

    if not args.dry_run and (new or changed):
        cand_store.append(new + changed)
        cand_store.reindex()
    return 0


if __name__ == "__main__":
    sys.exit(main())
