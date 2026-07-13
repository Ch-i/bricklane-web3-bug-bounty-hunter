---
id: synthesis-private-mempool-sequencing
source: synthesis
source_url: null
title: "Private Mempool & Sequencing Guarantees: pattern, variants, audit checklist"
ingested_at: 2026-06-04T21:41:01Z
vuln_class:
  - front-running
  - mev
  - transaction-order-dependence
  - sequencing
  - censorship
protocol_category:
  - rollup
  - sequencer
  - stablecoin
  - dex
  - clob
tags:
  - synthesis
  - private-mempool
  - sequencing
  - encrypted-mempool
  - fair-ordering
derives_from:
  - arxiv-2601.19570
  - arxiv-2601.14996
  - arxiv-2601.20783
  - arxiv-2604.04748
  - arxiv-2603.07716
  - arxiv-2602.15395
  - arxiv-2603.27739
  - swc-114
  - solodit-pashov-audit-group-2022-12-01-cadmos-0-2
  - solodit-pashov-audit-group-2023-10-01-ethena-0-0
  - solodit-cyfrin-2026-04-20-cyfrin-metamask-veda-adapter-v2-0-0-0
  - solodit-cyfrin-2026-04-20-cyfrin-metamask-veda-adapter-v2-0-0-1
  - solodit-cyfrin-2026-01-10-cyfrin-boundary-v2-2-0-1
  - solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-2-6
---

# Private Mempool & Sequencing Guarantees

## Pattern

On a public chain the contents of a pending transaction are visible to
anyone running a node *before* it is mined, and whoever controls block
inclusion decides the order in which transactions execute. This is the
root of transaction-order dependence (TOD): "a race condition
vulnerability occurs when code depends on the order of the transactions
submitted to it" (`swc-114`). Because order is for sale — historically
through Priority Gas Auctions and today through private order flow and
direct payments to block producers — any contract whose outcome depends
on which of two competing transactions lands first is exposed
(`arxiv-2603.07716`). The canonical defensive answer is a **private
mempool**: submit the sensitive transaction through a relay
(e.g. Flashbots) so it never appears in the public mempool and cannot be
observed and reordered before inclusion.

The recurring audit finding is that a privileged or value-bearing action
is *front-runnable* and the recommended mitigation is "route it through
a private mempool." This shows up for admin actions that an adversary
wants to dodge — freezing/blacklisting an account before the freeze
lands (`solodit-pashov-audit-group-2022-12-01-cadmos-0-2`,
`solodit-pashov-audit-group-2023-10-01-ethena-0-0`,
`solodit-cyfrin-2026-01-10-cyfrin-boundary-v2-2-0-1`) — and for
permissionless flows where the attacker rewrites caller-supplied
parameters or grief-consumes a single-use object lifted from public
calldata (`solodit-cyfrin-2026-04-20-cyfrin-metamask-veda-adapter-v2-0-0-0`,
`solodit-cyfrin-2026-04-20-cyfrin-metamask-veda-adapter-v2-0-0-1`,
`solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-2-6`).

The critical auditor insight is that **a private mempool is an
operational mitigation, not a protocol guarantee, and it changes the
threat model rather than removing it.** First, it depends on the *caller*
actually using the relay every time, so it cannot protect permissionless
functions that anyone may submit publicly. Second, on rollups the
"private" mempool is the sequencer itself: there is no public mempool to
observe, but there is also no guaranteed atomic inclusion, so adversarial
ordering becomes *probabilistic* — attackers rely on sequencer ordering,
redundant submissions, and priority-fee placement
(`arxiv-2601.19570`). Third, concentrating order flow in a few trusted
sequencers/builders re-introduces censorship and fairness risk at the
infrastructure layer (`arxiv-2602.15395`, `arxiv-2603.27739`).

Stronger guarantees require protocol-level mechanisms: encrypted/
threshold mempools that hide content until ordering is fixed, batch
**fair-ordering** services, or contract-specified sequencing constraints
(`arxiv-2604.04748`, `arxiv-2601.20783`). But these have real limits —
batch-order fair-ordering can only give strong fairness for a narrow
subset of transactions in practice (`arxiv-2601.14996`) — so an auditor
should treat any "we use a private/fair mempool" assumption as a claim to
be checked, not a fact.

## Variants

### V1: Front-running a privileged "freeze/blacklist" action

A privileged role action (freeze, blacklist, restrict, force-transfer) is
broadcast publicly; the target monitors the mempool and front-runs it by
moving assets to a fresh, unrestricted address before the restriction
lands. The restriction then applies to an empty address. Seen across
`solodit-pashov-audit-group-2022-12-01-cadmos-0-2` (`freezeAccount`,
`whitelistAccount`, `forceTransfer`),
`solodit-pashov-audit-group-2023-10-01-ethena-0-0`
(`FULL_RESTRICTED_STAKER_ROLE` / `addToBlacklist`), and
`solodit-cyfrin-2026-01-10-cyfrin-boundary-v2-2-0-1` (`setRestrictedStatus`
to `FULL`, where restriction is per-address and not "sticky" to shares).
Recommended fix: route admin transactions through a private mempool
(Ethena fixed by always submitting through Flashbots), or redesign so the
action is not front-runnable / so restriction binds to the shares.

