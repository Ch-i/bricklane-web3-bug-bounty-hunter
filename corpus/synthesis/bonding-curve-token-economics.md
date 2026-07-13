---
id: synthesis-bonding-curve-token-economics
source: synthesis
source_url: null
title: "Bonding Curve Token Economics: pattern, variants, audit checklist"
ingested_at: 2026-06-04T00:00:00Z
vuln_class:
  - price-manipulation
  - flash-loan
  - mev
  - sandwich
  - slippage
  - rounding
  - dos
  - accounting
  - economic-design
protocol_category:
  - launchpad
  - amm
  - token
  - nft
  - defi
tags:
  - synthesis
  - bonding-curve
  - continuous-token
  - fair-launch
  - graduation
derives_from:
  - rekt-eminence-rekt-in-prod
  - rekt-snowdog-rekt
  - rekt-odin-fun-rekt
  - solodit-zachobront-2023-03-01-sound-xyz-0-0
  - solodit-zachobront-2023-03-01-sound-xyz-1-1
  - solodit-zachobront-2023-03-01-sound-xyz-2-1
  - solodit-hexens-2025-05-26-moonbound-0-0
  - solodit-hexens-2025-05-26-moonbound-1-2
  - solodit-hexens-2025-05-26-moonbound-1-1
  - solodit-hexens-2025-05-26-moonbound-2-0
  - solodit-hexens-2025-02-03-rush-trading-0-0
  - solodit-cyfrin-2023-06-01-sudoswap-1-2
  - solodit-cyfrin-2023-06-01-sudoswap-1-1
  - solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-6
  - solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-16
  - solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-0-7
  - solodit-zokyo-2022-10-13-thestandard-io-2-6
  - solodit-pashov-audit-group-2024-02-01-catalyst-1-0
  - arxiv-2603.07996
---

# Bonding Curve Token Economics

## Pattern

A bonding curve makes token price a deterministic function of supply: the
contract itself mints tokens when buyers deposit reserve currency and burns
them when sellers redeem, moving the price up the curve on every buy and down
on every sell. There is no order book and no external counterparty — the curve
*is* the market maker, so price discovery is fully on-chain and continuous.
This is the engine behind continuous-token / Bancor-style reserve models, NFT
mint markets (sound.xyz SAM), Sudoswap-style NFT AMMs, perp "seat" markets
(Deriverse), and the current generation of memecoin fair-launch launchpads
(Moonbound, Odin.fun, Rush) that sell on a curve and then "graduate" the token
to a normal DEX pool.

The core danger is that the *same transaction* that changes supply also changes
price. Because mint and burn are atomic and permissionless, an attacker who can
temporarily acquire a large amount of supply (flash loan) or who controls the
curve parameters can shift the price, then realize the difference against a
secondary venue or back against the curve. Eminence is the canonical example:
flash-mint EMN, burn it for the underlying eTokens to drive EMN's supply (and
therefore price) down, then redeem the rest at the depressed curve price for a
profit — $15M drained in one transaction. The arxiv tMEV work generalizes this:
any non-standard supply-control function (mint/burn on a curve) is a candidate
MEV surface that off-the-shelf searchers miss.

The second structural danger is that bonding-curve protocols are full of
*privileged state transitions* — the curve→AMM "graduation", a fixed-price→curve
switch, the first liquidity deposit into an empty pool — and each of these is a
high-value, often unprotected moment. Attackers target the seam between the
curve phase and the open-market phase, where slippage checks are weakest and the
reserve balance is largest. The third danger is purely economic: monotonic
curves guarantee that every trade is sandwichable, and curve-based "reserve"
tokenomics (OHM-forks, buyback schemes) can be engineered as rugs.

## Variants

### V1: Flash-loan / supply-control price manipulation on the curve

