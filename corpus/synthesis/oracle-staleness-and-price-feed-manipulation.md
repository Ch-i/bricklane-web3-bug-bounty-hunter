---
id: synthesis-oracle-staleness-and-price-feed-manipulation
source: synthesis
source_url: null
title: "Oracle staleness and price-feed manipulation: pattern, variants, audit checklist"
ingested_at: 2026-05-18T00:00:00Z
vuln_class:
  - oracle-manipulation
  - stale-price
  - sequencer-uptime
  - flash-loan
  - spot-price
protocol_category:
  - lending
  - dex
  - perpetuals
  - vault
  - stablecoin
tags:
  - synthesis
  - oracle
  - chainlink
  - twap
  - l2-sequencer
  - price-feed
  - flash-loan
derives_from:
  - solodit-zokyo-2024-02-27-paribus-1-2
  - solodit-zokyo-2024-02-27-paribus-1-3
  - solodit-zokyo-2024-06-23-copra-1-2
  - solodit-zokyo-2024-06-23-copra-1-0
  - solodit-zokyo-2024-06-23-copra-2-6
  - solodit-zokyo-2024-10-24-beyond-0-0
  - solodit-trust-security-2023-05-29-stella-1-2
  - solodit-cyfrin-2024-09-27-cyfrin-bima-v2-0-1-6
  - solodit-cyfrin-2024-09-27-cyfrin-bima-v2-0-1-7
  - solodit-cyfrin-2025-09-01-cyfrin-licredity-v2-0-2-0
  - solodit-cyfrin-2025-09-01-cyfrin-licredity-v2-0-4-0
  - solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-1-3
  - solodit-cyfrin-2024-02-23-cyfrin-swell-barracuda-1-3
  - solodit-cyfrin-2024-09-13-cyfrin-the-standard-smart-vault-v2-0-1-2
  - solodit-cyfrin-2024-07-13-cyfrin-zaros-1-0
  - solodit-cyfrin-2025-06-02-cyfrin-evo-soulboundtoken-v2-0-0-0
  - solodit-zachobront-2023-11-01-splits-oracle-0-0
  - solodit-zachobront-2023-11-01-splits-oracle-2-0
  - solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-1-1
  - solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-3-0
  - solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-1-0
  - solodit-recon-audits-2025-03-23-quill-finance-report-0-0
  - rekt-venus-blizz-rekt
  - rekt-inverse-finance-rekt
  - rekt-inverse-rekt2
  - rekt-uwulend-rekt
  - rekt-deus-dao-rekt
  - rekt-woo-rekt
  - rekt-makina-rekt
  - rekt-sturdy-rekt
---

# Oracle staleness and price-feed manipulation

## Pattern

DeFi protocols depend on price oracles for nearly every critical
decision — collateral valuation, borrow capacity, liquidation
thresholds, redemption rates, share-price minting, and swap slippage
checks. Two complementary failure modes dominate the corpus: (1) the
oracle keeps returning a value the protocol *believes* is current when
in reality the real market price has moved, and (2) the oracle reports
a value an attacker can deliberately distort within a single
transaction. Both fail in the same direction: the protocol books trades
or liquidations against a price that doesn't reflect reality, and
someone walks off with the difference.

The "staleness" branch covers everything that lets old data look fresh:
no `updatedAt` check at all
([solodit-cyfrin-2025-09-01-cyfrin-licredity-v2-0-2-0],
[solodit-cyfrin-2024-07-13-cyfrin-zaros-1-0],
[solodit-cyfrin-2024-02-23-cyfrin-swell-barracuda-1-3],
[solodit-cyfrin-2025-06-02-cyfrin-evo-soulboundtoken-v2-0-0-0]); a
single hard-coded heartbeat shared across feeds with very different
update cadences
([solodit-zokyo-2024-02-27-paribus-1-2],
[solodit-zokyo-2024-06-23-copra-1-2]); ignoring Chainlink's built-in
`minAnswer/maxAnswer` circuit-breaker so the oracle silently floors at
a stale lower bound
([solodit-zokyo-2024-02-27-paribus-1-3],
[solodit-cyfrin-2024-09-27-cyfrin-bima-v2-0-1-7],
[rekt-venus-blizz-rekt]); and on L2s, failing to check the Chainlink
sequencer uptime feed so prices that physically cannot update appear
to be live
([solodit-trust-security-2023-05-29-stella-1-2],
[solodit-cyfrin-2024-09-27-cyfrin-bima-v2-0-1-6],
[solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-1-3],
[solodit-zachobront-2023-11-01-splits-oracle-0-0]).