### V2: Parameter override on permissionless calls

A function is callable by anyone and trusts caller-supplied parameters
(output token, `minimumMint`, `minimumAssets`, slippage). The signed/
authorized portion does not cover these fields, so a front-runner reads
the pending calldata and resubmits with altered parameters, bypassing
slippage protection or forcing an unintended denomination
(`solodit-cyfrin-2026-04-20-cyfrin-metamask-veda-adapter-v2-0-0-0`).
A private mempool "significantly mitigates" this, but because the
function is permissionless the real fix is to bind safety parameters into
the signed/authorized data so they cannot be rewritten.

### V3: Grief-consuming single-use objects from public calldata

Public batch execution processes streams sequentially and reverts the
whole batch if any one fails. An attacker extracts a single delegation
chain (or order) from the pending batch in the public mempool and
front-runs it with a cheap single call, pre-consuming the single-use
delegation so the victim's batch reverts after spending gas
(`solodit-cyfrin-2026-04-20-cyfrin-metamask-veda-adapter-v2-0-0-1`). The
same shape appears in CLOB settlement: orders are off-chain signatures
with no on-chain escrow, so a trader sees the operator's match tx and
front-runs it with a transfer that moves the required collateral, causing
the settlement to revert after burning gas
(`solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-2-6`). Mitigation is
private orderflow for submission *plus* per-stream isolation / on-chain
locking so one griefable item cannot revert the whole batch.

### V4: Probabilistic MEV under rollup "private" mempools

On rollups there is no public mempool, but also no builder market and no
guaranteed atomic inclusion. Sandwiching therefore depends on sequencer
ordering, redundant submission, and priority-fee placement, making it
probabilistic rather than deterministic. Measurement shows naive
heuristics overstate sandwich activity: most flagged patterns are false
positives and median net return is negative, so sandwiching is rare and
largely unprofitable on rollups with private mempools — though this is a
property of the current sequencing policy, not a guarantee
(`arxiv-2601.19570`).

### V5: Centralized sequencer/builder — censorship and fairness erosion

Bypassing the public mempool via whitelisted PBS / private order flow
concentrates power: on BSC two builders produced 87%+ of blocks and
captured ~90%+ of MEV, and short block intervals collapse the contestable
window, amplifying latency advantage and making the system structurally
more vulnerable to censorship and fairness erosion (`arxiv-2602.15395`).
Relatedly, ordering power *is* enforcement power: a stablecoin freeze is
just another transaction racing the sanctioned party's transfer for
priority, so block producers — not the issuer — decide the outcome and
extract "Sanction-Evasion MEV" (`arxiv-2603.27739`). Private/centralized
order flow shifts trust to whoever sequences.

### V6: Fair-ordering / encrypted-mempool guarantees that don't fully hold

Protocol-level defenses exist but are bounded. Cryptographically
verifiable fair-ordering services can ensure sequencing fairness with
negligible violation probability and prevent detectable ordering
manipulation (`arxiv-2604.04748`). Contract-specific sequencing lets
developers attach monotone integer priorities to calls, and builders
simply sequence high-to-low priority (`arxiv-2601.20783`). But mempool
auditing / batch-order fair-ordering analysis shows these schemes give
strong fairness only for a limited subset of transactions in real
deployments — and naive mempool auditing can mis-accuse honest miners
with >25% probability unless transactions are consistently observed and
spaced (≈30s apart) (`arxiv-2601.14996`).

## Audit checklist

- Does any function's outcome depend on the order in which competing
  transactions land (classic TOD / race condition)? (`swc-114`)
- Can a privileged freeze/blacklist/restrict action be observed in the
  public mempool and front-run by the target moving assets to a fresh
  address before it lands? (`solodit-pashov-audit-group-2022-12-01-cadmos-0-2`,
  `solodit-pashov-audit-group-2023-10-01-ethena-0-0`)
- Is the restriction "sticky" to the shares/assets, or only to an
  address that can be emptied before the restriction applies?
  (`solodit-cyfrin-2026-01-10-cyfrin-boundary-v2-2-0-1`)
- Does the design merely *recommend* a private mempool, or does it
  actually enforce private submission for every sensitive path? (an
  operational mitigation cannot protect permissionless functions)
  (`solodit-cyfrin-2026-04-20-cyfrin-metamask-veda-adapter-v2-0-0-0`)
- Are safety-critical parameters (output token, min-out, slippage,
  deadline) covered by the signed/authorized payload, or are they
  caller-supplied and thus rewritable by a front-runner?
  (`solodit-cyfrin-2026-04-20-cyfrin-metamask-veda-adapter-v2-0-0-0`)
- Can a single-use object (delegation, signed order, nonce) be extracted
  from public calldata and pre-consumed to grief a batch or settlement?
  Is each stream isolated so one failure can't revert the whole batch?
  (`solodit-cyfrin-2026-04-20-cyfrin-metamask-veda-adapter-v2-0-0-1`,
  `solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-2-6`)
