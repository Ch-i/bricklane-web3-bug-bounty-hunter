"""Autoresearch scheduler — topic queue for continuous knowledge synthesis.

Maintains a curated list of web3 logic patterns grouped by domain, tracks
which have been synthesized, and drives batch synthesis runs.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Literal

from harness.corpus import REPO_ROOT, corpus_dir

# ---------------------------------------------------------------------------
# Topic registry — the "what to research" queue
# ---------------------------------------------------------------------------

DOMAINS = {
    "defi": "DeFi Primitives",
    "security": "Security Patterns",
    "economics": "Economic Logic",
    "infrastructure": "Infrastructure",
    "governance": "Governance",
    "mev": "MEV & Ordering",
}

@dataclass
class ResearchTopic:
    slug: str
    title: str
    domain: str
    seed_query: str
    description: str = ""
    status: Literal["pending", "running", "done", "failed"] = "pending"
    error: str | None = None
    # Existing synthesis notes that cover this topic (different slug but same content)
    alias_slugs: list[str] = field(default_factory=list)


# Curated topic queue — each is a web3 logic pattern worth indexing
TOPIC_QUEUE: list[ResearchTopic] = [
    # --- DeFi Primitives ---
    ResearchTopic("amm-constant-product-invariant", "AMM Constant Product Invariant (x*y=k)", "defi",
                  "AMM constant product invariant x*y=k Uniswap liquidity",
                  "The mathematical foundation of automated market making: how x*y=k creates price discovery without order books."),
    ResearchTopic("flash-loan-mechanics", "Flash Loan Mechanics & Composability", "defi",
                  "flash loan atomic composability arbitrage liquidation",
                  "Uncollateralized loans that exist within a single transaction — the purest expression of atomic composability.",
                  alias_slugs=["flash-loan-attacks-oracle-manipulation-governance-sandwich"]),
    ResearchTopic("erc4626-tokenized-vault-standard", "ERC-4626 Tokenized Vault Standard", "defi",
                  "ERC-4626 vault share inflation attack deposit withdraw",
                  "The universal vault interface: share/asset accounting, inflation attack vectors, and defensive patterns.",
                  alias_slugs=["erc4626-vault-inflation-attack"]),
    ResearchTopic("liquidation-mechanics-health-factor", "Liquidation Mechanics & Health Factor Math", "defi",
                  "lending liquidation health factor collateral ratio bad debt",
                  "How lending protocols compute solvency, trigger liquidations, and prevent bad debt accumulation.",
                  alias_slugs=["lending-liquidations-bad-debt"]),
    ResearchTopic("yield-aggregator-composability", "Yield Aggregator Composability Patterns", "defi",
                  "yield aggregator strategy vault harvest compound",
                  "Multi-protocol yield stacking: how aggregators compose lending, staking, and LP positions."),
    ResearchTopic("stablecoin-peg-mechanisms", "Stablecoin Peg Mechanisms", "defi",
                  "stablecoin peg mechanism CDP algorithmic collateral",
                  "Collateralized, algorithmic, and hybrid peg maintenance — the hardest problem in DeFi."),
    ResearchTopic("concentrated-liquidity-math", "Concentrated Liquidity (Uniswap V3) Math", "defi",
                  "concentrated liquidity tick range Uniswap V3 position",
                  "Tick-based liquidity provision: the math of price ranges, capital efficiency, and impermanent loss."),
    ResearchTopic("ve-tokenomics-gauge-voting", "veTokenomics & Gauge Voting", "defi",
                  "veToken vote escrow gauge voting Curve emissions bribe",
                  "Vote-escrowed tokens, gauge weight voting, and the bribery markets that emerge from them."),

    # --- Security Patterns ---
    ResearchTopic("checks-effects-interactions", "Checks-Effects-Interactions Pattern", "security",
                  "checks effects interactions reentrancy CEI pattern state",
                  "The foundational security pattern: validate, mutate state, then interact with external contracts.",
                  alias_slugs=["reentrancy-variants-beyond-cei-read-only-cross-function-cross-contract-callback-hooks"]),
    ResearchTopic("access-control-hierarchies", "Access Control Hierarchies & Role Systems", "security",
                  "access control role admin modifier onlyOwner AccessControl",
                  "From single-owner to role-based hierarchies: how contracts enforce authorization.",
                  alias_slugs=["access-control-bypasses-missing-modifiers-tx-origin-role-checks"]),
    ResearchTopic("proxy-upgrade-patterns", "Proxy & Upgrade Patterns", "security",
                  "proxy upgrade UUPS transparent beacon storage collision",
                  "Contract upgradeability: transparent proxies, UUPS, beacon patterns, and storage collision risks.",
                  alias_slugs=["proxy-and-upgradeability-pitfalls"]),
    ResearchTopic("integer-overflow-precision-loss", "Integer Overflow & Precision Loss", "security",
                  "integer overflow underflow precision loss rounding dust",
                  "Fixed-point arithmetic in the EVM: rounding directions, dust accumulation, and overflow guards."),
    ResearchTopic("signature-replay-eip712", "Signature Replay & EIP-712 Typed Data", "security",
                  "signature replay EIP-712 nonce domain separator permit",
                  "Off-chain signature schemes: EIP-712 typed data, replay protection, and permit patterns."),
    ResearchTopic("denial-of-service-gas-griefing", "Denial of Service & Gas Griefing", "security",
                  "denial of service gas griefing unbounded loop block gas limit",
                  "How unbounded operations, external call failures, and gas limits create DoS vectors."),

    # --- Economic Logic ---
    ResearchTopic("bonding-curve-token-economics", "Bonding Curve Token Economics", "economics",
                  "bonding curve continuous token price discovery supply",
                  "Continuous token models: how mathematical curves create deterministic price discovery."),
    ResearchTopic("auction-mechanisms-dutch-english", "Auction Mechanisms (Dutch, English, Sealed-Bid)", "economics",
                  "auction dutch english sealed bid gradual mechanism",
                  "On-chain auction design: Dutch auctions for NFTs, liquidation auctions, and MEV resistance."),
    ResearchTopic("fee-distribution-reward-streaming", "Fee Distribution & Reward Streaming", "economics",
                  "fee distribution reward streaming staking dividend per-second",
                  "How protocols distribute fees and rewards: per-second accrual, snapshot vs streaming, JIT capture."),
    ResearchTopic("liquidity-bootstrapping-fair-launch", "Liquidity Bootstrapping & Fair Launch", "economics",
                  "liquidity bootstrapping pool LBP fair launch token distribution",
                  "Fair token distribution without VC capture: LBPs, lockdrops, and retroactive airdrops."),

    # --- Infrastructure ---
    ResearchTopic("oracle-aggregation-staleness", "Oracle Aggregation & Staleness Detection", "infrastructure",
                  "oracle aggregation Chainlink staleness heartbeat TWAP fallback",
                  "Multi-source price feeds: Chainlink integration, staleness checks, TWAP fallbacks, and manipulation resistance.",
                  alias_slugs=["oracle-staleness-and-price-feed-manipulation"]),
    ResearchTopic("cross-chain-message-passing", "Cross-Chain Message Passing", "infrastructure",
                  "cross chain bridge message passing relay verification",
                  "How bridges and messaging protocols verify cross-chain state: light clients, optimistic, and ZK approaches.",
                  alias_slugs=["bridge-token-attacks", "cross-chain-bridge-replay-and-signature-verification-flaws"]),
    ResearchTopic("rollup-sequencing-state-proofs", "Rollup Sequencing & State Proofs", "infrastructure",
                  "rollup sequencer state proof L2 batch submission",
                  "L2 architecture: sequencer responsibilities, state root submission, fraud/validity proofs."),
    ResearchTopic("account-abstraction-erc4337", "Account Abstraction (ERC-4337)", "infrastructure",
                  "account abstraction ERC-4337 UserOperation bundler paymaster",
                  "Programmable accounts: UserOperations, bundlers, paymasters, and the alt mempool.",
                  alias_slugs=["erc4337-account-abstraction"]),
    ResearchTopic("merkle-proof-verification", "Merkle Proof Verification Patterns", "infrastructure",
                  "merkle proof tree verification whitelist airdrop",
                  "On-chain set membership proofs: airdrop whitelists, state verification, and proof manipulation risks."),

    # --- Governance ---
    ResearchTopic("timelock-governance-patterns", "Timelock & Governance Execution", "governance",
                  "timelock governance propose delay execute cancel queue",
                  "Time-delayed execution: how DAOs protect against malicious proposals with mandatory waiting periods.",
                  alias_slugs=["governance-timelock-signature-attacks"]),
    ResearchTopic("delegation-voting-power-math", "Delegation & Voting Power Math", "governance",
                  "delegation voting power checkpoint snapshot block number",
                  "Vote delegation, checkpointing, and the math of preventing double-voting across blocks."),
    ResearchTopic("optimistic-governance-veto", "Optimistic Governance & Veto Mechanisms", "governance",
                  "optimistic governance veto emergency guardian multisig",
                  "Execute-unless-vetoed patterns: how protocols balance speed with safety using guardian roles."),

    # --- MEV & Ordering ---
    ResearchTopic("proposer-builder-separation", "Proposer-Builder Separation (PBS)", "mev",
                  "PBS proposer builder separation MEV boost relay",
                  "How Ethereum separates block building from proposing: MEV-Boost, relays, and builder markets."),
    ResearchTopic("intent-based-execution", "Intent-Based Execution & Order Flow", "mev",
                  "intent based execution order flow auction solver CoW",
                  "From explicit transactions to declared intents: solvers, batch auctions, and MEV internalization."),
    ResearchTopic("private-mempool-sequencing", "Private Mempool & Sequencing Guarantees", "mev",
                  "private mempool sequencing FCFS encrypted mempool",
                  "How private order flow, encrypted mempools, and FCFS sequencing change the MEV landscape."),
    ResearchTopic("backrunning-arbitrage-patterns", "Backrunning & Arbitrage Patterns", "mev",
                  "backrun arbitrage DEX price alignment cross-pool",
                  "Benign MEV: how arbitrage bots align prices across pools and the contracts they use."),
]


# ---------------------------------------------------------------------------
# State persistence
# ---------------------------------------------------------------------------

STATE_PATH = REPO_ROOT / "autoresearch-state.json"


def _load_state() -> dict[str, dict]:
    """Load topic statuses from disk."""
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _save_state(state: dict[str, dict]) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2))


def _check_synthesis_exists(topic: ResearchTopic) -> bool:
    """Check if a synthesis note already exists for this topic or its aliases."""
    # Check the primary slug
    note_path = corpus_dir() / "synthesis" / f"{topic.slug}.md"
    if note_path.exists():
        return True
    # Check alias slugs (existing synthesis notes with different names)
    for alias in topic.alias_slugs:
        alias_path = corpus_dir() / "synthesis" / f"{alias}.md"
        if alias_path.exists():
            return True
    return False


def _get_synthesis_id(topic: ResearchTopic) -> str | None:
    """Return the corpus ID of the synthesis note for this topic."""
    # Check primary slug
    note_path = corpus_dir() / "synthesis" / f"{topic.slug}.md"
    if note_path.exists():
        return f"synthesis-{topic.slug}"
    # Check aliases
    for alias in topic.alias_slugs:
        alias_path = corpus_dir() / "synthesis" / f"{alias}.md"
        if alias_path.exists():
            return f"synthesis-{alias}"
    return None


def get_topics_with_status() -> list[dict]:
    """Return all topics with their current status."""
    state = _load_state()
    results = []
    for t in TOPIC_QUEUE:
        info = asdict(t)
        # Override status from persisted state or from filesystem
        if t.slug in state:
            info["status"] = state[t.slug].get("status", "pending")
            info["error"] = state[t.slug].get("error")
        elif _check_synthesis_exists(t):
            info["status"] = "done"
        # Include the resolved synthesis ID
        info["synthesis_id"] = _get_synthesis_id(t)
        results.append(info)
    return results


def get_domains_summary() -> list[dict]:
    """Return domain summaries with counts."""
    topics = get_topics_with_status()
    domain_counts: dict[str, dict] = {}
    for t in topics:
        d = t["domain"]
        if d not in domain_counts:
            domain_counts[d] = {"domain": d, "label": DOMAINS.get(d, d), "total": 0, "done": 0, "pending": 0, "failed": 0}
        domain_counts[d]["total"] += 1
        domain_counts[d][t["status"]] = domain_counts[d].get(t["status"], 0) + 1
    return list(domain_counts.values())


def run_batch(n: int = 3) -> list[dict]:
    """Run synthesis for the next N pending topics. Returns results."""
    from harness.synthesize import synthesize

    state = _load_state()
    topics = get_topics_with_status()
    pending = [t for t in topics if t["status"] == "pending"][:n]

    results = []
    for t in pending:
        state[t["slug"]] = {"status": "running"}
        _save_state(state)

        try:
            result = synthesize(
                topic=t["title"],
                seed_query=t["seed_query"],
                slug=t["slug"],
                reindex_after=True,
            )
            if result.error:
                state[t["slug"]] = {"status": "failed", "error": result.error}
            else:
                state[t["slug"]] = {"status": "done"}
            results.append({"slug": t["slug"], "status": state[t["slug"]]["status"], "error": result.error})
        except Exception as e:
            state[t["slug"]] = {"status": "failed", "error": str(e)}
            results.append({"slug": t["slug"], "status": "failed", "error": str(e)})

        _save_state(state)

    return results