The curve quotes price instantaneously from current supply, so an attacker
flash-borrows reserve currency, mints (or in reverse, burns) a large slug of
supply to walk the price, and arbitrages the dislocation. In Eminence the curve
was relatively flat but bidirectional: mint EMN, burn half for eTokens to crash
EMN supply/price, then redeem the rest into DAI at the now-inflated DAI-vs-EMN
rate [cites: rekt-eminence-rekt-in-prod]. In sound.xyz SAM the attacker didn't
even need a flash loan — `create()` failed to verify that a registered "edition"
was a real edition, letting a malicious contract set its own curve parameters
(inflection price/point), inflate `data.supply` at ~zero cost, shift the curve
to raise price, and sell back into the reserve for more than was deposited,
draining the SAM contract [cites: solodit-zachobront-2023-03-01-sound-xyz-0-0].
The arxiv tMEV study formalizes the underlying surface: a static analyzer
(tSCAN on Slither) flags non-standard supply-control functions, and a searcher
(tSEARCH) extracts ~10x more profit than observed MEV by manipulating them
[cites: arxiv-2603.07996].

### V2: Graduation / migration to an AMM is unprotected

When a launchpad token finishes its curve phase it "graduates" — the contract
seeds a DEX pool with the collected reserve and a slice of supply. This call is
typically made with `amountMin = 0`, so it is sandwichable, and the pre-pool
state can be poisoned. In Moonbound an attacker could create the DEX pair early
(before graduation) and seed it with a wildly imbalanced reserve (e.g. 1e10 KAS
vs 1 wei of token); when `graduateToken()` later called `addLiquidityKAS`, the
ratio formula `amountB = amountA * reserveB / reserveA` forced almost all KAS in
against negligible tokens, and the attacker swapped to drain the pool
[cites: solodit-hexens-2025-05-26-moonbound-0-0]. Even without early pair
creation, graduation supplied liquidity with `amountTokenMin = 0` and
`amountKASMin = 0`, so anyone could buy the last tokens to trigger graduation and
sandwich the liquidity add [cites: solodit-hexens-2025-05-26-moonbound-1-2].
Deriverse shows the empty-pool analogue: the first LP into a fresh instrument
priced its deposit off `last_px`/`best_bid`/`best_ask`, which an attacker pre-set
with a 1-wei ask, forcing the honest LP to deposit at a manipulated price
[cites: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-0-7].

### V3: Graduation griefing / DoS via forced balance or boundary sells

Because graduation is gated on exact accounting, attackers grief the trigger.
Moonbound computed `kasCollected = address(this).balance`, so an attacker could
force-send extra KAS (via `selfdestruct`, bypassing the missing `receive()`)
to inflate `tokenForLiquidity` past the reserved token amount, making
`addLiquidityKAS` revert and permanently blocking graduation
[cites: solodit-hexens-2025-05-26-moonbound-1-1]. Separately, graduation fired
only on `totalTokensSold == curveTokens` (strict equality) with no minimum sell
size, so an attacker could front-run any buy by selling 1 wei of curve tokens to
push `totalTokensSold` back below the threshold and indefinitely stall the launch
[cites: solodit-hexens-2025-05-26-moonbound-2-0].

### V4: MEV sandwich and consumer-surplus capture along the curve

Any trade on a monotonic curve is sandwichable: a bot buys X tokens ahead of the
victim, lets the victim push the price up, then sells X behind them. sound.xyz
documented exactly this Flashbots bundle and noted that even with slippage params
(`msg.value` as a buy cap, `minimumPayout` on sell) bots capture all the consumer
surplus between what a user will pay and what the market requires; the fix was a
1-block freeze between buying and selling
[cites: solodit-zachobront-2023-03-01-sound-xyz-1-1]. Deriverse's seat market had
no slippage protection at all on `buy_market_seat`/`sell_market_seat`, so users
paid whatever the curve quoted at execution time
[cites: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-6], and because seat
price keyed off a live `perp_clients_count`, an attacker could pre-buy 1,000
seats and resell them around a victim's purchase to extract the difference with no
front-running required [cites: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-16].

### V5: Curve math — rounding, bounds, and formula/implementation drift

