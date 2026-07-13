---
id: synthesis-rollup-sequencing-state-proofs
source: synthesis
source_url: null
title: "Rollup Sequencing & State Proofs: pattern, variants, audit checklist"
ingested_at: 2026-06-04T00:00:00+00:00
vuln_class:
  - rollup-sequencing
  - state-proof-verification
  - censorship
  - liveness
  - oracle-manipulation
  - mev
protocol_category:
  - layer2-rollup
  - bridge
  - oracle
tags:
  - synthesis
  - rollup
  - sequencer
  - state-proof
  - validity-proof
  - forced-inclusion
derives_from:
  - solodit-cyfrin-2024-05-24-cyfrin-linea-2-1
  - solodit-cyfrin-2024-05-24-cyfrin-linea-1-0
  - solodit-hexens-2023-02-27-polygonzkevm-0-2
  - solodit-hexens-2023-02-27-polygonzkevm-2-0
  - solodit-hexens-2023-10-16-eigenlayer-0-1
  - solodit-zachobront-2023-11-01-splits-oracle-0-0
  - solodit-cyfrin-2024-04-09-cyfrin-wormhole-evm-cctp-v2-1-0-0
  - solodit-cyfrin-2024-04-11-cyfrin-wormhole-evm-ntt-v2-1-7
  - solodit-cyfrin-2024-07-13-cyfrin-zaros-1-1
  - solodit-zokyo-2023-04-19-umami-1-5
  - solodit-cyfrin-2024-09-27-cyfrin-bima-v2-0-1-6
  - arxiv-2601.19570
  - arxiv-2604.04748
  - arxiv-2602.16338
  - arxiv-2603.07716
---

# Rollup Sequencing & State Proofs

## Pattern

A rollup splits the chain into two roles that L1 normally fuses together:
a **sequencer** that orders and batches L2 transactions and posts them to
L1, and a **proof / settlement layer** that convinces the L1 bridge that a
posted L2 state root is the honest result of executing those batches. The
security of every asset bridged into the rollup rests on two assumptions:
(1) the L1 contract only finalizes a state root that is *actually proven*
(a validity/ZK proof for zk-rollups, or an unchallenged fraud-proof window
for optimistic rollups), and (2) users retain a way to *force* their
transactions in — and ultimately exit — even if the sequencer turns
malicious or goes offline. Bugs in rollup sequencing and state proofs are
the failures of one of these two assumptions.

The most dangerous class is a **broken or bypassable proof system**: if the
L1 finalization path can accept a state root without a real proof, or if a
Merkle/withdrawal proof can be forged because an index or length is left
unbounded, an attacker can write an arbitrary L2 state to L1 and drain the
bridge. This collapses the rollup's trust model down to "trust the
operator," which is precisely what the proof was supposed to remove
(solodit-cyfrin-2024-05-24-cyfrin-linea-2-1,
solodit-hexens-2023-10-16-eigenlayer-0-1).

The second class is **sequencer power abuse** — censorship, forced-batch
weaponization, and liveness failures. A centralized sequencer that can omit
a user's transactions, with no L1 escape hatch, can permanently freeze that
user's funds (solodit-cyfrin-2024-05-24-cyfrin-linea-1-0). Conversely, the
*escape hatch itself* (forced inclusion via the L1 inbox) becomes an attack
surface: forced batches reach the proving ROM directly, so any divergence
between L2 execution and the proof — or any missing bound — can be triggered
permissionlessly by an attacker who forces and then self-sequences a crafted
batch (solodit-hexens-2023-02-27-polygonzkevm-0-2,
solodit-hexens-2023-02-27-polygonzkevm-2-0).

The third class is **downstream protocols that ignore L2 reality**. A DeFi
protocol deployed on a rollup inherits sequencer downtime, forced-inclusion
address aliasing, and probabilistic ordering. Oracles that don't gate on a
sequencer-uptime feed serve stale prices that *look* fresh; access-control
and redemption logic that doesn't account for aliased senders becomes
uncallable exactly when forced inclusion is the only path
(solodit-zachobront-2023-11-01-splits-oracle-0-0,
solodit-cyfrin-2024-04-09-cyfrin-wormhole-evm-cctp-v2-1-0-0).

