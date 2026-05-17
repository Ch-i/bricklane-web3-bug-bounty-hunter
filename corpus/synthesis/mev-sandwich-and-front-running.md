---
id: synthesis-mev-sandwich-and-front-running
source: synthesis
source_url: null
title: "MEV sandwich and front-running: patterns, variants, audit checklist"
ingested_at: 2026-05-18T00:00:00Z
vuln_class:
  - mev
  - sandwich
  - frontrun
  - slippage
  - deadline
protocol_category:
  - amm
  - dex
  - vault
  - yield-aggregator
  - liquid-staking
  - bonding-curve
tags:
  - synthesis
  - mev
  - sandwich
  - frontrun
  - slippage
  - deadline
  - jit-liquidity
  - commit-reveal
derives_from:
  - solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-0-1
  - solodit-zokyo-2023-10-20-ember-1-0
  - solodit-pashov-audit-group-2022-11-01-yield-ninja-1-0
  - solodit-zokyo-2022-07-13-umami-0-0
  - solodit-zokyo-2023-06-16-umami-1-2
  - solodit-zokyo-2023-11-09-vaultka-1-8
  - solodit-pashov-audit-group-2023-05-01-bloom-2-0
  - solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-2-4
  - solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-1-0
  - solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-3-2
  - solodit-cyfrin-2024-01-10-cyfrin-thermae-0-0
  - solodit-pashov-audit-group-2023-11-01-nftcapsule-0-0
  - solodit-cyfrin-2023-10-13-cyfrin-beanstalk-bip-38-3-2
  - solodit-zokyo-2024-02-08-liquistake-0-0
  - solodit-zachobront-2023-03-01-sound-xyz-1-1
  - solodit-zachobront-2023-03-01-sound-xyz-1-0
  - solodit-zachobront-2023-04-12-sound-xyz-0-0
  - solodit-guardian-audits-2022-05-21-bridges-1-4
  - solodit-cyfrin-2025-06-10-cyfrin-bunni-v2-1-3-19
  - solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-1-1
  - solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-2-2
  - rekt-ripmevbot
  - rekt-ripmevbot2
  - arxiv-2601.19570
  - arxiv-2603.07716
  - arxiv-2602.15395
---

# MEV sandwich and front-running

## Pattern

Maximal Extractable Value (MEV) is the profit a block proposer, builder,
or searcher can extract by re-ordering, inserting, or censoring
transactions inside a block. The two dominant patterns that touch
ordinary smart contracts are **sandwich attacks** — front-run a victim
swap with a same-direction trade, let the victim execute at the
worsened price, then back-run with the reverse trade — and
**front-running** — replacing or pre-empting a target call by paying
higher priority fees or by getting picked up by a private order flow
auction. The era-by-era SoK in `arxiv-2603.07716` traces this from
early Priority Gas Auctions in public mempools to today's
Proposer-Builder Separation (PBS) and cross-chain MEV; the empirical
study of BNB's PBS in `arxiv-2602.15395` shows extraction now
concentrates in a small set of whitelisted builders with private order
flow.

For audited code, the *protocol's* exposure to MEV is almost always
shaped by three knobs on each token movement: (1) the **minimum
output** (`amountOutMin` / `minOut`) the swap will accept, (2) the
**deadline** by which the swap must execute, and (3) where the
**price reference** used to compute either of those knobs comes from.
Bad defaults — `amountOutMinimum: 0`, `deadline: block.timestamp`,
slippage derived from the same pool the swap will hit — turn every
swap into a free sandwich for any searcher
(`solodit-zokyo-2022-07-13-umami-0-0`,
`solodit-pashov-audit-group-2022-11-01-yield-ninja-1-0`,
`solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-0-1`,
`solodit-zokyo-2023-10-20-ember-1-0`).

Beyond AMM swaps, MEV-style attacks generalize to **any state
transition that becomes more or less profitable depending on the
order of inclusion**: bonding curve mints
(`solodit-zachobront-2023-03-01-sound-xyz-1-1`), dividend distributions
(`solodit-guardian-audits-2022-05-21-bridges-1-4`), liquidity-aware
redemption automations
(`solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-1-1`),
signature-gated mints (`solodit-zachobront-2023-04-12-sound-xyz-0-0`),
and slash/commit-reveal flows
(`solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-2-2`). The same
defensive primitives apply: bound the profit window with explicit
caller-supplied outputs and short, meaningful deadlines, and remove
public-mempool observability where ordering itself is value.

