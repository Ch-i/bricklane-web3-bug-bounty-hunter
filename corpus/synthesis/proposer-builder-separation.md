---
id: synthesis-proposer-builder-separation
source: synthesis
source_url: null
title: "Proposer-Builder Separation (PBS): pattern, variants, audit checklist"
ingested_at: 2026-06-04T21:25:31+00:00
vuln_class:
  - mev
  - front-running
  - sandwich
  - transaction-ordering
  - censorship
  - centralization
  - trust-assumptions
protocol_category:
  - consensus-infrastructure
  - staking
  - validator
  - block-building
  - dex
tags:
  - synthesis
  - pbs
  - mev-boost
  - relay
  - builder
  - proposer
derives_from:
  - arxiv-2602.15395
  - arxiv-2605.04471
  - arxiv-2602.04007
  - arxiv-2603.07716
  - arxiv-2603.26290
  - arxiv-2603.27739
  - arxiv-2601.20783
  - arxiv-2604.21169
  - arxiv-2601.19570
  - solodit-zachobront-2023-09-01-obol-3-0
  - solodit-hexens-2023-10-02-mantle-1-2
  - solodit-hexens-2023-10-02-mantle-1-1
  - rekt-moneyfornothing
  - rekt-ripmevbot2
  - swc-114
---

# Proposer-Builder Separation (PBS)

## Pattern

Proposer-Builder Separation splits block production into two roles. **Builders**
collect transactions (often from private order flow that bypasses the public
mempool), order them to maximize extractable value, and produce a full block.
**Proposers** (validators) only choose the most valuable block *header* offered
to them, sign it, and propose it — usually through a trusted **relay** that
escrows the body until the proposer commits. On Ethereum this is realized
off-protocol by **MEV-Boost**; on BNB Smart Chain a leaner, whitelisted PBS is
baked in. The stated goal is to democratize MEV: a hobbyist validator gets the
same block value as a sophisticated one without running searching infrastructure
itself. The SoK on MEV's evolution places PBS and MEV-Boost squarely in "Era II,"
the move from Miner-Extractable to Maximal-Extractable Value, alongside formal
MEV taxonomies and non-atomic / CEX-DEX arbitrage [arxiv-2603.07716].

The security-relevant consequence is that **ordering power concentrates**. The
party that builds the block decides what gets included, excluded, front-run,
back-run, or sandwiched. Empirically, the builder market under PBS centralizes:
on Ethereum, builder dominance is described as an *emergent property of the PBS
framework itself*, because the architecture systematically violates the
prerequisites of a competitive market — early dominance was won through
Exclusive Order Flows (EOFs) and incumbents then locked it in via network
effects [arxiv-2605.04471]. On BSC the effect is sharper: only whitelisted
builders may participate, blocks come at shorter intervals, and private order
flow bypasses the public mempool, so two builders (48Club and Blockrazor)
produced over 87% of blocks and captured 90%+ of MEV profit, with the short block
interval *collapsing the contestable window* and amplifying latency advantages
[arxiv-2602.15395]. MEV-Boost itself is characterized as highly centralized "due
to integration," which distorts competition, reduces blockspace efficiency, and
obscures MEV flow transparency [arxiv-2602.04007].

Because ordering is for sale, *any* privileged on-chain action that executes as
an ordinary transaction — a stablecoin freeze, an emergency pause, a governance
intervention, a judicial seizure — is just another bid competing for block-space
priority. Whoever controls ordering controls the outcome, which is why "ordering
power is sanctioning power": block producers extract rents (Sanction-Evasion MEV)
from the race between a freeze and the sanctioned party's escape transfer
[arxiv-2603.27739]. For auditors, PBS is not only a consensus-layer concern: the
roles it separates (intent originator, executor/searcher, beneficiary) decouple
in ways that break naive on-chain attribution and create new trust assumptions
wherever protocol code consumes relay/beacon data or assumes honest block
construction [arxiv-2603.26290][solodit-zachobront-2023-09-01-obol-3-0].

## Variants

### V1: Builder/relay centralization and order-flow capture

The dominant systemic risk. A small number of builders win persistent market
share through Exclusive Order Flows and integration with searchers, then keep it
through network effects even after decoupling from immediate EOF dependency
[arxiv-2605.04471]. Whitelisted PBS plus short block intervals (BSC) makes the
contestable window so small that slower builders and searchers are structurally
excluded, concentrating both block production and MEV profit and making the chain
*more* censorship-prone and fairness-eroded than Ethereum [arxiv-2602.15395].
Mitigation proposals (Boost+) try to restore equitability by decoupling
*collecting* transactions from *ordering* them and guaranteeing equal access to
all collected transactions, with mechanisms that make truthful bidding a dominant
strategy for builders and searchers [arxiv-2602.04007].

### V2: Proposer dishonesty / payment & metadata manipulation