The "manipulation" branch covers anything an attacker can move *in the
same transaction* as the read. The classic shape is a flash loan that
shifts a DEX pool's reserves, the protocol queries that pool's spot
price (`slot0`, `getAmountsOut`, `calc_withdraw_one_coin`, `get_dy`,
or a short-window TWAP), then borrows / mints / liquidates against the
distorted price before unwinding the loan in the same tx
([rekt-deus-dao-rekt],
[rekt-inverse-finance-rekt],
[rekt-inverse-rekt2],
[rekt-uwulend-rekt],
[rekt-woo-rekt],
[rekt-makina-rekt],
[solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-1-1],
[solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-3-0]). The Curve
"read-only reentrancy" family is a special case where the
manipulation happens mid-callback on `remove_liquidity`, so even
view-based virtual prices used as oracles get poisoned
([rekt-sturdy-rekt]).

Both branches converge on the same underlying mistake: trusting a
single number derived from a manipulable or potentially-stale source
without independent corroboration, bounds, freshness checks, or a
delay/snapshot mechanism that severs the attacker's ability to write
the price and read it in the same transaction.

## Variants

### V1: Missing or weak staleness check on Chainlink `latestRoundData`

The simplest variant: code calls `priceFeed.latestRoundData()` but
destructures only `answer`, ignoring `updatedAt`, `roundId`, and
`answeredInRound`. Even when a check exists, common errors are using a
single global `STALENESS_THRESHOLD` for feeds whose true heartbeats
differ by orders of magnitude (ETH/USD ≈ 1h vs AMPL/USD ≈ 48h —
[solodit-zokyo-2024-06-23-copra-1-2],
[solodit-zokyo-2024-02-27-paribus-1-2]), or assuming an asset has the
same heartbeat across chains (it doesn't —
[solodit-cyfrin-2024-02-23-cyfrin-swell-barracuda-1-3]). Cyfrin's
canonical fix is
`require(updatedAt >= block.timestamp - MAX_STALENESS)` plus
`require(answeredInRound >= roundId)` with a per-feed configurable
`maxStaleness` ([solodit-cyfrin-2025-09-01-cyfrin-licredity-v2-0-2-0]).
A subtle but reported variant is to write the check as
`updatedAt < block.timestamp - staleAfter`, which can underflow on
exotic chains; rearranging to `updatedAt + staleAfter < block.timestamp`
is the standard fix ([solodit-zachobront-2023-11-01-splits-oracle-2-0]).

### V2: Aggregator `minAnswer` / `maxAnswer` circuit breaker

Chainlink aggregators have built-in floor (`minAnswer`) and ceiling
(`maxAnswer`) bands. If an asset's market price crashes below the
floor, the feed *keeps returning the floor*, not the actual price — and
a vanilla staleness check still passes because `updatedAt` keeps
ticking. The canonical incident is the LUNA collapse: Venus and Blizz
both consumed Chainlink LUNA/USD with `minAnswer` hard-coded at $0.10,
so attackers bought LUNA on the open market for fractions of a cent
and posted it as $0.10 collateral, draining $13.5M and $8.3M
respectively ([rekt-venus-blizz-rekt]). The fix is to read
`minAnswer`/`maxAnswer` from the underlying aggregator and revert if
`answer <= minAnswer || answer >= maxAnswer`
([solodit-zokyo-2024-02-27-paribus-1-3],
[solodit-cyfrin-2024-09-27-cyfrin-bima-v2-0-1-7],
[solodit-cyfrin-2025-06-02-cyfrin-evo-soulboundtoken-v2-0-0-0]).

### V3: Missing L2 sequencer uptime check