Note that MEV exposure is asymmetric across execution venues: the L2
study in `arxiv-2601.19570` shows that on rollups with private mempools,
naive sandwich heuristics overstate activity and median net returns
are negative — but this is a *probabilistic* mitigation, not a
guarantee, and it does not protect against an integrating contract
forwarding swaps with no slippage check.

## Variants

### V1: Missing or zero `amountOutMin` / `minOut`

The textbook flavor: a contract performs a swap with
`amountOutMinimum = 0` (or `uint256.max` for input bounds), accepting
**100% slippage**. Any searcher watching the mempool sandwiches the
trade. Seen in Beefy's `UniV3Utils::swap`
(`solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-0-1`), Yield Ninja's
`_swapFarmEmissionTokens` harvest path
(`solodit-pashov-audit-group-2022-11-01-yield-ninja-1-0`), Umami
Tracer's `commitAndClose` Uniswap V3 swap
(`solodit-zokyo-2022-07-13-umami-0-0`), Ember's `liquidateToken`
(`solodit-zokyo-2023-10-20-ember-1-0`), and the Beanstalk BIP-38
migration script (`solodit-cyfrin-2023-10-13-cyfrin-beanstalk-bip-38-3-2`).
Even when the protocol controls the swap (vault harvest, auto-compound),
zero slippage is exploitable because anyone can call or trigger the
function in the public mempool.

### V2: Missing or ineffective `deadline`

A deadline of `block.timestamp` is not a deadline — it is satisfied by
*any* future inclusion. Validators or congested mempools can hold a
transaction and execute it later when conditions have moved against
the user (`solodit-pashov-audit-group-2023-05-01-bloom-2-0`,
`solodit-zokyo-2023-11-09-vaultka-1-8`,
`solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-2-4`,
`solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-3-2`).
Beefy's audit notes that even with a slippage check, lack of a real
deadline lets a malicious validator pick the worst calm-period
inclusion (`solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-0-1`).
Off-chain orders (escrow `fillOrder`, OTC fills) inherit the same
mempool-stale-execution risk and need a real expiry too.

### V3: Circular / on-chain slippage from a manipulable spot price

The most common *subtle* failure: the contract computes
`minOut = expectedOut * (1 - slippage)` where `expectedOut` is read
from the **same pool the swap will hit**, using a quote function like
Uniswap V3's `slot0` / `quoter` or Curve's `get_dy`. Because both the
quote and the swap read the same reserves in the same transaction, an
attacker who imbalances the pool ahead of the call sees both values
move together — the slippage check becomes circular and admits
arbitrary loss within the static `slippageTolerance` cap. The Sablier
Lido adapter's `_wstETHToWeth` is a near-perfect template: `get_dy` on
Curve's stETH/ETH pool is read into `expectedEthOut`, then
`minEthOut = expectedEthOut * 0.95` is checked against
`exchange(...)` which reads the same manipulated reserves
(`solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-1-0`).
Same pattern in Thermae/Portico via `pool.slot0`
(`solodit-cyfrin-2024-01-10-cyfrin-thermae-0-0`), in NFTCapsule's
`tradeCRVtoWETH` via Curve's `get_dy`
(`solodit-pashov-audit-group-2023-11-01-nftcapsule-0-0`), and in
LiquiStake where slippage was being computed in-contract just before
the swap (`solodit-zokyo-2024-02-08-liquistake-0-0`). The fix is to
pass `minOut` calculated *off-chain*, or anchor it to an external
reference (Chainlink, TWAP).

### V4: Hardcoded or excessively-loose slippage tolerance

Even with a real `minOut`, a hardcoded tolerance set far above market
norms (e.g. 2% when 0.5% is typical) leaves a profit window for
sandwiches every time the swap fires
(`solodit-zokyo-2023-06-16-umami-1-2`). The protocol-set slippage in
BENQI's `swapForQI` is the dual problem: users cannot override it
downward and so are forced to accept the protocol's worst-case
(`solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-2-4`).

### V5: Bonding curves and consumer-surplus capture