## Variants

### V1: Proof bypass / trust-door in finalization

The L1 settlement contract has a path that finalizes an L2 state root
*without* verifying a real proof. On Linea this is explicit
(`finalizeBlocksWithoutProof`, which takes no proof and never calls
`_verifyProof`) and subtle (`setVerifierAddress` can point a `_proofType`
at a verifier whose `Verify` simply `return`s `true`, after which
`finalizeBlocksWithProof` always succeeds). Either path lets the operator
add false L2 merkle roots that `claimMessageWithProof` can then use to drain
L1 ETH, reducing the zk-rollup to an optimistic one *without* watchers or
challenges (solodit-cyfrin-2024-05-24-cyfrin-linea-2-1). These are typically
"training wheels" guarded by a Security Council — the audit point is that
they exist and concentrate trust.

### V2: Forgeable state / withdrawal proofs (missing bound checks)

The proof verifier is present but a user-supplied index or length is not
range-checked, so an attacker steers the Merkle traversal off the intended
path. In EigenLayer's `BeaconChainProofs.verifyWithdrawal`, every leaf index
is checked against its tree height *except* `historicalSummaryIndex`. Because
the combined index is built by bit-shifting and OR-ing several user indices
together, an out-of-range value bleeds into adjacent index fields and lets a
forged withdrawal proof verify against the beacon state root — forging a
withdrawal that never happened (solodit-hexens-2023-10-16-eigenlayer-0-1).
Generic lesson: any time a proof concatenates user-controlled indices, each
must be bounded to its subtree height.

### V3: Forced-batch weaponization

Forced inclusion is the censorship escape hatch, but forced batches flow
straight into the proving ROM, so any execution edge case becomes a
permissionless attack. In Polygon zkEVM, an `identity` (0x4) precompile bug
mis-handled context switching so global variables (e.g. `oldStateRoot`)
collided with per-call variables (`txGasLimit`); an attacker who forces a
batch and self-sequences it credits the sequencer address an enormous ETH
balance, then bridges it out (solodit-hexens-2023-02-27-polygonzkevm-0-2).
A sibling finding: the ROM's RLP decoder accepted non-canonical encodings
(short data in long-string form) that the EVM rejects, so a "poison" forced
transaction is provable by the ROM but desyncs every node, halting the chain
and forcing an L1 state rollback (solodit-hexens-2023-02-27-polygonzkevm-2-0).
Both require only the public force-batch path plus a timeout.

### V4: Sequencer censorship with no L1 escape hatch

A centralized sequencer can omit a target's transactions, and if there is no
way to withdraw L2 assets by *initiating an L1 transaction*, those funds are
permanently frozen — a censorship downgrade far below L1, where even OFAC
enforcement was partial (solodit-cyfrin-2024-05-24-cyfrin-linea-1-0). The
mirror-image bug is when an escape hatch *exists* but downstream contracts
break it: rollups alias the sender address for forced L1->L2 messages, so
access-controlled functions and redemptions that compare `msg.sender`
against an un-aliased owner/recipient become uncallable precisely during
sequencer downtime (solodit-cyfrin-2024-04-11-cyfrin-wormhole-evm-ntt-v2-1-7,
solodit-cyfrin-2024-04-09-cyfrin-wormhole-evm-cctp-v2-1-0-0).

### V5: Sequencer-downtime stale oracle data

