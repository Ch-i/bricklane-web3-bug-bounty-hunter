"""Attack composition graph — maps how patterns chain into real exploits.

Edges represent real-world attack chains: pattern A + pattern B = exploit.
Auto-discovers additional links by mining synthesis note cross-references.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from harness.autoresearch import TOPIC_QUEUE, DOMAINS, get_topics_with_status
from harness.corpus import corpus_dir, REPO_ROOT


@dataclass
class Incident:
    name: str
    loss_usd: str
    date: str
    description: str


@dataclass
class CompositionEdge:
    source: str  # pattern slug
    target: str  # pattern slug
    severity: str  # Critical, High
    incidents: list[Incident] = field(default_factory=list)
    description: str = ""

    @property
    def weight(self) -> int:
        return len(self.incidents) + 1


# ---------------------------------------------------------------------------
# Known attack chains — manually curated from real exploits
# ---------------------------------------------------------------------------

KNOWN_EDGES: list[CompositionEdge] = [
    CompositionEdge(
        "flash-loan-mechanics", "oracle-aggregation-staleness", "Critical",
        [Incident("Euler Finance", "$197M", "2023-03-13", "Flash loan + oracle manipulation via donate()"),
         Incident("Mango Markets", "$114M", "2022-10-11", "Flash-funded oracle manipulation on perp market"),
         Incident("Cream Finance", "$130M", "2021-10-27", "Flash loan oracle price manipulation")],
        "Flash loans provide capital to manipulate on-chain oracles within a single transaction."
    ),
    CompositionEdge(
        "flash-loan-mechanics", "checks-effects-interactions", "Critical",
        [Incident("bZx", "$8M", "2020-02-15", "Flash loan + reentrancy on margin trading"),
         Incident("Lendf.me", "$25M", "2020-04-19", "ERC-777 reentrancy via flash-borrowed tokens"),
         Incident("Rari Capital", "$80M", "2022-04-30", "Flash loan reentrancy via cETH")],
        "Flash loans amplify reentrancy by providing unbounded capital for recursive calls."
    ),
    CompositionEdge(
        "flash-loan-mechanics", "erc4626-tokenized-vault-standard", "Critical",
        [Incident("ERC-4626 Inflation", "varies", "2022+", "Flash-funded first-depositor inflation attack on vaults")],
        "Flash loans enable the first-depositor inflation attack by providing donation capital."
    ),
    CompositionEdge(
        "flash-loan-mechanics", "liquidation-mechanics-health-factor", "Critical",
        [Incident("Deus DAO", "$13.4M", "2022-04-28", "Flash loan to manipulate price, trigger liquidations"),
         Incident("Venus Protocol", "$200M", "2021-05-19", "Price manipulation causing mass liquidations")],
        "Flash loans manipulate collateral prices to trigger cascading liquidations."
    ),
    CompositionEdge(
        "checks-effects-interactions", "erc4626-tokenized-vault-standard", "Critical",
        [Incident("Read-only Reentrancy", "varies", "2023+", "Re-entering vault view functions during state transition")],
        "Reentrancy into vault share price calculations during deposit/withdraw."
    ),
    CompositionEdge(
        "oracle-aggregation-staleness", "liquidation-mechanics-health-factor", "Critical",
        [Incident("Compound v2 Oracle", "$89M", "2022-10", "Stale oracle price → incorrect liquidations")],
        "Stale oracle prices cause incorrect health factor calculations and bad liquidations."
    ),
    CompositionEdge(
        "proxy-upgrade-patterns", "access-control-hierarchies", "Critical",
        [Incident("Nomad Bridge", "$190M", "2022-08-01", "Compromised upgrade → drained bridge"),
         Incident("Ronin Bridge", "$624M", "2022-03-29", "Validator key compromise → unauthorized upgrade"),
         Incident("Wormhole", "$320M", "2022-02-02", "Uninitialized proxy → governance bypass")],
        "Weak access control on proxy upgrades enables full protocol takeover."
    ),
    CompositionEdge(
        "signature-replay-eip712", "cross-chain-message-passing", "High",
        [Incident("Wormhole", "$320M", "2022-02-02", "Signature verification bypass on cross-chain VAA")],
        "Signature replay across chains when domain separator doesn't include chainId."
    ),
    CompositionEdge(
        "timelock-governance-patterns", "flash-loan-mechanics", "High",
        [Incident("Beanstalk", "$182M", "2022-04-17", "Flash loan governance attack — borrow, vote, execute, return")],
        "Flash-borrowed governance tokens to pass and execute a malicious proposal atomically."
    ),
    CompositionEdge(
        "amm-constant-product-invariant", "flash-loan-mechanics", "High",
        [Incident("Pancake Bunny", "$45M", "2021-05-20", "Flash loan sandwich on AMM → price manipulation")],
        "Flash loans provide capital for sandwich attacks on AMM pools."
    ),
    CompositionEdge(
        "integer-overflow-precision-loss", "erc4626-tokenized-vault-standard", "High",
        [],
        "Rounding errors in share/asset conversion create extractable value over time."
    ),
    CompositionEdge(
        "denial-of-service-gas-griefing", "liquidation-mechanics-health-factor", "High",
        [],
        "Gas griefing on liquidation calls prevents timely liquidation → bad debt."
    ),
    CompositionEdge(
        "integer-overflow-precision-loss", "amm-constant-product-invariant", "High",
        [],
        "Precision loss in k calculation allows small amounts to be extracted per swap."
    ),
    CompositionEdge(
        "merkle-proof-verification", "access-control-hierarchies", "Medium",
        [],
        "Weak merkle tree construction allows unauthorized whitelist access."
    ),
]


def _auto_discover_links() -> list[CompositionEdge]:
    """Mine synthesis notes for cross-references between patterns."""
    auto_edges: list[CompositionEdge] = []
    synth_dir = corpus_dir() / "synthesis"
    if not synth_dir.exists():
        return auto_edges

    # Map slugs to their synthesis content
    slug_set = {t.slug for t in TOPIC_QUEUE}

    # For each synthesis note, find references to other pattern slugs
    pattern_refs: dict[str, set[str]] = {}
    for md_file in synth_dir.glob("*.md"):
        slug = md_file.stem
        if slug not in slug_set:
            # Check if it's an alias
            for t in TOPIC_QUEUE:
                if slug in t.alias_slugs:
                    slug = t.slug
                    break
            else:
                continue

        content = md_file.read_text().lower()
        refs = set()
        for other_slug in slug_set:
            if other_slug == slug:
                continue
            # Check if the other pattern's keywords appear in this note
            other_title = ""
            for t in TOPIC_QUEUE:
                if t.slug == other_slug:
                    other_title = t.title.lower()
                    break
            if other_title and other_title in content:
                refs.add(other_slug)
        if refs:
            pattern_refs[slug] = refs

    # Create edges from cross-references (bidirectional → only add one direction)
    known_pairs = {(e.source, e.target) for e in KNOWN_EDGES}
    known_pairs |= {(e.target, e.source) for e in KNOWN_EDGES}

    for slug, refs in pattern_refs.items():
        for ref_slug in refs:
            pair = tuple(sorted([slug, ref_slug]))
            if pair not in known_pairs:
                auto_edges.append(CompositionEdge(
                    source=pair[0], target=pair[1], severity="Medium",
                    description=f"Cross-referenced in synthesis notes.",
                ))
                known_pairs.add(pair)

    return auto_edges


def get_graph_data() -> dict:
    """Return the full composition graph as nodes + edges for the UI."""
    topics = get_topics_with_status()

    nodes = []
    for t in topics:
        if t["status"] != "done":
            continue
        nodes.append({
            "slug": t["slug"],
            "title": t["title"],
            "domain": t["domain"],
            "domain_label": DOMAINS.get(t["domain"], t["domain"]),
        })

    # Combine known + auto-discovered edges
    all_edges = list(KNOWN_EDGES) + _auto_discover_links()

    # Filter to only include edges where both nodes exist
    node_slugs = {n["slug"] for n in nodes}
    edges = []
    for e in all_edges:
        if e.source in node_slugs and e.target in node_slugs:
            edges.append({
                "source": e.source,
                "target": e.target,
                "severity": e.severity,
                "weight": e.weight,
                "description": e.description,
                "incidents": [
                    {"name": i.name, "loss_usd": i.loss_usd, "date": i.date, "description": i.description}
                    for i in e.incidents
                ],
            })

    return {"nodes": nodes, "edges": edges}