On Arbitrum, Optimism, Base, Scroll, etc., when the centralized
sequencer is down, Chainlink feeds simply stop updating. Their
`updatedAt` becomes a frozen snapshot of pre-downtime price — which
*looks* fresh as soon as the sequencer comes back, and L1 forced
transactions can execute against that frozen price while the sequencer
is down. The standard mitigation is the Chainlink sequencer uptime
feed: revert if `answer == 1` (sequencer down) and revert if
`block.timestamp - startedAt <= GRACE_PERIOD_TIME` (typically ~1
hour) after recovery, and additionally `revert if startedAt == 0`
([solodit-trust-security-2023-05-29-stella-1-2],
[solodit-cyfrin-2024-09-27-cyfrin-bima-v2-0-1-6],
[solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-1-3],
[solodit-zokyo-2024-10-24-beyond-0-0],
[solodit-cyfrin-2025-06-02-cyfrin-evo-soulboundtoken-v2-0-0-0]). A
related design tension: in lending protocols, blanket-blocking
*liquidations* during the grace period can trap insolvent positions
and lock in bad debt — some teams choose to allow liquidations while
the sequencer recovers ([solodit-recon-audits-2025-03-23-quill-finance-report-0-0]).
This is the same family of bug for non-Chainlink L2 oracles: a UniV3
TWAP extrapolates the last observation across downtime, so when the
sequencer returns, the TWAP carries a stale price that an L1-forced
transaction can exploit ([solodit-zachobront-2023-11-01-splits-oracle-0-0]).

### V4: DEX spot price used as the protocol's oracle

Reading `slot0.sqrtPriceX96` on UniV3, `getReserves()` /
`getAmountsOut` on UniV2-likes, `calc_withdraw_one_coin` /
`get_dy` / `get_virtual_price` on Curve, or any other function that
reflects current pool balances, exposes a flash-loan attack surface.
Example incidents:

* **Deus DAO** flash-loaned the Solidex USDC/DEI pool to inflate
  collateral value and trigger liquidations
  ([rekt-deus-dao-rekt]).
* **Inverse Finance (2022-04)** swapped 500 ETH into a thin SushiSwap
  INV/WETH pair to inflate INV's price 50× on a SushiSwap TWAP fed by
  Keeper Network, then posted $644k of INV as collateral and borrowed
  $15.6M ([rekt-inverse-finance-rekt]).
* **WooFi sPMM** had a fallback that didn't actually cover the WOO
  token's own price; attacker manipulated WOO via flash loans and
  drained $8.5M from `WooPPV2` ([rekt-woo-rekt]).
* **UwuLend** used Curve pool state as a fallback oracle, allowing
  borrow at $0.99 and liquidate at $1.03 for $19.4M
  ([rekt-uwulend-rekt]).
* **Makina** (2026) had a permissionless `updateTotalAum()` that
  pulled `calc_withdraw_one_coin` from manipulated Curve pools and
  locked the result into share price, draining $4.13M atomically with
  a $280M flash loan from Morpho + Aave V2 ([rekt-makina-rekt]).

In audits this shows up as warnings against `pool.slot0` for any
deposit/withdraw math
([solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-3-0],
[solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-1-1])
and against using `get_dy` to derive a *minOut* slippage threshold
for an `exchange` call in the same tx — a "circular" check that only
protects between two reads of the same manipulated state
([solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-1-0]). The
fix is a price reference *outside* the pool being swapped (Chainlink,
a long TWAP, or an off-chain `minOut` parameter).

### V5: LP-token / virtual-price oracles vulnerable to imbalance or read-only reentrancy

Pricing an LP token by reading the pool's current asset balances is a
direct flash-loanable formula: imbalance the pool, the LP looks
cheaper or more expensive, the protocol mints or accepts collateral
incorrectly. The "fair LP pricing" formula (e.g. Alpha Homora style)
is the standard mitigation. Inverse Finance was hit a second time
because its yvcrv3Crypto oracle "misused the balances of assets in
the pool to directly calculate the LP token price"
([rekt-inverse-rekt2]). Curve's `get_virtual_price` is *almost* a
manipulation-resistant LP price — but the **read-only reentrancy**
class lets an attacker call `remove_liquidity` (which sends ETH/native
via a callback) and re-enter the oracle while pool state is partially
updated, returning a temporarily inflated `virtual_price`. Sturdy
Finance lost ~$800k this way on a Balancer B-stETH-STABLE pool used
as collateral oracle; the same vector previously hit Midas and dForce
([rekt-sturdy-rekt]).