Pricing-function bugs leak value continuously rather than in one exploit.
Sudoswap's `XykCurve` and `GDACurve` used the *same* rounding direction for
`getBuyInfo` and `getSellInfo` (and didn't round fees in the protocol's favor),
so value leaks to traders, worst for low-decimal tokens — best practice is to
round buys up and sells down [cites: solodit-cyfrin-2023-06-01-sudoswap-1-1].
`GDACurve` also updated the spot price without re-checking it against `MIN_PRICE`,
letting the price decay below the intended floor
[cites: solodit-cyfrin-2023-06-01-sudoswap-1-2]. Catalyst's curve reverted via
unchecked subtraction `supply - p` whenever supply fell below the curve's premint
parameter, bricking mints [cites: solodit-pashov-audit-group-2024-02-01-catalyst-1-0].
TheStandard's `getBucketMidpoint` quantized supply in a way that diverged from the
documented `y = k*(x/m)^j + i` formula, so the implemented curve simply wasn't the
designed curve [cites: solodit-zokyo-2022-10-13-thestandard-io-2-6]. sound.xyz's
fixed-price→curve transition could never fire because the `mintConcluded()`
threshold was set to `type(uint32).max`, leaving the edition permanently in the
fixed-price phase [cites: solodit-zachobront-2023-03-01-sound-xyz-2-1].

### V6: Launch-fee / incentive bypass and curve-reserve rug economics

The economic wrapper around the curve is also attackable. In Rush, launch fees
flowed into an unlocked ERC4626 liquidity pool, so an attacker could flash-loan
WETH, deposit to capture >99.99% of the stake, launch a token to bump the share
rate, and withdraw — pocketing the launch fees and nullifying LP incentives
[cites: solodit-hexens-2025-02-03-rush-trading-0-0]. Curve-backed "reserve" token
designs can be rugs by construction: Snowdog (an OHM-fork) ran an accumulation
phase then a treasury buyback on a freshly-deployed, password-gated AMM, and the
first two transactions of the buyback captured ~$18M
[cites: rekt-snowdog-rekt]. Odin.fun's launchpad lost $7M when attackers pumped
worthless tokens through its AMM to inflate price and drained the real BTC
liquidity [cites: rekt-odin-fun-rekt].

## Audit checklist

- Can supply (and therefore price) be moved and realized within a single
  transaction — i.e. is there any buy/sell or mint/burn-back atomicity an
  attacker could flash-loan into? [sound-xyz-1-1, eminence, arxiv]
- Is there a same-block / cooldown lock between buying and selling on the curve
  (e.g. a 1-block freeze) to kill risk-free sandwich profit? [sound-xyz-1-1]
- Do buy and sell paths both have slippage protection (max-in on buy, min-out on
  sell), and is it actually enforced, not just present? [sound-xyz-1-1, deriverse-0-1-6]
- Does the graduation / curve→AMM migration set non-zero `amountTokenMin` /
  `amountReserveMin` so the liquidity add can't be sandwiched? [moonbound-1-2]
- Can the AMM pair/pool be created or seeded *before* the token graduates, and is
  pool creation gated on graduation status? [moonbound-0-0]
- Does graduation read `address(this).balance` (force-donatable via selfdestruct)
  instead of an internal accounting variable? [moonbound-1-1]
- Is the graduation trigger robust to boundary games — does it use `>=` rather
  than strict `==`, and is there a minimum sell size so 1-wei sells can't stall it?
  [moonbound-2-0]
- Are buy and sell quotes rounded in *different* directions (buy up, sell down)
  and are fees rounded in the protocol's favor? [sudoswap-1-1]
- Is every updated spot/curve price re-validated against MIN/MAX price bounds on
  the update path, not only at initial validation? [sudoswap-1-2]
- Are curve inputs (supply vs premint, supply vs MAX_SUPPLY) bounded to avoid
  underflow/overflow reverts that brick minting? [catalyst-1-0]
- Does the implemented pricing function actually match the documented curve
  formula (no quantization/precision drift)? [thestandard-io-2-6]
- For the first deposit into an empty pool/instrument, is the initial price taken
  from a manipulable spot (best_bid/best_ask/last_px) rather than user-supplied
  amounts? [deriverse-0-0-7]
- Are curve/edition/market parameters validated as legitimate, or can an attacker
  register an arbitrary contract and set their own inflection price/point?
  [sound-xyz-0-0]
- Is launch-fee or reward stake locked/vested so it can't be flash-loaned into to
  capture fees via share-rate inflation? [rush-trading-0-0]
