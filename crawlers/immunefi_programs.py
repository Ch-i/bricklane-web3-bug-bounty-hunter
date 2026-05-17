"""Immunefi continuous-bounty ingestor.

Immunefi differs from C4/Sherlock/Cantina: programs are continuous (no
deadline), each has a per-program scope of deployed addresses, and the
payout is "up to" with a per-severity table.

We pull (in priority order):
  1. immunefi.com/api/projects — Immunefi exposes a public JSON of all
     bounty programs through their explorer API.
  2. immunefi.com/explore HTML scrape — fallback.

Output: Candidate records with kind="deployed", addresses populated from
the program's scope. payout_max_usd = the program's max bounty cap.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import httpx

from harness import candidates as cand_store
from harness.candidates import Candidate
from harness.corpus import REPO_ROOT

IMMUNEFI_BASE = "https://immunefi.com"
USER_AGENT = "web3sentinel-immunefi-ingestor/0.1 (research)"

CHAIN_NAME_TO_ID = {
    "ethereum": 1, "eth": 1, "mainnet": 1,
    "optimism": 10, "op": 10,
    "arbitrum": 42161, "arb": 42161,
    "polygon": 137, "matic": 137,
    "base": 8453,
    "bsc": 56, "binance": 56,
    "avalanche": 43114, "avax": 43114,
}


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
    # Immunefi's data endpoints have moved a few times; try common ones.
    for path in (
        "/api/projects",
        "/api/explore",
        "/api/v1/projects",
        "/api/bounties",
    ):
        try:
            r = _http_get(f"{IMMUNEFI_BASE}{path}")
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
            for k in ("projects", "bounties", "data", "results", "items"):
                if isinstance(data.get(k), list):
                    return data[k]
    return None


_ADDR_RE = re.compile(r"\b0x[a-fA-F0-9]{40}\b")


def _extract_addresses(scope_field) -> tuple[list[str], int | None]:
    """Best-effort address + chain_id extraction from heterogeneous scope shapes.

    Returns (addresses, chain_id_if_unambiguous).
    """
    addrs: list[str] = []
    chain_id: int | None = None
    if isinstance(scope_field, list):
        for item in scope_field:
            if isinstance(item, str):
                addrs.extend(_ADDR_RE.findall(item))
            elif isinstance(item, dict):
                for v in item.values():
                    if isinstance(v, str):
                        addrs.extend(_ADDR_RE.findall(v))
                # If the scope object has a chain hint, capture it
                for k in ("chain", "network", "blockchain"):
                    val = item.get(k)
                    if isinstance(val, str):
                        c = CHAIN_NAME_TO_ID.get(val.lower())
                        if c and chain_id is None:
                            chain_id = c
    elif isinstance(scope_field, dict):
        flat = json.dumps(scope_field)
        addrs.extend(_ADDR_RE.findall(flat))
        for k in ("chain", "network", "blockchain"):
            val = scope_field.get(k)
            if isinstance(val, str):
                c = CHAIN_NAME_TO_ID.get(val.lower())
                if c and chain_id is None:
                    chain_id = c
    elif isinstance(scope_field, str):
        addrs.extend(_ADDR_RE.findall(scope_field))
    # Dedup, preserve order
    seen: set[str] = set()
    deduped = []
    for a in addrs:
        a_low = a.lower()
        if a_low in seen:
            continue
        seen.add(a_low)
        deduped.append(a)
    return deduped, chain_id


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


def _slug(entry: dict) -> str | None:
    for k in ("slug", "id", "name", "project"):
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
        entry.get("maxBounty") or entry.get("max_bounty")
        or entry.get("totalBounty") or entry.get("bountyMax")
        or entry.get("rewards")
    )

    addrs, chain_id = _extract_addresses(
        entry.get("scope") or entry.get("assets") or entry.get("targets") or {}
    )
    return Candidate(
        id=f"immunefi-{s}",
        platform="immunefi",
        kind="deployed",
        title=str(title),
        sourced_at=sourced_at,
        payout_max_usd=payout,
        closes_at=None,  # Immunefi is continuous
        addresses=addrs,
        chain_id=chain_id,
        notes=(entry.get("description") or entry.get("summary") or "")[:1500],
    )


def fetch_active_candidates() -> list[Candidate]:
    """Immunefi candidates don't need cloning (kind=deployed); source fetch
    happens later via harness.onchain when audited."""
    sourced_at = _now()
    out: list[Candidate] = []
    api = _fetch_api()
    if api:
        for entry in api:
            c = _candidate_from_api(entry, sourced_at)
            if c:
                out.append(c)
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    fresh = fetch_active_candidates()
    new, changed = cand_store.diff_against_log(fresh)
    print(f"Fetched {len(fresh)} active Immunefi candidates ({len(new)} new, {len(changed)} changed).")
    for c in new[:10]:
        payout = f"${c.payout_max_usd:,}" if c.payout_max_usd else "?"
        n_addr = len(c.addresses) if c.addresses else 0
        print(f"  + {c.id}  payout={payout}  addresses={n_addr}  chain={c.chain_id or '?'}")
    if not args.dry_run and (new or changed):
        cand_store.append(new + changed)
        cand_store.reindex()
    return 0


if __name__ == "__main__":
    sys.exit(main())
