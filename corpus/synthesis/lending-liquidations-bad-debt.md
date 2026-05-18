---
id: synthesis-lending-liquidations-bad-debt
source: synthesis
source_url: null
title: "Lending liquidations and bad debt: pattern, variants, audit checklist"
ingested_at: 2026-05-18T00:00:00+00:00
vuln_class:
  - liquidation
  - bad-debt
  - oracle-manipulation
  - incentive-design
  - dos
protocol_category:
  - lending
  - cdp
  - perp
tags:
  - synthesis
  - liquidation
  - bad-debt
  - health-factor
  - ltv
  - liquidator-incentive
derives_from:
  - solodit-cyfrin-2025-09-01-cyfrin-licredity-v2-0-0-0
  - solodit-trust-security-2023-05-29-stella-0-2
  - solodit-zachobront-2023-11-01-fungify-1-3
  - solodit-zokyo-2024-08-15-filament-1-10
  - solodit-zokyo-2023-08-28-stfil-1-1
  - solodit-zokyo-2024-03-19-cedro-finance-1-2
  - solodit-cyfrin-2024-07-13-cyfrin-zaros-1-6
  - solodit-zokyo-2024-03-19-cedro-finance-0-3
  - solodit-zokyo-2024-01-24-narwhal-finance-0-1
  - solodit-recon-audits-2025-03-22-apollon-report-2-3
  - solodit-recon-audits-2025-03-22-apollon-report-2-11
  - solodit-hexens-2023-11-06-fungify-0-3
  - solodit-hexens-2023-11-06-fungify-0-1
  - solodit-cyfrin-2026-03-09-cyfrin-firm-money-v2-0-0-3
  - solodit-zokyo-2023-12-22-creditswap-0-0
  - solodit-zokyo-2023-12-22-creditswap-3-0
  - solodit-cyfrin-2025-07-15-cyfrin-vii-v2-0-0-0
  - solodit-cyfrin-2025-05-26-cyfrin-eulerswap-v2-0-0-1
  - solodit-recon-audits-2025-03-23-bold-report-2-15
  - rekt-aave-rekt
  - rekt-mango-markets-rekt
  - rekt-lodestar-rekt
  - rekt-cream-rekt-2
  - rekt-moola-markets-rekt
  - rekt-inverse-finance-rekt
  - rekt-uwulend-rekt
  - rekt-yieldblox-rekt
---

# Lending liquidations and bad debt

## Pattern

Every collateralized lending protocol — Aave/Compound-style pool, Liquity-style
trove + stability pool, perp/margin engine, isolated lending vault — relies on
the same chain of trust:

1. An **oracle** prices the borrower's collateral and debt.
2. A **health factor / LTV / collateralization-ratio / ICR / debt-ratio** check
   compares collateral value to debt value.
3. When that check is breached, an external **liquidator** is allowed to repay
   some or all of the debt in exchange for the collateral, sweetened by a
   **liquidation bonus / premium / discount** that funds their gas cost and
   profit.
4. Any shortfall — collateral seized worth less than debt repaid — is
   **socialized** to lenders via a stability pool offset, debt-share
   redistribution, insurance fund, or simply written off as **bad debt**.

Bad debt is the failure state of this loop. It accrues whenever (a) the
oracle is wrong, (b) the math allows users to underwater themselves
"instantly" before any external party can react, (c) the bonus is too low
for liquidators to act in time, or (d) something prevents a willing
liquidator from completing the seize transaction at all.

Across the corpus, almost every loss-of-funds incident at a lending
protocol reduces to one of those four failure modes — and high-severity
audit findings tend to describe the same patterns in dev-environment form.
The remainder of this note enumerates the recurring variants and the audit
questions that surface them.

## Variants

### V1: Oracle / collateral re-pricing into the liquidation engine

The dominant historical attack on lending markets. The attacker doesn't
break the liquidation logic — they feed the **healthy / unhealthy**
check a wrong price.

* **Spot/DEX-as-oracle**: Inverse Finance's INV oracle read a SushiSwap
  TWAP off a thinly-traded pair, letting a $500k swap mark $1.7k INV as
  collateral worth ~$15.6M [cites: rekt-inverse-finance-rekt]. Moola
  Markets allowed its own native low-liquidity MOO token as collateral
  and was drained for $8.4M by a single Ubeswap pump [cites:
  rekt-moola-markets-rekt]. YieldBlox accepted USTRY collateral on a
  market with <$1/hr of volume; a 100× sell-offer on the SDEX poisoned
  the Reflector VWAP and unlocked $10.97M of borrows [cites:
  rekt-yieldblox-rekt].