- When a position/seat is bought and later sold, is the refund pinned to the price
  originally paid rather than re-derived from live curve state? [deriverse-0-1-16]
- Do the curve-phase→open-market state transitions actually fire under the
  documented thresholds (no unreachable `mintConcluded`-style conditions)?
  [sound-xyz-2-1]

## Prior incidents

- **Eminence (2020-09-28) — $15M**: flash-mint EMN, burn for eTokens to drop
  curve supply/price, redeem the rest into inflated DAI; ~$8M later returned
  [cites: rekt-eminence-rekt-in-prod].
- **Snowdog (2021-11-25) — $18.1M**: OHM-fork "reserve meme coin" whose treasury
  buyback on a freshly-deployed, gated AMM was captured by the first two
  transactions [cites: rekt-snowdog-rekt].
- **Odin.fun (2025-08-12) — $7M**: Bitcoin memecoin launchpad whose AMM was
  manipulated by pumping worthless tokens to inflate price and drain real BTC
  liquidity (third breach in six months) [cites: rekt-odin-fun-rekt].
- **sound.xyz SAM (2023-03, audit-stage High)**: unvalidated "editions" let an
  attacker set arbitrary curve parameters and sell back into the reserve to drain
  all funds [cites: solodit-zachobront-2023-03-01-sound-xyz-0-0].
- **Moonbound (2025-05, audit-stage High/Medium)**: early-pair-creation drain of
  the BondingCurvePool plus unprotected, griefable graduation
  [cites: solodit-hexens-2025-05-26-moonbound-0-0,
  solodit-hexens-2025-05-26-moonbound-1-1].
- **Rush (2025-02, audit-stage High)**: launch-fee bypass via flash-loan stake of
  an unlocked ERC4626 liquidity pool [cites: solodit-hexens-2025-02-03-rush-trading-0-0].

## References

- rekt-eminence-rekt-in-prod — Eminence: flash-loan bonding-curve mint/burn price manipulation ($15M)
- rekt-snowdog-rekt — Snowdog: OHM-fork reserve-token buyback rug ($18.1M)
- rekt-odin-fun-rekt — Odin.fun: launchpad AMM liquidity manipulation ($7M)
- solodit-zachobront-2023-03-01-sound-xyz-0-0 — SAM: unvalidated curve params drain reserve (High)
- solodit-zachobront-2023-03-01-sound-xyz-1-1 — SAM: MEV sandwich on curve; 1-block freeze fix (Medium)
- solodit-zachobront-2023-03-01-sound-xyz-2-1 — SAM: fixed-price→curve transition never fires (Low)
- solodit-hexens-2025-05-26-moonbound-0-0 — Moonbound: early pair creation breaks fair launch / drain (High)
- solodit-hexens-2025-05-26-moonbound-1-2 — Moonbound: no slippage protection during graduation (Medium)
- solodit-hexens-2025-05-26-moonbound-1-1 — Moonbound: forced balance donation blocks graduation (Medium)
- solodit-hexens-2025-05-26-moonbound-2-0 — Moonbound: 1-wei front-run sell prevents graduation (Low)
- solodit-hexens-2025-02-03-rush-trading-0-0 — Rush: launch-fee bypass via flash-loan stake (High)
- solodit-cyfrin-2023-06-01-sudoswap-1-2 — Sudoswap GDACurve: missing MIN_PRICE validation on update (Medium)
- solodit-cyfrin-2023-06-01-sudoswap-1-1 — Sudoswap: same rounding direction for buy/sell leaks value (Medium)
- solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-6 — Deriverse: missing slippage on seat buy/sell curve (Medium)
- solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-16 — Deriverse: pre-buy/sell seat value extraction (Medium)
- solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-0-7 — Deriverse: initial-price manipulation on empty pool (High)
- solodit-zokyo-2022-10-13-thestandard-io-2-6 — TheStandard: curve formula vs implementation drift (Informational)
- solodit-pashov-audit-group-2024-02-01-catalyst-1-0 — Catalyst: supply < premint underflow reverts mint (Medium)
- arxiv-2603.07996 — "More to Extract": tMEV from token supply-control (mint/burn) functions
