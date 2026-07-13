---
id: synthesis-yield-aggregator-composability
source: synthesis
source_url: null
title: "Yield aggregator composability patterns: pattern, variants, audit checklist"
ingested_at: 2026-06-04T19:38:53Z
vuln_class:
  - share-price-manipulation
  - flash-loan
  - oracle-manipulation
  - first-depositor
  - sandwich
  - accounting
  - access-control
  - untrusted-external-call
protocol_category:
  - yield
  - vault
  - aggregator
  - strategy
tags:
  - synthesis
  - yield-aggregator
  - composability
  - harvest
  - auto-compound
  - strategy
  - erc4626
derives_from:
  - rekt-harvest-finance-rekt
  - rekt-yearn-rekt
  - rekt-belt-rekt
  - rekt-pickle-finance-rekt
  - rekt-deathbed-confessions-c3pr
  - rekt-11-rekt
  - rekt-gamma-strategies-rekt
  - solodit-pashov-audit-group-2022-11-01-yield-ninja-1-0
  - solodit-trust-security-2023-01-08-ninja-yield-farming-v3-0-0
  - solodit-trust-security-2023-01-08-ninja-yield-farming-v3-1-2
  - solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-0-0
  - solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-2-5
  - solodit-0x52-2023-10-07-dynamo-0-2
  - solodit-zachobront-2023-11-01-stakedao-onlyboost-1-0
  - solodit-pashov-audit-group-2023-06-01-protectorate-0-0
  - solodit-oxorio-2024-02-06-zunami-protocolv2-0-2
  - solodit-zokyo-2022-03-30-spool-0-2
  - solodit-hexens-2024-07-22-tokemak-2-2
  - solodit-zokyo-2024-02-08-liquistake-0-0
  - solodit-zokyo-2024-03-06-vaultka-0-0
  - arxiv-2604.03274
---

# Yield aggregator composability patterns

## Pattern

A yield aggregator is fundamentally a *composability machine*: users deposit
an asset, the aggregator mints them vault shares, and the underlying capital is
routed into one or more **strategies** that deposit into external protocols
(AMM LP positions, lending markets, gauges, restaking, other vaults), then
periodically **harvest** the emitted reward tokens and **auto-compound** them
back into principal. Every external protocol the strategy touches is a new
trust boundary and a new source of manipulable state. The recurring failure is
that the aggregator's two core mechanisms — *share pricing* and *harvesting* —
both read or act on live, attacker-influenceable state in those external
protocols.

The first structural weakness is **share price derivation**. Most vaults price
shares as `pricePerShare = totalAssets / totalSupply`, where `totalAssets` is
computed from the *current* value of positions held in external protocols: a
Curve LP token's USD value, a lending-pool exchange rate, an oracle quote, or
the balance returned by a strategy. Because flash loans let an attacker move
that underlying state within a single transaction, they can deflate the share
price, deposit cheaply, re-inflate, and withdraw — minting "free" shares at
honest depositors' expense. This is exactly what felled Harvest, Yearn and
Belt: in each case the vault valued shares off a pool whose price the attacker
had temporarily distorted with flash-loaned capital
[rekt-harvest-finance-rekt, rekt-yearn-rekt, rekt-belt-rekt]. The same logic
appears at audit time when a strategy mints shares using a manipulable LP/oracle
price on deposit [solodit-oxorio-2024-02-06-zunami-protocolv2-0-2].

The second structural weakness is the **harvest/compound path**, which almost
always performs an AMM swap of reward tokens into the principal asset. If that
swap is unprotected (`amountOutMin = 0`, or a slippage bound computed on-chain
from the same manipulable pool), it is a free lunch for MEV sandwich bots on
every harvest [solodit-pashov-audit-group-2022-11-01-yield-ninja-1-0,
solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-0-0,
solodit-zokyo-2024-02-08-liquistake-0-0]. And because harvest is frequently
*permissionless* (anyone can call it to trigger fee accrual or keeper rewards),
it doubles as a griefing and accounting-manipulation primitive: an attacker can
front-run users to move timestamps or share ratios that gate their withdrawals
[solodit-trust-security-2023-01-08-ninja-yield-farming-v3-0-0,
solodit-0x52-2023-10-07-dynamo-0-2].

