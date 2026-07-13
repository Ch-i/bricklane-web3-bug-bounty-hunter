---
id: synthesis-amm-constant-product-invariant
source: synthesis
source_url: null
title: "AMM Constant Product Invariant (x*y=k): pattern, variants, audit checklist"
ingested_at: 2026-06-04T19:31:02Z
vuln_class:
  - amm-invariant
  - accounting
  - rounding
  - flash-loan
  - oracle-manipulation
  - business-logic
protocol_category:
  - amm
  - dex
  - defi
tags:
  - synthesis
  - constant-product
  - xyk
  - uniswap-v2
  - amm
derives_from:
  - solodit-cyfrin-2023-06-16-beanstalk-wells-0-2
  - solodit-cyfrin-2023-06-16-beanstalk-wells-0-0
  - solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-1-12
  - solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-1-4
  - solodit-cyfrin-2025-10-01-cyfrin-sorella-l2-angstrom-v2-1-2-2
  - solodit-cyfrin-2023-11-10-cyfrin-dexe-3-1
  - solodit-cyfrin-2025-06-10-cyfrin-bunni-v2-1-1-11
  - solodit-cyfrin-2025-06-10-cyfrin-bunni-v2-1-1-13
  - solodit-recon-audits-2025-03-22-apollon-report-2-9
  - rekt-uranium-rekt
  - rekt-value-rekt3
  - rekt-burgerswap-rekt
  - rekt-newgold-protocol-rekt
  - arxiv-2602.00101
---

# AMM Constant Product Invariant (x*y=k)

## Pattern

Constant-product automated market makers (Uniswap-v2 and its thousands of
forks) price swaps by holding the product of the two pool reserves
constant: `x * y = k`. A swap that adds `Δx` of token X must remove enough
`Δy` of token Y that the product after the swap is at least as large as
before, *net of the trading fee*. In Uniswap v2 this is enforced at the end
of `swap()` by recomputing balances, subtracting the fee, and requiring
that the new (fee-adjusted) product is `>= k` — i.e. `k` is allowed to grow
(fees accrue to LPs) but is *never allowed to decrease*. The arxiv
formalization of fee-adjusted constant-product models makes this precise:
swaps preserve the product up to a trading fee `φ ∈ (0,1]`, and key
properties such as output-boundedness and monotonicity hold only when the
fee math is implemented correctly [arxiv-2602.00101].

The bug class is any code path where the implemented invariant check no
longer faithfully encodes "k must not decrease" — or where the reserves
used to evaluate it can be manipulated. Because the entire solvency of the
pool rests on this one inequality, an error here is almost always
high/critical: an attacker who can make the check pass while extracting
more value than they put in can drain the pool in a single transaction.
The Uranium Finance fork demonstrates the extreme case: a copy-paste error
that changed a `1000` constant to `10000` in two of three places left the
fee-adjusted `k` check satisfiable while swapping 1 wei in for ~98% of the
output reserve — $57.2M gone [rekt-uranium-rekt].

Three things make this class especially dangerous in forks and novel AMM
designs. First, the invariant is often re-derived or generalized (weighted
pools, virtual reserves, concentrated liquidity, vault-backed reserves),
and the generalization quietly breaks an assumption the original code
relied on [solodit-cyfrin-2023-06-16-beanstalk-wells-0-2,
rekt-value-rekt3]. Second, integer rounding in the reserve update can erode
`k` a little on every trade, which is both a slow value leak and, in
virtual-reserve designs, a path to `k → 0` and permanent DoS
[solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-1-12,
solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-1-4].
Third, the *spot* reserves that define the price (`y/x`) are trivially
movable with a flash loan, so any contract that reads pool reserves for
pricing, fee selection, or accounting inherits a manipulation surface even
when the swap math itself is correct [solodit-cyfrin-2023-11-10-cyfrin-dexe-3-1,
rekt-newgold-protocol-rekt, solodit-recon-audits-2025-03-22-apollon-report-2-9].

## Variants