* **Vault/PPS-as-oracle**: Cream Finance v2 priced `yUSDVault` shares by
  `underlying/totalSupply`. Looped flash-loan deposit-withdraw inflated
  the share price ~2× and let the attacker borrow ~$130M against
  manipulated collateral [cites: rekt-cream-rekt-2]. Lodestar priced
  plvGLP via `assets/supply` and was drained $6.5M after `donate()`
  inflated the numerator [cites: rekt-lodestar-rekt].
* **Curve / fallback oracles**: UwuLend used Curve pool state as a
  fallback price for sUSDe; the attacker flash-loaned trades into the
  pool to skew the fallback feed, then borrowed at 0.99 and liquidated
  at 1.03 — $19.4M loss [cites: rekt-uwulend-rekt]. The Deus DAO and
  similar incidents reduce to the same pattern.
* **Perp / unrealised-PnL as collateral**: Mango Markets let a perp
  position's unrealised profit count as collateral. A $5M counter-trade
  squeezed MNGO spot 30×, then the inflated PnL was borrowed against,
  leaving $115M of bad debt [cites: rekt-mango-markets-rekt].
* **Oracle drift / safety-cap misconfig**: Aave's CAPO oracle on wstETH
  drifted ~2.85% below market after a stale 2024 snapshotRatio paired
  with a fresh timestamp; the rate-limited cap prevented correction,
  and $27.78M of healthy E-Mode positions were liquidated by the
  protocol's own anti-manipulation layer [cites: rekt-aave-rekt].

Audit-finding analogues confirm the pattern: pull-based Pyth oracles let
multiple valid prices co-exist in a 5-minute window, opening a profitable
"open trove → deposit to SP → update price → self-liquidate with bad
debt" loop [cites: solodit-recon-audits-2025-03-22-apollon-report-2-11].

### V2: Atomic self-liquidation / under-collateralize-then-seize

The borrower opens, under-collateralizes, and liquidates the same
position in one transaction, pocketing the liquidator bonus while the
shortfall socializes to lenders.

* In Licredity, the `seize` guard `position.owner != msg.sender` was
  bypassed by calling through a proxy contract. Combined with the
  `unlock` callback pattern, the attacker could open a position,
  borrow into it, and self-seize atomically — a critical-severity
  drain that required no price movement
  [cites: solodit-cyfrin-2025-09-01-cyfrin-licredity-v2-0-0-0]. The
  mitigation cited Euler's EVC/EVK approach: forbid seize on a
  position that was touched earlier in the same unlock execution.
* In Apollon, `claimUnassignedAssets` raised debt without re-checking
  the trove's ICR inside `_finaliseTrove`, opening a self-liquidation
  flow [cites: solodit-recon-audits-2025-03-22-apollon-report-2-11].

This pattern is the modern, code-level version of "borrow into bad
debt"; it doesn't need an oracle exploit, just an integrity gap in the
borrow / liquidate state machine.

### V3: Liquidator-incentive failures (bad debt by economic neglect)

Liquidation only happens if it is profitable. When it isn't, bad debt
accumulates passively.

* **Zero bonus past a threshold**: Cedro's formula set the liquidation
  discount to 0 whenever `currentLTV > 1e18`. The team cited the
  "toxic liquidation spiral" paper as justification, but the practical
  effect is that the deepest underwater positions are precisely the
  ones nobody wants to liquidate
  [cites: solodit-zokyo-2024-03-19-cedro-finance-0-3].
* **No bonus at all**: STFIL's `liquidation()` paid no reward to
  `msg.sender`, making the function uneconomic to call
  [cites: solodit-zokyo-2023-08-28-stfil-1-1].
* **Dust positions**: Narwhal allowed many tiny positions whose gas
  cost exceeded the bonus, so they decayed into bad debt unliquidated.
  Mitigation: a minimum position size
  [cites: solodit-zokyo-2024-01-24-narwhal-finance-0-1].
* **Stability-pool dependency**: Firm Money's redistribution path left
  `collGasCompensation = 0`, so when the SP was drained — exactly the
  moment liquidations matter most — no liquidator was paid anything
  [cites: solodit-cyfrin-2026-03-09-cyfrin-firm-money-v2-0-0-3]. In
  Liquity-V2-style designs, liquidator EV shifts between SP-offset and
  redistribution depending on which carries the higher penalty, and an
  attacker can rotate funds between paths to steer the protocol toward
  the worse option for itself
  [cites: solodit-recon-audits-2025-03-23-bold-report-2-15].