The third weakness is the **strategy/adapter trust layer** itself. Aggregators
delegate principal to strategy contracts that are often upgradeable, swappable
by an admin, or invoked via `delegatecall`. If the set of strategies/jars is not
strictly whitelisted and immutable-by-governance, the strategy becomes a rug
vector or arbitrary-code surface [rekt-pickle-finance-rekt,
rekt-deathbed-confessions-c3pr, solodit-zokyo-2022-03-30-spool-0-2]. Layered on
top of all of this is **contagion**: composed yield products inherit the risk of
every protocol beneath them, so a failure in an underlying market (or a bridge
that wraps the yield token) propagates upward
[arxiv-2604.03274]. An auditor reading aggregator code should constantly ask:
*"what external state does this number depend on, and can someone move it in the
same transaction?"*

## Variants

### V1: Flash-loan manipulation of underlying-derived share price

The vault prices shares (or mints them on deposit / values them on withdrawal)
from the *spot* state of an external pool. An attacker flash-loans capital,
distorts that pool (Curve stable balances, a Venus lending balance, an oracle
LP quote), then transacts with the vault at the wrong price and unwinds. Harvest
Finance ($25M) stretched Curve Y-pool stablecoin prices to deposit into
FARM_USDT/USDC at a depressed share price and redeem high
[rekt-harvest-finance-rekt]; Yearn's yDAI v1 vault ($11M) was gamed by inflating
the Curve 3pool through repeated flash-loaned deposit/withdraw cycles
[rekt-yearn-rekt]; Belt ($6.3M) repeatedly swapped through Ellipsis to flip its
multi-strategy "most under/over-subscribed" share valuation
[rekt-belt-rekt]. The audit-time analogue: Zunami minted shares using the
current oracle USD price of Curve LP tokens, so an elevated price yielded a
larger share of the pool than deposited value justified
[solodit-oxorio-2024-02-06-zunami-protocolv2-0-2].

### V2: Vault-level first-depositor / donation share inflation

Distinct from V1 (which abuses *external* state), this abuses the vault's *own*
empty-market rounding. The first depositor mints a tiny number of shares, then
directly transfers (donates) assets to the vault to inflate `pricePerShare`, so
the next depositor's deposit rounds down to fewer shares than it should and the
attacker redeems the difference. Seen directly in Vaultka's `gmTokenDeposit`
flow [solodit-zokyo-2024-03-06-vaultka-0-0] and reproduced (though not
profitably exploitable) in Beefy's concentrated-liquidity vault, where the first
depositor could recycle deposits/withdrawals to inflate their share count
[solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-2-5]. (See the dedicated ERC4626
inflation synthesis note for the full treatment of this sub-class.)

### V3: Unprotected harvest/compound swaps (MEV sandwich + reverting swaps)

The compound path swaps reward emissions to the principal token on an AMM. If
`amountOutMin` is hardcoded to `0`, every harvest in a public mempool is a
guaranteed sandwich [solodit-pashov-audit-group-2022-11-01-yield-ninja-1-0]. The
mirror failure is computing the slippage bound *on-chain* from the same pool
state the attacker can move, or denominating the bound in the wrong token —
Beefy's `setPositionWidth`/`unpause` redeployed liquidity into a tick-derived
range with no calm-period check, lettable into an unfavorable range by sandwich
[solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-0-0]; LiquiStake stored slippage
as a percentage of the *reward* token but compared it against the *output* token
[solodit-zokyo-2024-02-08-liquistake-0-0]. A too-rigid constant slippage bound
fails the other way — harvest reverts and rewards get stuck once accrued amounts
grow large [solodit-trust-security-2023-01-08-ninja-yield-farming-v3-1-2].

### V4: Permissionless harvest as a griefing / accounting primitive

When `harvest()` is callable by anyone (for keeper incentives), it can be used
to manipulate the state that gates other users' actions. In Ninja Yield Farming
v3, `withdrawProfit()` reverts if `block.timestamp <= lastProfitTime`; an
attacker front-runs a user's withdrawal with a permissionless `harvest()` that
bumps `lastProfitTime` to the current block, freezing the victim's yield
indefinitely [solodit-trust-security-2023-01-08-ninja-yield-farming-v3-0-0].
Dynamo's allocator blocked any adapter whose `pool.current < pool.last_value`;
because a Compound V2 share ratio can be nudged downward by careful
manipulation, an attacker could trip that check to disable the Compound adapter
and steer the vault toward their own proposal
[solodit-0x52-2023-10-07-dynamo-0-2].