### V6: Short-window or single-source TWAPs

TWAPs are robust only when the window is long enough that moving the
average to a profitable target costs more than the attack yields, and
when the underlying pool is liquid enough that an attacker can't move
the entire averaged window cheaply. Inverse Finance's TWAP was sampled
over a short window on a thinly traded SushiSwap pair —
ChainLinkGod's post-mortem comment: *"Relying upon a TWAP oracle
generated from a single thinly traded DEX trading pair with a short
time sample compounds market manipulation risks"*
([rekt-inverse-finance-rekt]). On UniV3, Cyfrin recommends TWAP
intervals of at least 900-1800 seconds and notes that UniV3 pool
oracles are still not multi-block-MEV-resistant
([solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-1-1]).
On L2s, even a long TWAP is unsafe across sequencer downtime because
Uniswap extrapolates the last observation
([solodit-zachobront-2023-11-01-splits-oracle-0-0]).

### V7: Fallback / multi-oracle logic that defaults to the manipulable source

Several incidents involved a "Chainlink + fallback" design where the
fallback was a DEX-derived price. The fallback either took over too
aggressively or didn't actually cover the asset being attacked. WooFi
explicitly admitted the Chainlink fallback "didn't actually cover the
WOO token price" ([rekt-woo-rekt]); UwuLend's fallback computed prices
from Curve pools that the attacker manipulated
([rekt-uwulend-rekt]). Audit-side, two related issues recur: (a) no
fallback at all, so a stale or revoked primary feed bricks the
protocol or accepts the stale price
([solodit-zokyo-2024-06-23-copra-1-0]); (b) primary `latestRoundData`
not wrapped in try-catch, so Chainlink revoking the consuming address
DOSes every price-dependent function
([solodit-zokyo-2024-06-23-copra-2-6]).

### V8: Oracle update logic / decimal / encoding bugs

Even when staleness, bounds, and sequencer are checked, the protocol
can mishandle the data after the fact. Licredity had a short-circuit
intended to skip redundant updates that compared `sqrtPriceX96`
against `lastPriceX96` (which was stored as `(sqrt^2) >> 96`) — the
condition almost never triggered, defeating the optimisation and in
other shapes could let stale data be accepted as "unchanged"
([solodit-cyfrin-2025-09-01-cyfrin-licredity-v2-0-4-0]). Audits
routinely catch missing decimal normalisation, missing `answer > 0`
checks, missing `roundId != 0` checks, and missing `updatedAt > 0`
("round not complete") guards
([solodit-cyfrin-2024-09-13-cyfrin-the-standard-smart-vault-v2-0-1-2],
[solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-1-3],
[solodit-zokyo-2024-10-24-beyond-0-0]).

## Audit checklist

Use as a YES/NO pass when reviewing any price-feed integration. Each
item maps to a real finding in `derives_from`.

**Freshness / staleness**

- Is `updatedAt` (and ideally `roundId`/`answeredInRound`) read from
  `latestRoundData` and validated against a configurable threshold?
- Is the staleness threshold *per-feed*, not a single global constant
  shared across feeds with different heartbeats?
- For multi-chain deployments, does the threshold account for the same
  feed having different heartbeats on different chains?
- Is the stale-check arithmetic written in a form that cannot
  underflow on chains with non-standard timestamps?
- Is there a sanity check that `updatedAt > 0` (round not complete)
  and `updatedAt <= block.timestamp` (no future timestamps)?
- Is there an off-chain monitoring bot that alerts when the feed
  stops updating, separate from the on-chain revert?

**Aggregator bounds**

- Are `minAnswer` and `maxAnswer` of the underlying aggregator read
  and the result rejected if `answer <= minAnswer || answer >=
  maxAnswer`?
- If `minAnswer/maxAnswer` are *not* read, has the team documented
  why (e.g. using a non-Chainlink oracle without that pattern)?

**L2 sequencer**

- On L2 deployments, is the Chainlink sequencer uptime feed queried
  and the price rejected if `answer == 1` (sequencer down)?