- Are off-chain orders backed by on-chain escrow/locking, or can a
  trader withdraw collateral after validation to force a costly revert?
  (`solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-2-6`)
- On a rollup, does the security argument rely on the sequencer's private
  mempool? Is inclusion atomic/guaranteed, or only probabilistic via
  sequencer ordering and priority fees? (`arxiv-2601.19570`)
- Does routing through a private mempool / whitelisted builder set
  introduce a censorship or single-sequencer-trust risk the protocol must
  document? (`arxiv-2602.15395`, `arxiv-2603.27739`)
- For a freeze/sanction-style control, can the controlled transaction be
  out-raced for priority by the party it targets (ordering-layer vs
  contract-layer authority gap)? (`arxiv-2603.27739`)
- If the protocol claims fair-ordering or an encrypted/threshold mempool,
  is the fairness guarantee scoped to all transactions or only a limited
  subset, and what is its violation probability? (`arxiv-2601.14996`,
  `arxiv-2604.04748`, `arxiv-2601.20783`)

## Prior incidents

- **Ethena `StakedUSDe` blacklist evasion (audit, 2023-10) — no on-chain loss**:
  `FULL_RESTRICTED_STAKER_ROLE` blacklisting could be front-run by moving
  `stUSDe` to a new address before `addToBlacklist` lands; remediated by
  always submitting admin transactions through Flashbots (private mempool)
  [cites: `solodit-pashov-audit-group-2023-10-01-ethena-0-0`].
- **Cadmos InvestmentPool admin actions (audit, 2022-12) — Medium**:
  `freezeAccount` / `whitelistAccount` / `forceTransfer` were front-runnable
  from the public mempool; fix is private-mempool submission or non-front-
  runnable redesign [cites: `solodit-pashov-audit-group-2022-12-01-cadmos-0-2`].
- **Boundary `sUSBD` FULL restriction bypass (audit, 2026-01) — Low**:
  per-address (non-sticky) restriction front-run by transferring shares to
  a fresh address before `setRestrictedStatus(.., FULL)`
  [cites: `solodit-cyfrin-2026-01-10-cyfrin-boundary-v2-2-0-1`].
- **MetaMask VedaAdapter parameter/grief front-running (audit, 2026-04) — Low**:
  permissionless delegation calls let a front-runner rewrite output token /
  slippage or pre-consume a single-use delegation to revert a public batch
  [cites: `solodit-cyfrin-2026-04-20-cyfrin-metamask-veda-adapter-v2-0-0-0`,
  `solodit-cyfrin-2026-04-20-cyfrin-metamask-veda-adapter-v2-0-0-1`].
- **BSC builder centralization (measurement, Apr 2025–Feb 2026)**: two
  whitelisted builders produced 87%+ of blocks and captured ~90%+ of MEV
  under private order flow / leaner PBS, eroding censorship resistance and
  fairness [cites: `arxiv-2602.15395`].
- **Stablecoin Sanction-Evasion MEV (measurement, 2017–2025) — >$1.5B frozen value**:
  at least 7.3% of sanctioned USDT and 18.7% of sanctioned USDC addresses
  were drained to zero before the freeze took effect, because the freeze is
  an ordinary transaction racing the transfer for priority
  [cites: `arxiv-2603.27739`].

## References

- `arxiv-2601.19570` — How to Serve Your Sandwich? MEV Attacks in Private L2 Mempools (probabilistic ordering under rollup private mempools)
- `arxiv-2601.14996` — On the Effectiveness of Mempool-based Transaction Auditing (limits of batch fair-ordering / mempool auditing)
- `arxiv-2601.20783` — The Monotone Priority System: Foundations of Contract-Specific Sequencing
- `arxiv-2604.04748` — RegGuard: Legitimacy and Fairness Enforcement for Optimistic Rollups (verifiable fair-ordering service)
- `arxiv-2603.07716` — SoK: The Evolution of Maximal Extractable Value, From Miners to Cross-Chain
- `arxiv-2602.15395` — MEV in Binance Builder (private order flow, builder centralization)
- `arxiv-2603.27739` — Ordering Power is Sanctioning Power: Sanction Evasion-MEV
- `swc-114` — Transaction Order Dependence (TOD / race conditions)
- `solodit-pashov-audit-group-2022-12-01-cadmos-0-2` — Front-running risk in key admin actions
- `solodit-pashov-audit-group-2023-10-01-ethena-0-0` — Evading FULL_RESTRICTED_STAKER_ROLE; fixed via Flashbots
- `solodit-cyfrin-2026-04-20-cyfrin-metamask-veda-adapter-v2-0-0-0` — Front-runner overrides withdrawal token/slippage params
- `solodit-cyfrin-2026-04-20-cyfrin-metamask-veda-adapter-v2-0-0-1` — Public batch griefable via pre-consumed delegation
- `solodit-cyfrin-2026-01-10-cyfrin-boundary-v2-2-0-1` — FULL restriction bypass via share transfer front-run
- `solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-2-6` — Trader front-runs operator to cause settlement reverts