### V1: Broken/weakened invariant check in the swap path (fork math errors)

The most direct variant: the on-chain check that should enforce
`k_after >= k_before` is implemented incorrectly, so a swap that should
revert succeeds. Uranium Finance changed the fee-denominator constant
`1000 → 10000` in two of three places in a Uniswap-v2 fork; the resulting
balance-adjustment math let the `x*y=k` check pass while draining both
reserves via the low-level `swap()` [rekt-uranium-rekt]. BurgerSwap's loss
came from a closely related fork mistake: a missing guard allowed a second
swap (reentrancy / double-swap through a self-created fake-token pair) to be
executed before reserves were reconciled, so the invariant was evaluated
against stale balances [rekt-burgerswap-rekt]. The audit-side analogue is
any divergence from canonical Uniswap rounding/fee handling that an auditor
must diff line-by-line against the reference implementation.

### V2: Generalized invariant that breaks the implicit constant-product assumptions

When a protocol abstracts the swap curve behind a pluggable "well
function" or a weighted/exponential formula, code written for the linear
constant-product case silently becomes wrong for other curves. In Beanstalk
Wells, `removeLiquidity`/`getRemoveLiquidityOut` assume *linearity*
(`Δx = (l/L)·x`), which holds for `ConstantProduct2` (`L² = 4xy`) but
breaks for non-linear (e.g. quadratic / Numoen-style) well functions,
breaking the well invariant on withdrawal and causing LP loss
[solodit-cyfrin-2023-06-16-beanstalk-wells-0-2]. A related Wells finding is
that the invariant `totalSupply() == calcLpTokenSupply(reserves)` can be
broken by valid transactions, leading to reverts on legitimate liquidity
removal (insolvency-style DoS) [solodit-cyfrin-2023-06-16-beanstalk-wells-0-0].
Value DeFi's vSwap is the catastrophic version: their weighted constant
product used Bancor's `power()` routine, which assumes `baseN >= baseD`; a
crafted swap on any non-50/50 pool violated that assumption, so the
weighted-invariant enforcement passed while the pool was drained — $11M
[rekt-value-rekt3].

### V3: Rounding direction erodes k (value leak and DoS)

Even with the correct formula, integer division must round *in the
protocol's favor* so that `k` never decreases. Rounding the new reserve
down on each trade lets users receive slightly more output than correct and
causes `k` to decay over time; best practice is the Uniswap-v2 invariant
that `k` never decreases (round up via `Math.ceilDiv`)
[solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-1-12].
In a virtual-reserve AMM this rounding erosion compounds: each trade can
lose up to `denominator-1` from `k`, and once `k` is small a single trade
can round a reserve to zero, after which every trade reverts at the
`initialized`/`reserve > 0` guard — a permanent DoS until an admin resets
the baseline
[solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-1-4].
Rounding-direction *inconsistency* with Uniswap is itself a finding: in
Angstrom's `CompensationPriceFinder`, amount deltas always rounded down
instead of choosing direction by exact-in vs exact-out, diverging from
`SwapMath::computeSwapStep` and mispricing the effective swap
[solodit-cyfrin-2025-10-01-cyfrin-sorella-l2-angstrom-v2-1-2-2].

### V4: Fee accounting that desynchronizes reserves from the invariant

The invariant only stays sound if every value that leaves the pool is
charged for. Two failure modes appear: fees that can exceed 100% and fees
that are silently *not* charged. In Bunni v2, when an am-AMM manager is
active the swap fee and hook fee are computed separately on the full amount,
so the combined fee can exceed 100% (`SWAP_FEE_BASE`), causing reverts or
overcharging [solodit-cyfrin-2025-06-10-cyfrin-bunni-v2-1-1-11]. Conversely,
`BunniHook::beforeSwap` moves tokens to/from fee-charging ERC4626 vaults
without charging the swap for the vault fee, silently decreasing the pool
balances that proportionally belong to LPs — a slow leak relative to the
intended invariant [solodit-cyfrin-2025-06-10-cyfrin-bunni-v2-1-1-13].