- Is `startedAt == 0` (round not started) handled explicitly?
- Is there a grace period (typically ~1 hour, but ≥ TWAP window if a
  TWAP is in play) after the sequencer recovers before prices are
  consumed?
- If the protocol uses a non-Chainlink on-chain TWAP (UniV3, etc.) on
  L2, does the design account for `getSurroundingObservations`
  extrapolating the last pre-downtime observation?
- If liquidations are blocked during the grace period, has the team
  weighed the bad-debt risk of being unable to liquidate insolvent
  positions?

**Spot / TWAP manipulation resistance**

- Does the protocol ever read `slot0`, `sqrtPriceX96`, reserves,
  `getAmountsOut`, `calc_withdraw_one_coin`, `get_dy`, or
  `get_virtual_price` from a pool whose state can be moved by a
  flash loan within the same transaction?
- If a TWAP is used, is the window long enough (≥ 900s for UniV3 is a
  common floor) and the underlying pool deep enough that moving the
  average is uneconomic?
- Is the `minOut` for an in-tx swap derived from an *independent*
  price source (Chainlink, long TWAP, off-chain user param), not
  from the same pool's `get_dy`/`getAmountsOut`?
- For LP-token pricing, is a manipulation-resistant formula used
  ("fair LP pricing") rather than directly reading pool balances?
- For Curve / Balancer LPs used as oracles, is there reentrancy
  protection covering the `remove_liquidity` callback path, including
  read-only reentrancy on view functions?

**Multi-feed / fallback design**

- If there is a fallback oracle, does it actually cover *every* asset
  the primary covers, or are there assets that silently fall through
  to a DEX-derived price?
- Is the fallback at least as manipulation-resistant as the primary?
- Is `latestRoundData` wrapped in try-catch so that Chainlink
  multisig access revocation does not brick the integration?
- Is there a configurable, governance-controlled circuit-breaker that
  can pause price-dependent functions if abnormal movement is
  detected?

**Permissioning of price-writing functions**

- Is any function that updates / snapshots the protocol's internal
  price (`updateTotalAum`, `accountForPosition`, custodial NAV
  pushers) permissioned, rate-limited, or otherwise gated against
  same-tx flash-loan abuse?
- Is the snapshot frequency low enough or the gate strict enough
  that the attacker can't pay flash-loan fees + gas just to refresh
  the snapshot at a manipulated price?

**Decimals / encoding**

- Are decimals normalised correctly (8 → 18 conversion for typical
  Chainlink price feeds)?
- Are encoded prices (e.g. UniV4 `sqrtPriceX96`) handled in the same
  encoding throughout the codebase, including in cached/last-known
  comparison logic?

## Prior incidents

- **Venus Protocol + Blizz Finance (2022-05-13) — ~$21.8M combined**:
  LUNA collapsed below Chainlink's `minAnswer` of $0.10; aggregator
  kept returning $0.10, attackers borrowed against LUNA priced at the
  floor [cites: rekt-venus-blizz-rekt].
- **Inverse Finance (2022-04-02) — $15.6M**: Short-window SushiSwap
  TWAP on thinly-traded INV/WETH was inflated 50× by a swap; attacker
  borrowed against $644k of INV valued at the manipulated price
  [cites: rekt-inverse-finance-rekt].
- **Inverse Finance (2022-06-16) — $5.8M**: yvcrv3Crypto LP price
  oracle "misused the balances of assets in the pool to directly
  calculate the LP token price"; flash-loaned WBTC imbalanced
  Curve before borrowing [cites: rekt-inverse-rekt2].
- **Deus DAO (2022-03-15) — ~$3M**: Flash-loan manipulated the
  Solidex USDC/DEI pool used as oracle on Deus's lending contract,
  forcing insolvent positions and self-liquidating them
  [cites: rekt-deus-dao-rekt].
- **Sturdy Finance (2023-06-12) — ~$800k**: Read-only reentrancy on
  Balancer B-stETH-STABLE poisoned SturdyOracle's collateral price;
  same family as Midas / dForce / EraLend / Conic
  [cites: rekt-sturdy-rekt].
- **WooFi (2024-03-05) — $8.5M (Arbitrum)**: WOOFi sPMM oracle had a
  Chainlink fallback that didn't cover the WOO token; flash-loan
  manipulated WOO price and drained WooPPV2
  [cites: rekt-woo-rekt].
