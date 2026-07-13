---
id: synthesis-concentrated-liquidity-math
source: synthesis
source_url: null
title: "Concentrated Liquidity (Uniswap V3/V4) Math: pattern, variants, audit checklist"
ingested_at: 2026-06-04T21:00:00Z
vuln_class:
  - rounding
  - accounting
  - oracle-manipulation
  - slippage
  - dos
  - mev
  - flash-loan
protocol_category:
  - amm
  - dex
  - concentrated-liquidity-manager
  - vault
tags:
  - synthesis
  - concentrated-liquidity
  - uniswap-v3
  - uniswap-v4
  - tick-math
  - fee-growth
derives_from:
  - solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-2-0
  - solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-1-2
  - solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-1-1
  - solodit-trust-security-2023-05-29-stella-0-6
  - solodit-trust-security-2023-05-29-stella-1-5
  - solodit-cyfrin-2025-10-01-cyfrin-sorella-l2-angstrom-v2-1-0-0
  - solodit-cyfrin-2025-10-01-cyfrin-sorella-l2-angstrom-v2-1-3-7
  - solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-2-4
  - solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-2-3
  - solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-3-0
  - solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-1-0
  - solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-2-3
  - solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-3-1
  - solodit-cyfrin-2025-06-10-cyfrin-bunni-v2-1-1-3
  - solodit-cyfrin-2025-07-15-cyfrin-vii-v2-0-0-1
  - solodit-cyfrin-2023-06-07-cyfrin-uniswap-v3-limit-orders-0-0
  - solodit-cyfrin-2024-01-10-cyfrin-thermae-0-0
  - rekt-moneyfornothing
---

# Concentrated Liquidity (Uniswap V3/V4) Math

## Pattern

Uniswap V3 (and V4) replace the V2 constant-product curve with *concentrated
liquidity*: each LP position supplies liquidity `L` over a bounded price range
`[tickLower, tickUpper)` rather than over `(0, ∞)`. Three primitives recur in
every integration and are where almost all bugs live:

1. **Ticks and `tickSpacing`.** Price is indexed logarithmically:
   `tick = log_{√1.0001}(price ratio)`, where the ratio is `token1/token0`.
   Positions may only start/end on ticks that are exact multiples of the pool's
   `tickSpacing`, and ticks are bounded by `MIN_TICK = -887272` /
   `MAX_TICK = 887272` (the usable bounds shrink with tick spacing). The pool
   stores price as `sqrtPriceX96`, a `Q64.96` fixed-point square root of the
   price ratio [solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-2-0].

2. **Amount/liquidity conversion.** `LiquidityAmounts.getAmountsForLiquidity`
   (and its inverse `getLiquidityForAmounts`) is a three-branch function of where
   the current `sqrtPriceX96` sits relative to the range: below the range the
   position is 100% token0, inside it is a mix, above it is 100% token1
   [solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-1-0]. At every
   initialized tick the pool stores a signed `liquidityNet` delta that is added
   (or subtracted) to active liquidity when the price crosses that tick
   [solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-1-2].

3. **Fee / reward growth accounting.** Fees are not pushed to the LP; the pool
   tracks per-unit-liquidity accumulators (`feeGrowthGlobal`,
   `feeGrowthOutside` at each tick) and derives
   `feeGrowthInside = global − below − above`. These subtractions are *designed
   to underflow/overflow* and must run in `unchecked` arithmetic. Earned fees
   accrue into a separate `tokensOwed0/1` balance distinct from the position's
   principal [solodit-trust-security-2023-05-29-stella-1-5,
   solodit-cyfrin-2025-07-15-cyfrin-vii-v2-0-0-1].

The bug class is therefore **any integrator re-implementing or reading these
primitives incorrectly**: mishandling signed integers, getting an off-by-one at a
range boundary, breaking the wrap-around fee-growth invariant, using
non-standard or unvalidated tick bounds, reusing a stale tick, reading
aggregated rather than per-position state, or trusting the instantaneous
`slot0` price. Because liquidity and rewards are denominated *per unit of
liquidity*, a small math error often scales into full theft of fees/rewards or a
pool-wide DoS, and attackers routinely amplify it with just-in-time (JIT)
liquidity and flash loans.

## Variants

### V1: Signed-integer tick rounding (truncation toward zero)

Computing the enclosing tick range with `tick / spacing * spacing` is only
correct for negative ticks or exact multiples. Solidity integer division
truncates *toward zero*, not toward negative infinity, so for a positive
non-multiple tick the computed `upperTick`/`lowerTick` land one spacing *below*
the true range, sending later loops or branch selection astray. The fix is to
account for the sign of the tick when rounding
[solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-2-0].