On bonding curves, *any* point along the curve is sandwichable. Even
when the contract exposes a max-slippage parameter (e.g. `msg.value`
as a cap on `buy()`), MEV bots capture all consumer surplus between
the user's set ceiling and the fair price during high volatility
(`solodit-zachobront-2023-03-01-sound-xyz-1-1`). The accepted fix is a
**per-block (or per-mint) freeze** between buy and sell so the same
address can't execute both legs atomically. Sound.xyz combined this
with an artist-frontrun vector
(`solodit-zachobront-2023-03-01-sound-xyz-1-0`): privileged role
holders can sandwich their own users by adjusting fees in a Flashbots
bundle around the buy.

### V6: JIT (just-in-time) liquidity manipulation

A specialized sandwich on liquidity-aware logic. The attacker mints
concentrated liquidity in a single block, lets the protocol read pool
state (`slot0`, `liquidity`, `get_dy`, or rebalance amount), then
removes the liquidity. The Standard's auto-redemption used
instantaneous `sqrtPriceX96` and `liquidity`, letting a vault owner
JIT-mint liquidity to force a redemption at a fee-skipping price
(`solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-1-1`).
Bunni v2's rebalance orders can be inflated the same way, forcing
unprofitable fulfilment
(`solodit-cyfrin-2025-06-10-cyfrin-bunni-v2-1-3-19`).

### V7: Signature / claim-ticket frontrunning

When mint or claim signatures don't bind `msg.sender`, an attacker
copies the signature out of the mempool and replays it for a smaller
quantity (or different recipient), invalidating the ticket. Sound.xyz
`FixedPriceSignatureMinterV2` lets Bob frontrun Alice's bulk claim
with a 1-NFT mint and burn her ticket
(`solodit-zachobront-2023-04-12-sound-xyz-0-0`).

### V8: Dividend / reward distribution sniping

Public `distributeDividends`-style calls let bots front-run by
depositing right before and withdrawing right after, capturing
rewards they never economically earned
(`solodit-guardian-audits-2022-05-21-bridges-1-4`). The defensive
shape is a holding period or warmup that decouples eligibility from
single-tx presence.

### V9: Insufficient commit-reveal protection

Commit-reveal is the textbook front-run defense, but only if both
phases are protected. In Status L2's slasher flow, a hash commit is
made, and at reveal time the private key is exposed in the
transaction — any observer can copy that key and front-run the
reveal itself with their own recipient
(`solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-2-2`). The pattern:
if the reveal still races a public window where the secret is
broadcast, the protection collapses.

### V10: MEV bots self-pwned (unprotected entrypoints)

Searcher contracts themselves repeatedly leave callback functions
(`callFunction` for dYdX flashloans, `0xf6ebebbb` for Curve swaps)
permissionless. Anyone can call them to drain or to sandwich the bot
against a Curve pool funded by a $50M flashloan — `rekt-ripmevbot`
($1.5M, 0xbad, 2022) and `rekt-ripmevbot2` ($2M, 2023). The audit
lesson is generic: external functions that move funds via
flash-loan-style callbacks need strict caller checks.

## Audit checklist

- For *every* DEX swap call site (Uniswap V2/V3 router, Curve
  `exchange`, etc.): is `amountOutMinimum` / `minOut` non-zero, and
  derived from data **outside** the pool being swapped against?
- Is the swap `deadline` a real time bound (e.g. `block.timestamp +
  N`) supplied by the caller, **not** literally `block.timestamp`?
- Can the slippage tolerance be **overridden downward** by the user,
  rather than fixed in the contract?
- Is `minOut` computed off-chain by the caller, or anchored to a
  manipulation-resistant oracle (Chainlink, sufficiently long
  Uniswap V3 TWAP — note V3 pool oracles are not multi-block MEV
  resistant)?
- If `slot0` / `get_dy` / spot quoter functions are read on-chain,
  are they ever fed back into a slippage check that gates a swap in
  the same transaction? (If yes, it is circular.)
- For harvest / compound / rebalance functions, is the caller
  restricted to a trusted address that submits via a private mempool
  (Flashbots Protect, MEV-Share)?
- On bonding curves or rebasing curves, is there a per-block or
  per-mint freeze that prevents a single actor from executing buy
  and sell in the same block?