Price oracles on a rollup must gate on the sequencer-uptime feed. When the
sequencer is down, Chainlink updates stop but the last answer still appears
fresh, and Uniswap V3 TWAPs extrapolate the last observation forward — so an
attacker can transact against the stale price, and on Arbitrum even *force*
such a transaction through the delayed inbox to guarantee inclusion while the
sequencer is down (solodit-zachobront-2023-11-01-splits-oracle-0-0). Multiple
audits flag the missing `L2 Sequencer Uptime` check and the need for a grace
period after the sequencer returns (solodit-cyfrin-2024-07-13-cyfrin-zaros-1-1,
solodit-zokyo-2023-04-19-umami-1-5,
solodit-cyfrin-2024-09-27-cyfrin-bima-v2-0-1-6).

### V6: Ordering, MEV, and proving-latency liveness

Sequencer ordering policy is itself a security parameter. Private L2 mempools
remove guaranteed atomic inclusion, so sandwiching becomes probabilistic
(attackers lean on sequencer ordering, redundant submissions, and priority
fees) rather than deterministic (arxiv-2601.19570), and MEV is increasingly
cross-domain across rollups, bridges and sequencers (arxiv-2603.07716).
Optimistic rollups additionally face cross-layer L1/L2 state-consistency and
fair-ordering gaps that frameworks like RegGuard try to close
(arxiv-2604.04748). On the proving side, delayed proof generation causes
finality lag and direct economic loss for zk-rollups, making prover
throughput/fault-tolerance a liveness property, not just a perf metric
(arxiv-2602.16338).

## Audit checklist

- Is there *any* finalization path that writes an L2 state root to L1 without
  verifying a real proof (e.g. a `finalizeWithoutProof` function, or a
  pausable/owner-settable verifier)? Who controls it, and can a fake verifier
  that returns `true` be installed? (V1)
- Can the verifier/proof-type address be changed by a single privileged role
  without timelock, watcher, or Security-Council quorum? (V1)
- For every Merkle/withdrawal/state proof: is each user-supplied leaf index
  range-checked against its subtree height? Are proof array lengths checked
  before they are consumed? (V2)
- When multiple indices are combined by shifting/OR-ing into one path index,
  is *every* component bounded so it cannot overflow into an adjacent field? (V2)
- Do forced/self-sequenced batches reach the same execution and decoding path
  as normal batches? Are precompiles and RLP/calldata decoders canonical-form
  strict (rejecting non-canonical encodings the EVM rejects)? (V3)
- Can a permissionless forced batch reach a state where the prover accepts a
  transaction that nodes/synchronizers reject, desyncing or halting the chain? (V3)
- Is there an L1-initiated escape hatch that lets users withdraw/transact even
  if the sequencer censors or halts? Is it actually honored by the bridge
  contracts? (V4)
- Do access-control modifiers, redemption, and "caller must be recipient"
  checks account for the rollup's **aliased** sender address for forced
  L1->L2 messages? (V4)
- Does every oracle read check an L2 Sequencer Uptime feed and enforce a grace
  period (e.g. sequencer up for at least the TWAP window / ≥1h) before trusting
  a price? (V5)
- For TWAP oracles: can a stale/extrapolated observation be exploited at the
  old price when the sequencer returns? Is a fallback (e.g. Chainlink) used on L2s? (V5)
- Are critical actions safe under probabilistic ordering / private-mempool
  sequencing, and is proof-generation latency bounded so finality/withdrawals
  can't be indefinitely stalled? (V6)

## Prior incidents

These are documented audit findings (mostly latent / fixed before
exploitation) demonstrating the pattern; severities are the reviewers'.

- **Linea zk-rollup (2024) — Low/operator-trust**: `finalizeBlocksWithoutProof`
  and a settable no-op verifier let the operator finalize false L2 merkle
  roots and drain L1 ETH via `claimMessageWithProof` [cites: solodit-cyfrin-2024-05-24-cyfrin-linea-2-1].
- **Linea zk-rollup (2024) — Medium**: centralized sequencer can censor users
  with no L1 escape hatch, permanently locking L2 ETH [cites: solodit-cyfrin-2024-05-24-cyfrin-linea-1-0].