### V2: Unsafe signed→unsigned cast of `liquidityNet` at crossings

When walking ticks manually, `liquidityNet` is `int128` and can be negative
(less active liquidity in the next range). Casting it with `uint128(_liquidityNet)`
without checking the sign turns a negative delta, via two's complement, into a
huge positive number that silently inflates active liquidity — accidentally, or
deliberately via JIT liquidity, to redeem/withdraw far more than intended. Use
`LiquidityMath.addDelta` (Uniswap's own library) instead of a raw cast
[solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-1-2].

### V3: Off-by-one when the current tick sits exactly on a range boundary

When the current tick equals the upper bound of a range and is an exact multiple
of tick spacing, Uniswap considers that range's liquidity *inactive*
(`[t0, t1)` is half-open). Custom tick iterators that seed from `currentTick − 1`
skip the boundary tick's `liquidityNet`, causing either an arithmetic underflow
that reverts swaps, or — worse — a smaller-than-real `liquidity` denominator in a
reward-growth-per-unit-liquidity calculation. In Sorella's Angstrom L2 an
attacker could swap the price onto a boundary tick, JIT-add liquidity to
`[t1−s, t1)`, and steal *all* accumulated pool rewards because the growth delta
was divided by `L` instead of `L + L'`. The fix decrements the boundary tick's
net liquidity *before* other calculations / seeds inclusively
[solodit-cyfrin-2025-10-01-cyfrin-sorella-l2-angstrom-v2-1-0-0].

### V4: Broken fee/reward growth accumulator invariants

Two failure modes: (a) re-implementing `feeGrowthInside` math *without* allowing
under/overflow makes the `_computePendingFees` calculation revert in normal
operation — Uniswap wraps these in `unchecked` on the 0.8 branch and integrators
must do the same [solodit-trust-security-2023-05-29-stella-1-5]; and (b)
mis-initializing `feeGrowthOutside`/`rewardGrowthOutside` for a newly initialized
tick. Uniswap's convention: if a tick is just initialized and the current tick is
to its right, seed its outside accumulator with the current global value. An
integrator hook that tries to replicate this *after* liquidity is added (when the
tick is already initialized) never executes the seeding branch, leaving the
accumulator un-initialized [solodit-cyfrin-2025-10-01-cyfrin-sorella-l2-angstrom-v2-1-3-7].

### V5: Reading aggregated pool state instead of per-position state

The canonical `NonfungiblePositionManager` holds the liquidity of *all* of its
users in a given price range under a single pool-level position key. Reading
`liquidity`, `tokensOwed0`, `tokensOwed1` from the *pool* position (by NPM
address + ticks) therefore returns everyone's aggregated liquidity and fees, not
the specific NFT's. Always read per-`tokenId` via `INonfungiblePositionManager.positions(tokenId)`;
otherwise PnL/valuation is grossly inflated, over-paying lenders and draining
borrowers [solodit-trust-security-2023-05-29-stella-0-6].

### V6: Non-standard, unaligned, or unvalidated tick bounds

- **Wrong MIN/MAX constants.** A full-range hook hard-coding `MIN_TICK = -887220`
  (a tick-spacing-60 bound) while the pool's real bound is `±887272` leaves
  *two* regions outside the "full" range. An attacker swaps the fresh pool's
  price into that gap so `getLiquidityForAmounts` returns a tiny liquidity for a
  large deposit — DoS via an unmeetable minimum-liquidity check, or theft of
  value from later LPs [solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-1-0].
- **Unaligned ticks.** Creating a range whose ticks aren't multiples of
  `tickSpacing` later reverts with `TickMisaligned` inside `flipTick`; validate
  alignment at range-creation time [solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-3-1].
- **Post-shift bounds.** Dynamic liquidity distributions that shift a range and
  recompute `tickUpper = tickLower + tickLength` can push `tickUpper` past
  `maxUsableTick`, reverting with `InvalidTick()` and permanently DoS-ing the
  pool; clamp both bounds to `[minUsableTick, maxUsableTick]` after the shift
  [solodit-cyfrin-2025-06-10-cyfrin-bunni-v2-1-1-3].
- **Ignoring MIN/MAX in calm/deviation checks.** A TWAP-vs-spot "calm period"
  guard that computes `twapTick ± deviation` without clamping to `MIN/MAX_TICK`
  reverts even when price has been stable for years, DoS-ing deposit/withdraw/
  harvest [solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-2-3].

### V7: Trusting instantaneous `slot0` price (spot) instead of a TWAP

`pool.slot0()` returns the *instantaneous* `sqrtPriceX96`/tick from current
reserves, which a flash loan or single sandwiching swap can set to an arbitrary
value. Using it to value LP positions, set the deploy range, gate automation
upkeep, or compute on-chain slippage is manipulable; combined with JIT liquidity
it lets an attacker force unfavorable liquidity deployment, trigger redemptions,
or exfiltrate value. Mitigations: use a Uniswap V3 TWAP with a sufficiently long
window (≥900–1800s; note V3 oracles are *not* multi-block-MEV resistant and TWAP
gives weaker protection on some L2 rollups), or pass minimum-out amounts computed
off-chain rather than deriving slippage on-chain
[solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-3-0,
solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-1-1,
solodit-cyfrin-2024-01-10-cyfrin-thermae-0-0].

### V8: Stale tick reuse when redeploying liquidity

Strategies that remove liquidity and immediately redeploy must re-fetch the
current tick (`_setTicks`) *before* `_addLiquidity`. Reusing a stored tick from a
previous interaction can deploy the new position in a range the price has since
left, earning no fees (or leaving it exploitably mispositioned)
[solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-2-4].

### V9: Single-sided liquidity & missing add/remove slippage protection

Because a position's token composition depends on where the price sits relative
to the range, an attacker can front-run an add/remove to push the price out of
range so the LP receives/contributes only one token. Without
`amount0Min`/`amount1Min` parameters (as Uniswap's own `PositionManager.validateMinOut`
provides) the victim silently eats the loss; this is most acute for multi-range
hooks where price moves across ranges freely
[solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-2-3]. The benign-but-costly
version is an LP setting an out-of-range position as a limit order and fat-
fingering the price [rekt-moneyfornothing].

### V10: Fixed-point / `uint128` overflow in amount math

Min-amount or fee math that multiplies `uint128` amounts by an 18-decimal
multiplier (`amount * 0.9999e18 / 1e18`) overflows `uint128` for amounts above
~`341e18`, reverting otherwise-valid orders. Cast to `uint256` before the
multiplication (or scale the multiplier down)
[solodit-cyfrin-2023-06-07-cyfrin-uniswap-v3-limit-orders-0-0].

### V11: Wrong fee-accounting model when wrapping V3 vs V4 positions

V3 keeps earned fees in a separate `tokensOwed` balance collected on demand,
whereas V4's `PoolManager` transfers *all* accrued fees to the caller whenever
liquidity is modified and requires same-tx settlement. A wrapper that proportions
fees among multiple ERC-6909 holders must track owed fees in storage and
*decrement* that state after paying out; failing to decrement (combined with the
ability to fully unwrap via the partial-unwrap path and re-wrap) lets an attacker
reuse stale `tokensOwed` to siphon other holders' fees
[solodit-cyfrin-2025-07-15-cyfrin-vii-v2-0-0-1].

## Audit checklist

- When the code computes a tick range from a price/tick, does it handle
  **negative ticks and positive non-multiples** correctly (no naive
  `tick/spacing*spacing` truncation)? [V1]
- Is `liquidityNet` combined with active liquidity via `LiquidityMath.addDelta`
  rather than a raw `uint128(...)` cast that ignores the sign? [V2]
- Does any custom tick walk/iterator correctly include the **boundary tick's net
  liquidity** when the current tick sits exactly on a range edge (half-open
  `[lower, upper)`)? [V3]
- Are `feeGrowthInside` / `rewardGrowthInside` subtractions wrapped in
  `unchecked` so the intended under/overflow is preserved? [V4]
- Is `feeGrowthOutside` / `rewardGrowthOutside` initialized following Uniswap's
  convention (and at a point where the tick is *not yet* initialized)? [V4]
- Is liquidity/fees read **per `tokenId`** (`positions(tokenId)`) rather than from
  the shared NPM pool position? [V5]
- Do hard-coded `MIN_TICK`/`MAX_TICK` match the pool's true usable bounds for the
  given `tickSpacing` (`±887272`, shrunk by spacing)? [V6]
- Are user-supplied or shifted ticks validated to be **aligned to `tickSpacing`**
  and **clamped to `[minUsableTick, maxUsableTick]`** after any shift? [V6]
- Do TWAP/deviation guards clamp to `MIN/MAX_TICK` so a long-stable price can't
  spuriously revert? [V6]
- Is the price used for valuation/range/upkeep/slippage a **manipulation-resistant
  TWAP (≥900–1800s)** rather than instantaneous `slot0`? [V7]
- Is the current tick **re-fetched immediately before redeploying** liquidity, not
  reused from storage? [V8]
- Do add/remove-liquidity entrypoints expose **`amount0Min`/`amount1Min`** slippage
  parameters, and are removals resistant to front-run single-sided extraction? [V9]
- Are `uint128` amounts **cast to `uint256` before multiplication** in min-amount/
  fee math to avoid overflow on large orders? [V10]
- For V3↔V4 wrappers, is earned-fee state **decremented after payout** (and is the
  V4 immediate-fee-transfer model accounted vs V3's deferred `tokensOwed`)? [V11]
- Can JIT liquidity added and removed within the same block/transaction skew any
  active-liquidity or reward-per-liquidity computation? [V2, V3, V7]

## Prior incidents

- **Uniswap V3 UNI/USDT LP "aavebank.eth" (Dec 2023) — ~$1.3M**: An LP added
  ~$2M USDT *out of range* (an out-of-range V3 position acts as a limit order) but
  fat-fingered the price, effectively offering to buy ~$730k of UNI for $2M; an
  MEV bot back-ran the excess and bribed 98% to a solo validator
  [cites: rekt-moneyfornothing].
- **Stella (Trust Security, May 2023) — audit finding (High/Med)**: PnL inflation
  from reading aggregated NPM pool liquidity/`tokensOwed` instead of per-position,
  plus pending-fee math that reverts because it doesn't allow the V3 fee-growth
  under/overflow [cites: solodit-trust-security-2023-05-29-stella-0-6,
  solodit-trust-security-2023-05-29-stella-1-5].
- **Sorella Angstrom L2 (Cyfrin, Oct 2025) — audit finding (High)**: Boundary-tick
  off-by-one let an attacker JIT-add liquidity and steal *all* pool rewards (or
  revert swaps via liquidity underflow) [cites:
  solodit-cyfrin-2025-10-01-cyfrin-sorella-l2-angstrom-v2-1-0-0,
  solodit-cyfrin-2025-10-01-cyfrin-sorella-l2-angstrom-v2-1-3-7].
- **Paladin Valkyrie hooks (Cyfrin, Mar 2025) — audit finding (High/Med)**:
  Non-standard full-range MIN/MAX ticks allowed pushing price outside the range
  for pool DoS / LP value theft; removals lacked slippage protection
  [cites: solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-1-0,
  solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-2-3].
- **The Standard Auto-Redemption (Cyfrin, Dec 2024) — audit finding (Med/Low)**:
  Signed-tick truncation bug and unchecked signed→unsigned `liquidityNet` cast,
  plus instantaneous-`sqrtPriceX96`/JIT manipulation of redemption sizing
  [cites: solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-2-0,
  solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-1-2,
  solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-1-1].
- **Beefy ConcLiq strategy (Cyfrin, Apr 2024) — audit finding (Info/Low)**:
  `slot0` spot-price reliance, stale-tick redeploy, and a calm-period guard that
  ignores MIN/MAX ticks [cites: solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-3-0,
  solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-2-4,
  solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-2-3].

## References

- solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-2-0 — signed-tick truncation in range calc
- solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-1-2 — unsafe signed→unsigned `liquidityNet` cast
- solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-1-1 — instantaneous `sqrtPriceX96` + JIT manipulation
- solodit-trust-security-2023-05-29-stella-0-6 — aggregated vs per-tokenId NPM position read
- solodit-trust-security-2023-05-29-stella-1-5 — fee-growth must under/overflow (`unchecked`)
- solodit-cyfrin-2025-10-01-cyfrin-sorella-l2-angstrom-v2-1-0-0 — boundary-tick off-by-one, reward theft
- solodit-cyfrin-2025-10-01-cyfrin-sorella-l2-angstrom-v2-1-3-7 — `rewardGrowthOutsideX128` init convention
- solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-2-4 — re-fetch tick before redeploying liquidity
- solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-2-3 — calm-period guard ignores MIN/MAX ticks
- solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-3-0 — `slot0` spot-price manipulation
- solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-1-0 — non-standard MIN/MAX full-range ticks
- solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-2-3 — missing remove-liquidity slippage protection
- solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-3-1 — tick-spacing alignment validation
- solodit-cyfrin-2025-06-10-cyfrin-bunni-v2-1-1-3 — post-shift tick-bound clamping (DoS)
- solodit-cyfrin-2025-07-15-cyfrin-vii-v2-0-0-1 — V3 `tokensOwed` vs V4 immediate fee transfer in wrappers
- solodit-cyfrin-2023-06-07-cyfrin-uniswap-v3-limit-orders-0-0 — `uint128` overflow in min-amount math
- solodit-cyfrin-2024-01-10-cyfrin-thermae-0-0 — on-chain slippage from `slot0` is manipulable; use TWAP/off-chain min-out
- rekt-moneyfornothing — out-of-range V3 LP limit-order fat-finger (~$1.3M)