### V5: Spot-reserve-derived prices/fees are flash-loan manipulable

The ratio `y/x` of current reserves is the pool's instantaneous price, and
it is movable within a single transaction with a flash loan. Any consumer
that reads reserves for pricing or logic inherits this. DeXe's `PriceFeed`
priced assets through `UniswapV2Router::getAmountsOut()/getAmountsIn()`,
which are pure functions of pool reserves, allowing the returned price to be
manipulated via flash loans (mitigation: TWAP or Chainlink)
[solodit-cyfrin-2023-11-10-cyfrin-dexe-3-1]. Apollon's `SwapPair` computes a
*dynamic swap fee* from the pre- and post-swap spot ratio; because the fee
keys off manipulable spot reserves with no deviation threshold, a holder of
most of the LP can donate to reserves to make the fee non-deterministic and
make others lose funds [solodit-recon-audits-2025-03-22-apollon-report-2-9].
New Gold Protocol combined a flash loan to move PancakeSwap pool reserves
with a broken fee/transfer mechanism that "synced the pool into oblivion"
after sending tokens to the dead address — ~$2M
[rekt-newgold-protocol-rekt]. The arxiv result that a single large swap is
strictly more profitable than splitting it under fees is the economic
backdrop to why atomic, flash-funded reserve moves are so effective
[arxiv-2602.00101].

## Audit checklist

- Does the swap path explicitly enforce that the fee-adjusted product of
  reserves after the swap is `>= k` before the swap (i.e. `k` never
  decreases), matching Uniswap v2's end-of-`swap()` check?
- For Uniswap-v2 forks, do the fee constants (`1000`/`997`, `getAmountOut`
  numerator/denominator) match the reference *in every place*, with no
  `1000→10000`-style copy edits? [rekt-uranium-rekt]
- Can `swap()` be re-entered or a second swap be performed before reserves
  are reconciled/synced, so the invariant is checked against stale balances?
  [rekt-burgerswap-rekt]
- If the curve is generalized (weighted, quadratic, pluggable well
  function), does liquidity add/remove math still preserve the *actual*
  invariant, rather than assuming linearity of the constant-product case?
  [solodit-cyfrin-2023-06-16-beanstalk-wells-0-2]
- Is the LP-supply invariant (`totalSupply == calcLpTokenSupply(reserves)`)
  maintained across all add/remove/transfer paths, and tested with fuzz/
  invariant tests? [solodit-cyfrin-2023-06-16-beanstalk-wells-0-0]
- Do underlying math primitives have documented domain assumptions (e.g.
  `power()` requires `baseN >= baseD`), and is every call site guaranteed to
  satisfy them for attacker-controlled inputs? [rekt-value-rekt3]
- Does every reserve update round in the protocol's favor (round up on
  reserves that must not shrink), e.g. via `Math.ceilDiv`, so integer
  truncation cannot erode `k`?
  [solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-1-12]
- For virtual-reserve / synthetic-`k` designs, is there a minimum-reserve
  floor preventing reserves from rounding to zero and bricking trading?
  [solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-1-4]
- Are rounding directions chosen by swap context (exact-in vs exact-out) and
  consistent with Uniswap's `SwapMath::computeSwapStep`, rather than always
  rounding the same way?
  [solodit-cyfrin-2025-10-01-cyfrin-sorella-l2-angstrom-v2-1-2-2]
- Can the total fee charged on a swap exceed 100% (`SWAP_FEE_BASE`) when
  multiple fee components are summed independently?
  [solodit-cyfrin-2025-06-10-cyfrin-bunni-v2-1-1-11]
- When reserves are routed through external/vault layers that charge fees,
  is that cost charged to the swap rather than silently deducted from LP-
  owned balances? [solodit-cyfrin-2025-06-10-cyfrin-bunni-v2-1-1-13]