- Does any function depend on instantaneous pool reserves or
  `liquidity()` that an attacker can JIT-mint into? If so, can the
  computation be moved to a TWAP or settled across blocks?
- Are claim / mint signatures bound to `msg.sender` and to an
  *exact* quantity (not a "≤ signedQuantity" range)?
- For dividend / reward distributions, is eligibility time-locked or
  warmup-gated rather than determined by a single-block snapshot?
- For commit-reveal flows, can the *reveal* itself be front-run by
  copying the revealed secret out of the mempool? Is there a
  one-shot bind from commit → execution that doesn't expose the
  secret to bystanders?
- For permissionless callback entrypoints
  (`callFunction`, `uniswapV3SwapCallback`, custom routers): is the
  caller restricted to the expected pool / lender address?
- On L2s with private mempools: does the security argument rely on
  the mempool being private, or is the contract independently safe
  if deployed to mainnet?
- For permissioned slippage settings: can governance or any role
  holder front-run users by widening the tolerance in a Flashbots
  bundle around their tx?

## Prior incidents

- **0xbad MEV bot (Sep 2022) — $1.5M**: dYdX flashloan callback
  `callFunction` was unprotected; attacker used the bot to approve
  and transfer all its WETH out
  [cites: `rekt-ripmevbot`].
- **MEV Bot 2 (Nov 2023) — $2M**: an unprotected public function
  `0xf6ebebbb` on a sandwicher contract was used (with a $50M
  flashloan) to sandwich the bot against Curve WETH/WBTC pools
  [cites: `rekt-ripmevbot2`].
- **Sablier Lido adapter (audit, 2026) — high severity, pre-deployment**:
  circular slippage protection in `_wstETHToWeth` would have let any
  attacker permanently reduce every adapter vault's WETH payout by
  flashloan-skewing Curve's stETH/ETH pool around a permissionless
  `unstakeTokensViaAdapter` call
  [cites: `solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-1-0`].
- **The Standard auto-redemption (audit, 2024) — medium**: JIT
  liquidity + instantaneous `sqrtPriceX96` would have let a vault
  owner force fee-skipping auto-redemption of their own debt
  [cites: `solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-1-1`].
- **Sound.xyz signature mint (audit, 2023) — high**: missing
  `msg.sender` and quantity binding in EIP-712 signatures let any
  observer waste a bulk claim ticket by replaying it for 1 NFT
  [cites: `solodit-zachobront-2023-04-12-sound-xyz-0-0`].

## References

- corpus entries (sandwich / slippage / deadline):
  `solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-0-1`,
  `solodit-zokyo-2023-10-20-ember-1-0`,
  `solodit-pashov-audit-group-2022-11-01-yield-ninja-1-0`,
  `solodit-zokyo-2022-07-13-umami-0-0`,
  `solodit-zokyo-2023-06-16-umami-1-2`,
  `solodit-zokyo-2023-11-09-vaultka-1-8`,
  `solodit-pashov-audit-group-2023-05-01-bloom-2-0`,
  `solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-2-4`,
  `solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-1-0`,
  `solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-3-2`,
  `solodit-cyfrin-2024-01-10-cyfrin-thermae-0-0`,
  `solodit-pashov-audit-group-2023-11-01-nftcapsule-0-0`,
  `solodit-cyfrin-2023-10-13-cyfrin-beanstalk-bip-38-3-2`,
  `solodit-zokyo-2024-02-08-liquistake-0-0`
- corpus entries (front-running specific):
  `solodit-zachobront-2023-03-01-sound-xyz-1-1`,
  `solodit-zachobront-2023-03-01-sound-xyz-1-0`,
  `solodit-zachobront-2023-04-12-sound-xyz-0-0`,
  `solodit-guardian-audits-2022-05-21-bridges-1-4`,
  `solodit-cyfrin-2025-06-10-cyfrin-bunni-v2-1-3-19`,
  `solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-1-1`,
  `solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-2-2`
- post-mortems (rekt): `rekt-ripmevbot`, `rekt-ripmevbot2`
- background (arxiv): `arxiv-2601.19570` (private L2 mempools),
  `arxiv-2603.07716` (SoK MEV evolution),
  `arxiv-2602.15395` (Binance Builder PBS)
