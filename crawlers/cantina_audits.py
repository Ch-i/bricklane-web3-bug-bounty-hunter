"""Cantina active-competition ingestor.

Cantina (cantina.xyz) hosts time-boxed Solidity audit competitions. We
try (in priority order):

  1. cantina.xyz/api/v0/competitions or similar JSON endpoint
  2. github.com/CantinaCompetitions (heuristic name) repo listing
  3. cantina.xyz/competitions HTML scrape

Cantina is the most opaque of the four (their API isn't well-documented
publicly), so this ingestor errs on the side of "register the contest
even with partial metadata" — the sweep can then enrich via clone+README.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import httpx

from harness import candidates as cand_store
from harness.candidates import Candidate
from harness.corpus import REPO_ROOT

CANTINA_BASE = "https://cantina.xyz"
USER_AGENT = "web3sentinel-cantina-ingestor/0.1 (research)"


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _http_get(url: str, *, timeout: float = 30.0) -> httpx.Response:
    return httpx.get(
        url,
        timeout=timeout,
        follow_redirects=True,
        headers={"User-Agent": USER_AGENT, "Accept": "application/json, text/html"},
    )


def _fetch_api() -> list[dict] | None:
    for path in (
        "/api/v0/competitions",
        "/api/competitions",
        "/api/v0/competitions?status=open",
    ):
        try:
            r = _http_get(f"{CANTINA_BASE}{path}")
        except httpx.HTTPError:
            continue
        if r.status_code != 200:
            continue
        try:
            data = r.json()
        except ValueError:
            continue
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            for k in ("competitions", "data", "results", "items"):
                if isinstance(data.get(k), list):
                    return data[k]
    return None


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
    for k in ("slug", "name", "id", "title"):
        v = entry.get(k)
        if isinstance(v, str) and v:
            return re.sub(r"[^a-z0-9-]+", "-", v.lower()).strip("-")
    return None


def _candidate_from_api(entry: dict, sourced_at: str) -> Candidate | None:
    s = _slug(entry)
    if not s:
        return None
    title = entry.get("title") or entry.get("name") or s
    payout = _parse_payout(entry.get("rewards") or entry.get("total_prize") or entry.get("prize"))
    closes_at = _parse_iso(entry.get("end_date") or entry.get("ends_at"))
    repo_url = entry.get("repo") or entry.get("repository_url") or entry.get("github_url")
    return Candidate(
        id=f"cantina-{s}",
        platform="cantina",
        kind="source-only",
        title=str(title),
        sourced_at=sourced_at,
        payout_max_usd=payout,
        closes_at=closes_at,
        repo_url=repo_url,
        commit=entry.get("commit"),
        scope_paths=list(entry.get("scope") or []),
        notes=(entry.get("description") or "")[:1000],
    )


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
    parser.add_argument("--cache", default=str(REPO_ROOT / ".cache" / "cantina"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    cache = None if args.no_clone else Path(args.cache)
    fresh = fetch_active_candidates(clone_cache=cache)
    new, changed = cand_store.diff_against_log(fresh)
    print(f"Fetched {len(fresh)} active Cantina candidates ({len(new)} new, {len(changed)} changed).")
    for c in new[:10]:
        payout = f"${c.payout_max_usd:,}" if c.payout_max_usd else "?"
        print(f"  + {c.id}  payout={payout}  closes={c.closes_at or '?'}")
    if not args.dry_run and (new or changed):
        cand_store.append(new + changed)
        cand_store.reindex()
    return 0


if __name__ == "__main__":
    sys.exit(main())