- Does any pricing/fee/accounting logic read *spot* reserves
  (`getAmountsOut`, `getReserves`, `slot0`) that a flash loan can move
  within one transaction? If so, is it replaced/guarded by a TWAP, oracle,
  or deviation threshold? [solodit-cyfrin-2023-11-10-cyfrin-dexe-3-1,
  solodit-recon-audits-2025-03-22-apollon-report-2-9]
- Can a direct token transfer / donation to the pair (`balanceOf` vs cached
  `reserve`) be used to skew the invariant, fees, or `sync`-based logic?
  [solodit-recon-audits-2025-03-22-apollon-report-2-9,
  rekt-newgold-protocol-rekt]

## Prior incidents

- **Uranium Finance (2021-04-28) — $57.2M**: Uniswap-v2 fork changed a
  `1000` fee constant to `10000` in two of three places, breaking the
  fee-adjusted `x*y=k` check so 1 wei of input could swap for ~98% of the
  output reserve via `swap()` [cites: rekt-uranium-rekt].
- **Value DeFi vSwap (2021-05-07) — $11M**: weighted constant-product pools
  used Bancor's `power()`, which assumes `baseN >= baseD`; a crafted swap on
  non-50/50 pools violated the assumption and passed the weighted-invariant
  enforcement while draining funds [cites: rekt-value-rekt3].
- **BurgerSwap (2021-05-28) — $7.2M**: flash-swap plus a self-created
  fake-token pair allowed a reentrant/double swap before reserves were
  reconciled, defeating the invariant check [cites: rekt-burgerswap-rekt].
- **New Gold Protocol (2025-09-17) — ~$2M**: flash loan to manipulate
  PancakeSwap pool reserves combined with a broken fee/transfer mechanism
  that "synced the pool into oblivion" after a dead-address transfer
  [cites: rekt-newgold-protocol-rekt].

## References

- solodit-cyfrin-2023-06-16-beanstalk-wells-0-2 — `removeLiquidity`
  linearity assumption breaks the invariant for non-constant-product well
  functions (High).
- solodit-cyfrin-2023-06-16-beanstalk-wells-0-0 — `totalSupply ==
  calcLpTokenSupply(reserves)` invariant can be broken by valid txs (High).
- solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-1-12 —
  rounding down lets `k` decrease; `k` should never decrease, round in
  protocol favor (Low).
- solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-1-4 —
  virtual-reserve rounding erosion drives `k → 0` and permanent trade DoS
  (Low).
- solodit-cyfrin-2025-10-01-cyfrin-sorella-l2-angstrom-v2-1-2-2 — amount
  delta rounding directions inconsistent with Uniswap `computeSwapStep`
  (Low).
- solodit-cyfrin-2023-11-10-cyfrin-dexe-3-1 —
  `UniswapV2Router::getAmountsOut()` spot-reserve price manipulable via
  flash loan; use TWAP/Chainlink (Informational).
- solodit-cyfrin-2025-06-10-cyfrin-bunni-v2-1-1-11 — swap fees can exceed
  100% when fee components are summed independently (Medium).
- solodit-cyfrin-2025-06-10-cyfrin-bunni-v2-1-1-13 — vault fees not charged
  on swaps, silently decreasing LP-owned reserves (Medium).
- solodit-recon-audits-2025-03-22-apollon-report-2-9 — dynamic `swapFee`
  derived from manipulable spot ratio with no deviation threshold; donation
  manipulation (Medium).
- rekt-uranium-rekt — Uniswap-v2 fork fee-constant error broke the `k`
  check; $57.2M (Critical).
- rekt-value-rekt3 — weighted constant product / Bancor `power()`
  assumption violation; $11M (Critical).
- rekt-burgerswap-rekt — reentrant/double-swap before reserve
  reconciliation; $7.2M (Critical).
- rekt-newgold-protocol-rekt — flash-loan reserve manipulation + broken fee
  sync; ~$2M (Critical).
- arxiv-2602.00101 — formal Lean 4 model of fee-adjusted constant-product
  AMMs: `k` preserved up to fee `φ`, output-boundedness/monotonicity
  preserved, single large swap strictly more profitable than splitting.