### V4: Liquidator-griefing / lose-premium DoS

Even when the bonus is correctly sized, the borrower can race a
liquidator and burn their gas without delivering the reward.

* **Front-run "mark-as-liquidatable" then add collateral**: in Stella,
  a victim could front-run `liquidatePosition()` with
  `markLiquidationStatus()` + `adjustExtraColls()`, restoring health
  but leaving `startLiqTimestamp != 0`. The liquidator's tx still
  executed at `discount = 0`, paying the premium for nothing
  [cites: solodit-trust-security-2023-05-29-stella-0-2].
* **Front-run with collateralization-ratio change**: Filament let
  governance change `CollateralizationRatio` with no grace period, so
  a back-runner could liquidate positions the moment they "became"
  unhealthy, without giving the borrower a chance to repay
  [cites: solodit-zokyo-2024-08-15-filament-1-10].
* **Equality / strict-balance asserts**: CreditSwap's `liquidate()`
  required `balance == debtAmount`. An attacker front-ran with a 1-wei
  transfer to make the equality false, permanently DoS'ing the
  liquidation [cites: solodit-zokyo-2023-12-22-creditswap-0-0].
* **Resume-from-pause cliff**: pausing repay but not liquidation (or
  resuming both simultaneously) lets bots sweep borrowers who had no
  chance to act [cites: solodit-zokyo-2024-03-19-cedro-finance-1-2].

### V5: Liquidation tx-reverts the borrower can engineer

Borrowers don't always need to *win* a race; they can make the seize
revert outright, locking bad debt into the vault.

* **Rounding to a whole NFT the borrower doesn't own**: Fungify's
  CErc721 `_seize` rounded up to a whole NFT, so a borrower could
  ship 1 wei of cToken to another address, leave themselves at 0.9999
  NFT, take a near-max loan, and make liquidation underflow
  permanently [cites: solodit-hexens-2023-11-06-fungify-0-3].
* **Bypassing the health check via auxiliary entry points**: also at
  Fungify, `payInterestInternal` could spend a borrower's collateral
  balance without re-running `redeemAllowed`, so a borrower could
  silently strip collateral, leaving a bad-debt loan
  [cites: solodit-hexens-2023-11-06-fungify-0-1].
* **Coordinated-account wrapper attacks**: in VII, two attacker-
  controlled accounts on an ERC-6909 LP wrapper combined fee-theft
  and enable-unowned-collateral to either inflate the transfer amount
  past the violator's balance or starve the wrapper of fees needed
  for partial unwraps, blocking liquidation entirely
  [cites: solodit-cyfrin-2025-07-15-cyfrin-vii-v2-0-0-0].
* **Reverts-on-zero-transfer collateral**: when collateral is a token
  that reverts on 0-value transfers, edge cases where `protocolFee=0`
  or `creditorFee=0` make the liquidation revert and the position
  permanently un-liquidatable [cites:
  solodit-zokyo-2023-12-22-creditswap-3-0].

### V6: Liquidation arithmetic / accounting bugs that leak value

Even when the seize succeeds, the math can pay liquidators too much,
skip redistribution, or hand back unsafe collateral.

* **Round-up reward greater than the configured incentive**: Fungify
  paid 1.08× incentive normally, but ERC-721 collateral rounded up to
  a whole NFT, producing effective bonuses up to `1/collateralFactor`
  (e.g. 1.176× at CF=0.85). The post-liquidation `afterRatio >
  beforeRatio` check did not catch it
  [cites: solodit-zachobront-2023-11-01-fungify-1-3].
* **Batch liquidations that skip redistribution**: Apollon's
  `batchLiquidateTroves` redistributed bad debt only at the end of
  the loop, so each per-trove computation used pre-redistribution
  balances and overpaid liquidators while underpaying coll stakers
  [cites: solodit-recon-audits-2025-03-22-apollon-report-2-3].
* **Riskier-collateral-first seize priority**: Zaros liquidated stable
  collateral first and left the trader with their riskiest assets,
  raising the probability of a follow-up liquidation
  [cites: solodit-cyfrin-2024-07-13-cyfrin-zaros-1-6]. The recommended
  mitigation: liquidate the *riskiest* collateral first.

### V7: Shared-collateral / cross-position bad-debt contagion

Bad debt in one position degrades the effective collateralization of
every other position sharing the vault.