- **Polygon zkEVM (2023) — Critical**: `identity` precompile CTX collision
  let a forced+self-sequenced batch credit the sequencer arbitrary ETH, then
  bridge it out [cites: solodit-hexens-2023-02-27-polygonzkevm-0-2].
- **Polygon zkEVM (2023) — Low→chain-halt**: non-canonical RLP "poison"
  transaction provable by the ROM but rejected by nodes, desyncing/halting
  the network and forcing an L1 rollback [cites: solodit-hexens-2023-02-27-polygonzkevm-2-0].
- **EigenLayer BeaconChainProofs (2023) — Critical**: missing
  `historicalSummaryIndex` bound let attackers forge beacon-chain withdrawal
  proofs that verify against the state root [cites: solodit-hexens-2023-10-16-eigenlayer-0-1].
- **0xSplits oracle (2023) — High**: Uniswap V3 TWAP unsafe on L2s during
  sequencer downtime (extrapolated stale price, forceable via delayed inbox)
  [cites: solodit-zachobront-2023-11-01-splits-oracle-0-0].
- **Wormhole CCTP / NTT (2024) — Medium**: redemption and access-controlled
  functions become uncallable during sequencer downtime because aliased
  forced-inclusion senders aren't checked [cites: solodit-cyfrin-2024-04-09-cyfrin-wormhole-evm-cctp-v2-1-0-0, solodit-cyfrin-2024-04-11-cyfrin-wormhole-evm-ntt-v2-1-7].
- **Zaros / Umami / Bima oracles (2023–2024) — Medium**: missing L2 Sequencer
  Uptime check serves stale-but-fresh-looking prices [cites: solodit-cyfrin-2024-07-13-cyfrin-zaros-1-1, solodit-zokyo-2023-04-19-umami-1-5, solodit-cyfrin-2024-09-27-cyfrin-bima-v2-0-1-6].

## References

- corpus entries:
  - solodit-cyfrin-2024-05-24-cyfrin-linea-2-1 — Linea can bypass validity proof verification for L2->L1 finalization
  - solodit-cyfrin-2024-05-24-cyfrin-linea-1-0 — Linea sequencer censorship permanently locks L2 ETH
  - solodit-hexens-2023-02-27-polygonzkevm-0-2 — Polygon zkEVM CTX collision credits sequencer arbitrary ETH (forced batch)
  - solodit-hexens-2023-02-27-polygonzkevm-2-0 — Polygon zkEVM RLP-decode discrepancy / poison forced batch halts chain
  - solodit-hexens-2023-10-16-eigenlayer-0-1 — EigenLayer withdrawal proofs forgeable (missing index bound)
  - solodit-zachobront-2023-11-01-splits-oracle-0-0 — UniV3 oracle unsafe on L2s during sequencer downtime
  - solodit-cyfrin-2024-04-09-cyfrin-wormhole-evm-cctp-v2-1-0-0 — Redemptions blocked when L2 sequencers down (aliased sender)
  - solodit-cyfrin-2024-04-11-cyfrin-wormhole-evm-ntt-v2-1-7 — Access-controlled functions uncallable when sequencer down (aliased sender)
  - solodit-cyfrin-2024-07-13-cyfrin-zaros-1-1 — getPrice missing L2 sequencer-down check
  - solodit-zokyo-2023-04-19-umami-1-5 — Unchecked Chainlink L2 sequencer uptime
  - solodit-cyfrin-2024-09-27-cyfrin-bima-v2-0-1-6 — No L2 sequencer-down check in PriceFeed / oracle wrapper
  - arxiv-2601.19570 — MEV attacks in private L2 mempools (sequencer ordering)
  - arxiv-2604.04748 — RegGuard: legitimacy, cross-layer state consistency, fair ordering for optimistic rollups
  - arxiv-2602.16338 — push0: proof-generation orchestration; delayed proofs cause finality lag
  - arxiv-2603.07716 — SoK: MEV evolution to cross-chain across rollups, bridges, sequencers