A proposer (or a validator's node operators) is *supposed* to honor the fee and
MEV-payment metadata in a block built for it, enforced only by social consensus —
builders avoid harming validators so their future blocks keep getting accepted.
A party not bound by that social consensus can defect. In Obol's DVT, a majority
of node operators able to reach consensus could build blocks that route large MEV
payments to their *own* address instead of the validator's 0xSplit, attach
fictitious header metadata, and have fellow operators sign it; because the fee
(coinbase) address is added by the nodes to each block, they can also redirect
all execution-layer fees to a 0xSplit containing only themselves
[solodit-zachobront-2023-09-01-obol-3-0]. The flip side is the proposer-payment
economics: searchers bid almost the entire profit back to the proposer — one MEV
bot paid **98%** of its take as a bribe to the block's solo validator
[rekt-moneyfornothing].

### V3: Ordering power weaponized against privileged actions (SE-MEV / censorship)

When a privileged transaction (blacklist freeze, pause, governance action) must
win an ordering race against an adversary's escape transaction, the block
producer — not the legal/contract authority — decides who wins, and can sell that
priority. Measured across USDT/USDC sanctions, at least 7.3% of sanctioned USDT
addresses and 18.7% of sanctioned USDC addresses were drained to zero *before* the
freeze landed, with escalation from public gas auctions to private order flow to
direct payments to block producers, and incentives toward vertical integration
into block-building [arxiv-2603.27739]. Auditors should treat any contract whose
security depends on a privileged tx landing first as exposed to builder/proposer
discretion.

### V4: Trusting unverified relay / beacon / node data

PBS introduces off-chain data surfaces (relays, beacon-node APIs) that protocol
or oracle code may consume without verification. Mantle's oracle retrieved a
`VersionedSignedBeaconBlock` from a third-party node API (QuickNode) without
verifying data or signatures, so forged data from the node would propagate into
oracle reports — remediated by using own/fully-trusted nodes and cross-checking
multiple nodes [solodit-hexens-2023-10-02-mantle-1-2]. Separately it failed to
validate the `execution_optimistic` flag from the beacon API, so it could act on
optimistic (unfinalized, later-invalidatable) state
[solodit-hexens-2023-10-02-mantle-1-1].

### V5: Block-building / simulation denial of service

The builder pipeline itself is an attack surface. Transaction *simulation* is a
core subsystem of block building, and denial of its service degrades block
production and transaction delivery. Beyond single-round (ConditionalExhaust) and
two-round (GhostTX, denial-of-sequencers) attacks, multi-round simulation can be
denied by crafting inter-transaction dependencies that manifest in smart-contract
state [arxiv-2604.21169]. A contract that can cheaply blow up simulation cost is a
DoS lever against builders.

### V6: PEB role decoupling breaks attribution

PBS-style separation generalizes into Principal-Execution-Beneficiary (PEB)
decoupling: the intent originator, the executor (an MEV searcher), and the
ultimate beneficiary are functionally distinct, and value migrates through
invariant-driven state transitions (e.g., AMM reserve rebalancing) rather than
explicit transfers. This makes transfer-graph (AML / fund-tracing) attribution
neither complete nor causally closed [arxiv-2603.26290]. Relevant when reasoning
about who actually profits from an exploit routed through searcher/builder
infrastructure.

### V7: Contract-level transaction-order dependence (the thing PBS monetizes)

At the application layer, the underlying bug class is Transaction Order
Dependence: code whose result depends on the order transactions are mined, where
anyone observing the mempool can reorder by paying for priority (the ERC-20
`approve` race is the canonical example) [swc-114]. PBS doesn't create this bug —
it industrializes its exploitation, since the builder now performs the reordering
deterministically. Note that *without* a builder market the exploit weakens:
sandwiching on rollups with private mempools is probabilistic (no guaranteed
atomic inclusion; attackers rely on sequencer ordering, redundant submissions and
priority-fee placement) and is mostly rare/unprofitable there
[arxiv-2601.19570].

## Audit checklist

- Does any contract invariant rely on a privileged transaction (freeze, pause,
  governance action, liquidation) **winning an ordering race**? If so, it is
  exposed to builder/proposer discretion and is not safe to assume first-in-block
  [arxiv-2603.27739].
- Is protocol/oracle logic consuming **relay or beacon-node data** (blocks,
  headers, validator sets, builder bids) without verifying signatures or
  cross-checking multiple independent nodes? [solodit-hexens-2023-10-02-mantle-1-2]
- Is the code acting on **optimistic / unfinalized** consensus data without
  checking finality flags such as `execution_optimistic`?
  [solodit-hexens-2023-10-02-mantle-1-1]
- For staking / DVT / validator systems: can the **fee (coinbase) recipient or
  MEV payout address** be set or overridden by node operators rather than being
  immutably bound to the protocol's split contract?
  [solodit-zachobront-2023-09-01-obol-3-0]
- Does the design assume builders/proposers behave honestly because of "social
  consensus"? Identify which party is *not* bound by that consensus and what they
  gain by defecting [solodit-zachobront-2023-09-01-obol-3-0].
- Is outcome correctness dependent on **transaction order within a block** (race
  conditions, `approve` double-spend, first-solver rewards, reveal/commit, swap
  sequencing)? Apply slippage bounds, commit-reveal, or order-independent logic
  [swc-114].
- Does the protocol assume execution happens in a **public mempool with a
  competitive builder market**? On chains with whitelisted/centralized builders or
  private order flow, assumptions about fair inclusion and contestable MEV may not
  hold [arxiv-2602.15395][arxiv-2605.04471].
- Can a single transaction make **block/simulation cost explode** via
  inter-transaction or stateful dependencies, giving an adversary a DoS lever on
  the builder pipeline? [arxiv-2604.21169]
- If MEV resistance is claimed via a private mempool / no builder market, is the
  residual risk (sequencer ordering, redundant submission, priority-fee placement)
  actually accounted for rather than assumed away? [arxiv-2601.19570]
- For fund-tracing / AML / accountability assumptions: does the design assume the
  executor equals the beneficiary? PEB decoupling and state-mediated value
  migration break that [arxiv-2603.26290].
- If the protocol proposes its own sequencing/priority scheme, is it
  builder-implementable and incentive-compatible (e.g., monotone contract-set
  priorities, equal-access collection à la Boost+) rather than relying on builder
  goodwill? [arxiv-2601.20783][arxiv-2602.04007]

## Prior incidents

- **Money for Nothing (26 Dec 2023) — $1.3M**: an MEV bot back-ran a Uniswap V3
  fat-finger LP error and paid **98% of the take as a bribe to the block's solo
  validator**, a textbook demonstration of proposer-payment economics under PBS
  and growing validator capture amid liquid-staking centralization
  [cites: rekt-moneyfornothing].
- **RIP MEV Bot 2 (07 Nov 2023) — $2M**: a searcher's own arbitrage contract left
  a swap function unprotected; an attacker used a $50M flash loan to manipulate
  Curve WETH/WBTC pools and sandwich the bot — illustrating the searcher layer of
  the PBS stack as its own attack surface [cites: rekt-ripmevbot2].
- **BSC builder monopoly (Apr 2025 – Feb 2026)**: under BSC's whitelisted PBS, two
  builders (48Club, Blockrazor) produced 87%+ of blocks and captured 90%+ of MEV
  profit; the short block interval collapsed the MEV-contestable window, making
  the chain structurally more censorship-prone than Ethereum
  [cites: arxiv-2602.15395].
- **Stablecoin sanction races (Nov 2017 – Aug 2025, >$1.5B frozen value)**: at
  least 7.3% of sanctioned USDT and 18.7% of sanctioned USDC addresses were drained
  to zero before the freeze took effect, with evasion escalating to direct payments
  to block producers — Sanction-Evasion MEV [cites: arxiv-2603.27739].

## References

- corpus entries (= `derives_from`):
  - `arxiv-2602.15395` — MEV in Binance Builder (BSC whitelisted PBS, builder monopoly)
  - `arxiv-2605.04471` — Order Flow Exclusivity & Ethereum Builder Centralization
  - `arxiv-2602.04007` — Boost+: Equitable, Incentive-Compatible Block Building (MEV-Boost centralization, mitigation)
  - `arxiv-2603.07716` — SoK: Evolution of MEV, Miners → Cross-Chain (PBS/MEV-Boost in Era II)
  - `arxiv-2603.26290` — PEB Separation and State Migration (role decoupling, attribution)
  - `arxiv-2603.27739` — Ordering Power is Sanctioning Power (SE-MEV, censorship)
  - `arxiv-2601.20783` — The Monotone Priority System (contract-specific sequencing constraints)
  - `arxiv-2604.21169` — DoS against Multi-Round Transaction Simulation (builder pipeline DoS)
  - `arxiv-2601.19570` — MEV Attacks in Private L2 Mempools (no builder market → probabilistic sandwich)
  - `solodit-zachobront-2023-09-01-obol-3-0` — DVT validator/node-operator trust, MEV & fee redirection
  - `solodit-hexens-2023-10-02-mantle-1-2` — Unverified VersionedSignedBeaconBlock / node-API trust
  - `solodit-hexens-2023-10-02-mantle-1-1` — Missing `execution_optimistic` validation (unfinalized data)
  - `rekt-moneyfornothing` — MEV bot pays 98% bribe to solo validator ($1.3M)
  - `rekt-ripmevbot2` — searcher contract with unprotected swap sandwiched ($2M)
  - `swc-114` — Transaction Order Dependence (application-layer ordering bug PBS monetizes)