### V5: Untrusted, swappable, or delegatecalled strategy/adapter layer

The aggregator routes principal through a strategy contract. If the strategy set
is not strictly whitelisted/immutable, it becomes an arbitrary-code or rug
vector. Pickle Finance ($19.7M) let its Controller accept *fake* "Pickle Jars"
that were not validated, so an attacker registered a malicious jar and drained
real funds [rekt-pickle-finance-rekt]. Compounder Finance ($12M) was rugged when
the admin swapped the live strategy for a malicious one that withdrew user
deposits — an upgradeable-strategy trust failure
[rekt-deathbed-confessions-c3pr]. Spool's `withdraw()` `delegatecall`ed into a
caller-supplied `strategies[]` address with no on-chain verification, relying on
the invariant that a strategy with zero shares is skipped
[solodit-zokyo-2022-03-30-spool-0-2]. Eleven Finance ($4.5M) exposed an
`emergencyBurn()` on an intermediary vault that let an attacker withdraw the
deposited balance *without* the withdrawal being recorded in internal
accounting, double-spending the vault's balance
[rekt-11-rekt].

### V6: Reward-token harvest accounting (stuck, lost, or mis-tallied rewards)

Multi-reward-token harvest logic is error-prone: tokens can be claimed but never
forwarded, double-counted, or lost to rounding dust. StakeDAO's harvest tallied
CRV across two claim paths but left CRV claimed as an *extra* reward token stuck
in the strategy [solodit-zachobront-2023-11-01-stakedao-onlyboost-1-0]. Tokemak's
`LiquidationRow` distributed swapped rewards pro-rata with a round-down per
vault, stranding dust because the loop never assigned the remainder
[solodit-hexens-2024-07-22-tokemak-2-2]. These are lower-severity individually
but accumulate into real, silent value leakage and signal weak harvest
accounting discipline.

### V7: Loss socialization and withdrawal ordering when assets are deployed

While principal is out working in a strategy, the vault's local balance may not
reflect strategy losses yet. If withdrawals are allowed against the local
balance at full `pricePerShare`, early withdrawers exit whole and the *last*
depositors absorb the entire loss. Protectorate's LendingVault let a user
withdraw their share from vault balance even while funds were lent to a
loss-making strategy, so the final claimants bore all losses
[solodit-pashov-audit-group-2023-06-01-protectorate-0-0]. The defense is to
either block withdrawals while funds are deployed or socialize unrealized
strategy losses into `pricePerShare` before honoring any withdrawal.

## Audit checklist

- Is `pricePerShare` / `totalAssets` ever derived from the *spot* state of an
  external pool, LP token, lending exchange rate, or oracle that a flash loan
  can move in the same transaction? (V1)
- Does the vault use a manipulation-resistant valuation (TWAP, Chainlink with
  staleness checks, or Curve/Balancer "fair" LP pricing) rather than a spot
  quote for deposit/withdraw share math? (V1)
- Is the empty-market / first-deposit case handled (dead shares, virtual
  shares/offset, seeded liquidity at deploy, or a minimum-deposit floor)? Can a
  direct token donation to the vault shift the share ratio? (V2)
- Do all harvest/compound swaps pass a non-zero `amountOutMin` derived from an
  *off-chain* or oracle-anchored expected price — not from the same pool being
  swapped against? (V3)
- Is `harvest()` restricted to trusted keepers / private mempool, or is the swap
  otherwise protected from public-mempool sandwiching? (V3)
- Is the slippage bound denominated in the correct (output) token, and is it
  configurable so harvests don't get permanently stuck as amounts grow? (V3)
- If `harvest()` (or any compound trigger) is permissionless, can calling it
  mutate any state — timestamps, share ratios, adapter eligibility — that gates
  another user's deposit, withdrawal, or claim? (V4)
- Is the set of strategies/adapters/jars strictly whitelisted, and is every
  caller-supplied strategy address validated before any `call`/`delegatecall`?
  (V5)
- Can an admin swap or upgrade the active strategy without timelock/governance,
  enabling a rug? Is strategy upgradeability behind a delay users can exit
  before? (V5)
- Do all withdraw/emergency paths decrement internal accounting atomically with
  the token transfer, so a balance can't be withdrawn without being recorded?
  (V5)
- Does multi-reward harvest forward *every* claimed reward token (including
  tokens that double as the primary reward), and does pro-rata distribution
  assign the rounding remainder rather than stranding dust? (V6)