* EulerSwap AMM positions are "safe by configuration" only as long as
  no unrelated position in the same vault leaves bad debt; once it
  does, the shared collateral's effective LTV slips and the AMM's
  position can be pushed into liquidation by a single swap
  [cites: solodit-cyfrin-2025-05-26-cyfrin-eulerswap-v2-0-0-1].

## Audit checklist

Use these as direct YES/NO questions when reading a lending or
margining protocol.

### Oracle / pricing surface

- Does any collateral asset rely on a spot DEX price, a single-pool
  TWAP, or a single-source VWAP with no liquidity-depth gate? [Inverse,
  Moola, YieldBlox]
- Can the oracle's collateral price be manipulated by a flash-loaned
  swap, donation, or LP imbalance in the same transaction the
  liquidation/borrow runs? [Cream, Lodestar, UwuLend, Deus]
- For "share / vault token" collateral (cTokens, LP, plvGLP, sUSDe),
  is the price computed from `assets/supply`-style state that an
  attacker can momentarily skew via `donate()`, `transfer()`, or
  imbalanced deposits? [Lodestar, Cream]
- Is unrealised PnL allowed to count as collateral, and is the spot
  feed for the underlying low-liquidity? [Mango]
- Do oracle safety caps (rate-limited growth, CAPO-style anchors)
  have a stale-anchor reset path? Can a stale anchor + a fresh
  timestamp produce a price below live market? [Aave wstETH CAPO]
- Are pull-based oracles allowed to deliver multiple prices within
  the same health-check window, enabling profitable atomic
  self-liquidation? [Apollon]

### Atomic self-liquidation surface

- Can a single user open, under-collateralize, and seize their own
  position in one transaction (directly or via a proxy contract)?
  [Licredity, Apollon]
- Is the `position.owner != msg.sender` check sufficient, or can it
  be bypassed by routing `seize` through a contract whose code path
  is controlled by the owner?
- Are any debt-mutating actions (claim, repay, fee-pay) reachable
  without re-running the health check on the affected account?
  [Fungify FNG-17]

### Liquidator-incentive design

- Is the liquidation bonus / discount strictly positive for *every*
  reachable `LTV >= 1` state? [Cedro: bonus=0 above 1e18 LTV]
- Is the bonus large enough to cover gas for the smallest admitted
  position size? Is there a minimum position size to make liquidation
  profitable? [Narwhal]
- If the protocol relies on a stability pool for offset, does the
  redistribution path still pay a non-zero gas compensation when the
  SP is empty? [Firm Money]
- If two settlement paths exist (SP offset vs redistribution), can a
  liquidator profitably steer the protocol into the worse path?
  [Liquity V2 / BOLD]
- Does the protocol re-pay a liquidator who already paid premium when
  the position is restored mid-transaction? [Stella]

### Liquidation-DoS surface

- Can a borrower front-run with a dust transfer or `addCollateral`
  call to make the liquidation revert (strict balance equality,
  rounding underflow, zero-transfer token)? [CreditSwap, Fungify
  FNG-16]
- Does seize math round in a way that can require more collateral
  than the borrower holds (whole-NFT rounding, fixed-tick wrapper
  amounts)? [Fungify, VII]
- Can a borrower (alone or with a coordinated accomplice) drain the
  wrapper / sub-position of fees or balance so that partial
  liquidations revert? [VII]
- Are `feeReceiver` and similar transfers gated by `if (amount > 0)`
  so they don't revert on zero-transfer tokens? [CreditSwap]
- If liquidation can be globally paused, is there a grace period for
  borrowers on resume? [Cedro]
- Can a privileged role (governance, operator) tighten the LTV /
  collateralization-ratio without a per-position grace period?
  [Filament]

### Bad-debt accounting

- When liquidation seizes less collateral than the debt repaid, is
  the shortfall explicitly redistributed (SP offset, debt-share
  rebase, insurance) or written off — and is the path always taken?
  [Apollon batch-redistribute]
- In multi-collateral systems, does liquidation order leave the
  borrower with *less risky* collateral, or more risky? [Zaros]
- Can bad debt in one position drop the effective LTV of every other
  position sharing the same vault, and does the protocol surface
  that to integrators? [EulerSwap]

## Prior incidents

- **Aave (March 2026) — $27.78M**: a misconfigured CAPO oracle on
  wstETH paired a stale 2024 anchor ratio with a fresh timestamp; the
  computed cap fell ~2.85% below market and 34 E-Mode positions —
  healthy in the real world — were liquidated by Aave's own anti-
  manipulation layer [cites: rekt-aave-rekt].