- **UwuLend (2024-06-10) — $19.4M**: Fallback oracle derived prices
  from Curve pools; attacker manipulated pool state with flash loans
  to borrow sUSDe at $0.99 and liquidate at $1.03
  [cites: rekt-uwulend-rekt].
- **Makina (2026-01-20) — $4.13M**: Permissionless `updateTotalAum`
  pulled `calc_withdraw_one_coin` from Curve pools manipulated with
  a $280M flash loan from Morpho + Aave V2; "Losses caused by oracle
  price/liquidity pool manipulation" had been explicitly listed
  *out of scope* in the Cantina CTF
  [cites: rekt-makina-rekt].

## References

Audit findings (Solodit):

- `solodit-zokyo-2024-02-27-paribus-1-2` — single hard-coded
  heartbeat across all feeds
- `solodit-zokyo-2024-02-27-paribus-1-3` — `minAnswer/maxAnswer`
  circuit-breaker check missing
- `solodit-zokyo-2024-06-23-copra-1-2` — incorrect per-feed staleness
  threshold
- `solodit-zokyo-2024-06-23-copra-1-0` — lack of fallback for stale
  feed
- `solodit-zokyo-2024-06-23-copra-2-6` — Chainlink access revocation
  DOS, try-catch pattern
- `solodit-zokyo-2024-10-24-beyond-0-0` — full Chainlink checklist
  (staleness + sequencer + try-catch)
- `solodit-trust-security-2023-05-29-stella-1-2` — Arbitrum sequencer
  uptime check
- `solodit-cyfrin-2024-09-27-cyfrin-bima-v2-0-1-6` — L2 sequencer
  down check
- `solodit-cyfrin-2024-09-27-cyfrin-bima-v2-0-1-7` — `minAnswer`
  failure mode
- `solodit-cyfrin-2025-09-01-cyfrin-licredity-v2-0-2-0` — canonical
  stale-price check with PoC
- `solodit-cyfrin-2025-09-01-cyfrin-licredity-v2-0-4-0` — wrong
  short-circuit logic in price update
- `solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-1-3` — L2 sequencer
  uptime on `OracleAdapter`
- `solodit-cyfrin-2024-02-23-cyfrin-swell-barracuda-1-3` — staleness
  for Proof-of-Reserve feed
- `solodit-cyfrin-2024-09-13-cyfrin-the-standard-smart-vault-v2-0-1-2`
  — full validation diff for `latestRoundData`
- `solodit-cyfrin-2024-07-13-cyfrin-zaros-1-0` — per-feed heartbeat
  storage
- `solodit-cyfrin-2025-06-02-cyfrin-evo-soulboundtoken-v2-0-0-0`
  — common Chainlink validations checklist
- `solodit-zachobront-2023-11-01-splits-oracle-0-0` — UniV3 TWAP
  unsafe across L2 sequencer downtime
- `solodit-zachobront-2023-11-01-splits-oracle-2-0` — stale-check
  formula rearrangement
- `solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-1-1`
  — `slot0`/`sqrtPriceX96` manipulation in upkeep
- `solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-3-0` — `pool.slot0`
  manipulation risk in concentrated-liquidity strategies
- `solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-1-0`
  — circular slippage protection using `get_dy` to set `minOut`
- `solodit-recon-audits-2025-03-23-quill-finance-report-0-0` — bad
  debt vs grace period tradeoff for liquidations

Incident post-mortems (Rekt):

- `rekt-venus-blizz-rekt` — Chainlink `minAnswer` (LUNA)
- `rekt-inverse-finance-rekt` — short-window SushiSwap TWAP
- `rekt-inverse-rekt2` — LP-token oracle using raw pool balances
- `rekt-deus-dao-rekt` — Solidex pool used as oracle
- `rekt-sturdy-rekt` — Balancer read-only reentrancy on LP oracle
- `rekt-woo-rekt` — sPMM oracle with incomplete Chainlink fallback
- `rekt-uwulend-rekt` — Curve-pool fallback oracle
- `rekt-makina-rekt` — permissionless `updateTotalAum` + Curve
  `calc_withdraw_one_coin` spot price