- While principal is deployed to a strategy, are unrealized losses socialized
  into `pricePerShare` before withdrawals, so early exiters can't dump losses
  onto the last claimants? (V7)
- Does the aggregator's risk model account for contagion from every underlying
  protocol (and any bridge wrapping the yield token), not just its own code?
  (contagion)

## Prior incidents

- **Harvest Finance (2020-10-26) — $25M**: flash loans stretched Curve Y-pool
  stablecoin prices so the FARM_USDT/USDC vaults mispriced shares on
  deposit/withdraw [cites: rekt-harvest-finance-rekt].
- **Pickle Finance (2020-11-22) — $19.7M**: Controller accepted unvalidated
  "fake" Pickle Jars, letting the attacker route real funds through a malicious
  strategy [cites: rekt-pickle-finance-rekt].
- **Compounder Finance (2020-12-02) — $12M**: admin swapped the live strategy
  for a malicious contract that drained user deposits (upgradeable-strategy rug)
  [cites: rekt-deathbed-confessions-c3pr].
- **Yearn (2021-02-05) — $11M**: yDAI v1 vault gamed via repeated flash-loaned
  Curve 3pool deposit/withdraw cycles that distorted the vault's share accounting
  [cites: rekt-yearn-rekt].
- **Belt (2021-05-29) — $6.3M**: incorrect multi-strategy share valuation
  manipulated by flash-loaning through Ellipsis to flip under/over-subscribed
  strategy pricing [cites: rekt-belt-rekt].
- **Eleven Finance (2021-06-22) — $4.5M**: `emergencyBurn()` in an intermediary
  vault allowed withdrawal without updating internal accounting, double-spending
  the vault balance [cites: rekt-11-rekt].
- **Gamma Strategies (2024-01-04) — $4.5M**: concentrated-liquidity management
  protocol (a strategy/aggregator over Uniswap-style LPs) exploited via its
  deposit/position logic [cites: rekt-gamma-strategies-rekt].

## References

- corpus entries (also listed in `derives_from`):
  - rekt-harvest-finance-rekt — Harvest Finance flash-loan share mispricing ($25M)
  - rekt-yearn-rekt — Yearn yDAI v1 flash-loan vault accounting ($11M)
  - rekt-belt-rekt — Belt incorrect multi-strategy share valuation ($6.3M)
  - rekt-pickle-finance-rekt — Pickle fake-jar strategy injection ($19.7M)
  - rekt-deathbed-confessions-c3pr — Compounder upgradeable-strategy rug ($12M)
  - rekt-11-rekt — Eleven Finance `emergencyBurn` double-withdraw ($4.5M)
  - rekt-gamma-strategies-rekt — Gamma concentrated-liquidity strategy exploit ($4.5M)
  - solodit-pashov-audit-group-2022-11-01-yield-ninja-1-0 — MEV sandwich on every harvest (`amountOutMin = 0`)
  - solodit-trust-security-2023-01-08-ninja-yield-farming-v3-0-0 — permissionless harvest freezes profit withdrawals
  - solodit-trust-security-2023-01-08-ninja-yield-farming-v3-1-2 — constant slippage bound makes harvest revert / rewards stuck
  - solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-0-0 — sandwich of owner reposition redeploys liquidity into bad range
  - solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-2-5 — first-depositor share inflation in conc-liq vault
  - solodit-0x52-2023-10-07-dynamo-0-2 — share manipulation disables Compound adapter
  - solodit-zachobront-2023-11-01-stakedao-onlyboost-1-0 — CRV extra-reward token stuck in strategy
  - solodit-pashov-audit-group-2023-06-01-protectorate-0-0 — last claimant bears all strategy loss
  - solodit-oxorio-2024-02-06-zunami-protocolv2-0-2 — LP-token oracle price inflates minted shares on deposit
  - solodit-zokyo-2022-03-30-spool-0-2 — delegatecall to unverified strategy address
  - solodit-hexens-2024-07-22-tokemak-2-2 — reward distribution rounding leaves dust stuck
  - solodit-zokyo-2024-02-08-liquistake-0-0 — slippage denominated in wrong token; on-chain slippage doesn't stop frontrun
  - solodit-zokyo-2024-03-06-vaultka-0-0 — ERC4626 first-deposit share-price manipulation
  - arxiv-2604.03274 — interconnected/contagion risk of composed (liquid restaking) yield protocols