- **YieldBlox / Blend V2 (Feb 2026) — $10.97M**: USTRY listed as
  collateral on a market with <$1/hr of volume; a single 100× sell
  offer poisoned Reflector's VWAP, and the protocol approved health-
  passing borrows of XLM and USDC against ~$160k of real collateral
  [cites: rekt-yieldblox-rekt].
- **UwuLend (June 2024) — $19.4M**: an Aave-V2 fork with a Curve-pool
  fallback oracle. Flash-loaned trades against the underlying pools
  let the attacker borrow sUSDe at 0.99 and liquidate at 1.03
  [cites: rekt-uwulend-rekt].
- **Lodestar Finance (Dec 2022) — $6.5M**: plvGLP price derived from
  `assets/supply`; a `donate()` inflated the numerator and let the
  attacker borrow against an overvalued share
  [cites: rekt-lodestar-rekt].
- **Mango Markets (Oct 2022) — $115M**: counter-trading spiked MNGO
  perp price 30×; the unrealised long PnL was counted as collateral
  for a $115M-shortfall borrow [cites: rekt-mango-markets-rekt].
- **Moola Market (Oct 2022) — $8.4M (returned)**: low-liquidity MOO
  used as collateral; a Ubeswap pump raised the oracle price and
  unlocked the protocol's reserves [cites: rekt-moola-markets-rekt].
- **Cream Finance v2 (Oct 2021) — $130M**: `yUSDVault` priced by
  `underlying/totalSupply`; coordinated flash-loaned deposit-redeem
  doubled the share price and unlocked the lending pool
  [cites: rekt-cream-rekt-2].
- **Inverse Finance (April 2022) — $15.6M**: INV TWAP oracle from a
  thin SushiSwap pair; a 500-ETH swap held the manipulated price
  across blocks while the attacker borrowed against it
  [cites: rekt-inverse-finance-rekt].

## References

Audit findings cited in derives_from:

- solodit-cyfrin-2025-09-01-cyfrin-licredity-v2-0-0-0 — proxy-based
  self-liquidation creates bad debt
- solodit-trust-security-2023-05-29-stella-0-2 — borrower can make
  liquidator lose premium
- solodit-zachobront-2023-11-01-fungify-1-3 — NFT liquidation pays
  more than configured incentive
- solodit-zokyo-2024-08-15-filament-1-10 — back-running CR change
  forecloses repay
- solodit-zokyo-2023-08-28-stfil-1-1 — no liquidator reward
- solodit-zokyo-2024-03-19-cedro-finance-1-2 — instant liquidation
  on repay-resume
- solodit-cyfrin-2024-07-13-cyfrin-zaros-1-6 — wrong collateral-
  priority queue
- solodit-zokyo-2024-03-19-cedro-finance-0-3 — bonus = 0 when LTV>1e18
- solodit-zokyo-2024-01-24-narwhal-finance-0-1 — dust positions
  uneconomic to liquidate
- solodit-recon-audits-2025-03-22-apollon-report-2-3 — batch
  liquidations skip bad-debt redistribution
- solodit-recon-audits-2025-03-22-apollon-report-2-11 — pull oracle
  enables profitable self-liquidations
- solodit-hexens-2023-11-06-fungify-0-3 — CErc721 loans made
  un-liquidatable by transfer trick
- solodit-hexens-2023-11-06-fungify-0-1 — interest-pay path bypasses
  health check
- solodit-cyfrin-2026-03-09-cyfrin-firm-money-v2-0-0-3 — empty SP
  removes liquidator incentive
- solodit-zokyo-2023-12-22-creditswap-0-0 — strict-equality balance
  check griefable by 1-wei front-run
- solodit-zokyo-2023-12-22-creditswap-3-0 — liquidation reverts on
  zero-value collateral transfer
- solodit-cyfrin-2025-07-15-cyfrin-vii-v2-0-0-0 — attacker can make
  liquidations revert via ERC-6909 wrapper coordination
- solodit-cyfrin-2025-05-26-cyfrin-eulerswap-v2-0-0-1 — shared-vault
  bad debt contaminates configured LTV reserves
- solodit-recon-audits-2025-03-23-bold-report-2-15 — liquidators may
  prefer redistribution over SP offset

Incidents cited in derives_from:

- rekt-aave-rekt
- rekt-mango-markets-rekt
- rekt-lodestar-rekt
- rekt-cream-rekt-2
- rekt-moola-markets-rekt
- rekt-inverse-finance-rekt
- rekt-uwulend-rekt
- rekt-yieldblox-rekt
