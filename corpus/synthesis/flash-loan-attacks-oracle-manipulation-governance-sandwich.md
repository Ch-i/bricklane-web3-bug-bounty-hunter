---
id: synthesis-flash-loan-attacks-oracle-manipulation-governance-sandwich
source: synthesis
source_url: null
title: "Flash-loan attacks: oracle manipulation, governance hijack, and sandwich variants — pattern, variants, audit checklist"
ingested_at: 2026-05-16T00:00:00Z
vuln_class:
  - oracle-manipulation
  - flash-loan
  - governance
  - mev
  - sandwich
  - price-manipulation
protocol_category:
  - lending
  - amm
  - dao
  - vault
  - bridge
tags:
  - synthesis
  - flash-loan
  - oracle
  - governance
  - sandwich
  - twap
  - spot-price
derives_from:
  - rekt-beanstalk-rekt
  - rekt-atlantis-loans-rekt
  - rekt-fortress-rekt
  - rekt-makina-rekt
  - rekt-inverse-finance-rekt
  - rekt-cream-rekt-2
  - rekt-pancakebunny-rekt
  - rekt-woo-rekt
  - rekt-deus-dao-rekt
  - rekt-sturdy-rekt
  - rekt-mango-markets-rekt
  - rekt-moola-markets-rekt
  - rekt-lodestar-rekt
  - rekt-shibarium-rekt
  - solodit-cyfrin-2023-11-10-cyfrin-dexe-0-1
  - solodit-cyfrin-2023-11-10-cyfrin-dexe-3-1
  - solodit-cyfrin-2024-01-10-cyfrin-thermae-0-0
  - solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-0-1
  - solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-2-2
  - solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-1-1
  - solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-1-0
  - solodit-cyfrin-2023-06-16-beanstalk-wells-3-17
  - solodit-cyfrin-2025-09-04-cyfrin-symbiotic-v2-0-0-0
  - solodit-pashov-audit-group-2022-11-01-yield-ninja-1-0
  - solodit-zokyo-2024-06-09-elektrik-1-5
  - solodit-zokyo-2022-03-06-radiant-capital-0-5
  - solodit-zachobront-2023-06-23-olympusdao-2-2
  - arxiv-2601.19570
---

# Flash-loan attacks: oracle manipulation, governance hijack, and sandwich variants

## Pattern

A flash loan gives an attacker huge, temporary capital that must be repaid in
the same transaction. The asset itself is never the prize — the prize is what
happens *while the capital is borrowed*. Three big families of bug emerge when
on-chain state that should be expensive to move (a DEX price, a vote tally, a
share price, a slippage minimum, a validator threshold) is cheap to move for
the duration of one atomic call.

In the **oracle-manipulation** family, the protocol reads pricing data from
something that responds to balances or reserves at the current moment: a
Uniswap V2 `getAmountsOut`/reserve ratio, Uniswap V3 `slot0`/`sqrtPriceX96`,
Curve `get_dy` / `calc_withdraw_one_coin`, a `balanceOf(address(this))`-based
share price, or a TWAP whose window is too short. The flash loan pushes the
pool, the protocol reads the lie, and a downstream action — minting, borrowing,
liquidating, redeeming, harvesting — settles at the manipulated price before
the transaction ends. This is what drained Cream Finance, Deus DAO, Inverse
Finance, PancakeBunny, Lodestar, WooFi, Sturdy and Makina; the audit findings
from Cyfrin, Zokyo and Pashov against `slot0`, `getAmountsOut`, `get_dy` and
short-window TWAPs are the same pattern caught pre-deployment.

In the **governance** family, the borrowed asset is the governance token (or
LP shares that confer voting weight). The attacker deposits, votes, and
withdraws within one block or one execution window, never holding economic
exposure to the proposal they just decided. Beanstalk lost $181M this way
because the emergency-commit path had no execution delay; Fortress and
Atlantis Loans were taken over by buying enough voting weight to push a
malicious proposal once the protocol was effectively unsupervised. Variations
exist at the validator/consensus layer (Shibarium) and at delegated-voting
layer (the Dexe finding, where flash-loaned tokens were delegated to a slave
contract to bypass per-account flash-loan checks).

In the **sandwich / on-chain-slippage** family, the protocol itself swaps and
either trusts a user-supplied `amountOutMin=0`, or *calculates* the minimum
on-chain from the same pool it's about to swap against (a circular check). An
MEV searcher — funded by a flash loan when liquidity is deep — front-runs to
move the pool, lets the victim swap execute at the manipulated price, and
back-runs to reset. This is the Yield Ninja, Beefy and Sablier-Lido findings,
and the mechanism behind WooFi's sPMM exploit. Crucially, the Sablier finding
shows that even *with* a slippage parameter the protection is illusory if
`minAmountOut` is derived from the same reserves the swap reads.

These three families share one defensive principle: any quantity that decides
real money — a price, a vote count, a slippage floor, a share value — must not
be readable and writable in the same atomic context. Either move the price
source off the manipulated surface (Chainlink, off-chain quote, native
withdrawal queue), make the read time-weighted across enough blocks that
manipulation is uneconomical, or split the read and the consequence across
blocks/snapshots.

## Variants

### V1: Spot-price oracle on AMM reserves

The protocol reads `pool.slot0` (Uniswap V3), `getReserves()` / `getAmountsOut`
(Uniswap V2), `get_dy` or `calc_withdraw_one_coin` (Curve), or
`balanceOf(address(this))` to derive a price. A flash loan distorts the pool,
the read returns the distorted value, the protocol mints/borrows/liquidates
against it. Examples: Makina (`calc_withdraw_one_coin` on Curve, permissionless
`updateTotalAum`), PancakeBunny (LP valuation from manipulated reserves),
Deus DAO (Solidex USDC/DEI used as oracle for the DEI lending market), Cream
Finance v2 ($130M via `pricePerShare = yUSD balance / totalSupply`), the
Cyfrin Thermae and Dexe `getAmountsOut` findings, the Cyfrin
`AutoRedemption` finding using `sqrtPriceX96`.

### V2: TWAP with too-short or thinly-traded window

A TWAP is used, but the time window is short enough or the pair is thin enough
that pushing the price across the window is still cheap. Inverse Finance is
the canonical case: a SushiSwap TWAP on a thinly-traded INV/WETH pair was
held above fair value across enough blocks that ~$15.6M was borrowed against
~$644k of INV collateral. The Zokyo Elektrik finding flags the same class:
`_period` configurable below 30 minutes makes TWAPs manipulable. Cyfrin's
Beanstalk-wells note plus The Standard Auto-Redemption note explicitly warn
that even canonical TWAPs are not multi-block-MEV-resistant unless the
interval is large (≥ 30 minutes).

### V3: Yield-bearing / LP collateral whose unit price is derived

The collateral is a wrapper (yUSDVault, plvGLP, stETH-LP, DUSD share token)
whose unit-price comes from `underlying / totalSupply`, `pricePerShare`, or
LP get_virtual_price. Cream v2 manipulated `yUSDVault.pricePerShare` by
redeeming most of the supply and dropping a small deposit; Lodestar
manipulated plvGLP's price by `donate()`-ing into the GlpDepositor; Sturdy
abused Curve LP oracle via read-only reentrancy. Same family as the Cyfrin
Beefy finding where an owner-controlled `setDeviation` / `setTwapInterval`
could weaken the calm-period check and then mint inflated shares via flash
loan.

### V4: Flash-loan governance takeover with no execution delay

Voting power is read at vote time (no snapshot) or with an execution path
short enough to fit one transaction. Attacker flash-loans the governance
token, deposits, votes, executes, withdraws. Beanstalk ($181M, emergency
commit had no delay), Fortress ($3M, voted to add FTS as collateral with a
70% factor and then borrowed everything), Atlantis Loans (voted to upgrade
token contracts on an abandoned protocol), Mango Markets (the attacker
voted with the stolen tokens themselves on the bailout proposal).

### V5: Flash-loan governance via delegation bypass

A per-account anti-flash-loan check (e.g. "your deposit and withdraw can't be
in the same block") is bypassed by depositing on contract A, delegating to
slave contract B, having B vote, then undelegating and withdrawing on A — all
within the same transaction. The Cyfrin Dexe finding details exactly this
PoC: the delegation/undelegation pair is not subject to the same in-block
guard as deposit/withdraw, so flash-loan governance still works.

### V6: Flash-loan validator/bridge takeover

Same principle, applied to consensus. Shibarium: the attacker flash-loaned
4.6M BONE within one block, used it to gain validator voting power, signed
a fraudulent checkpoint, and withdrew bridge funds — all atomically. L2BEAT
had warned that the bridge had no fraud-proof or validity-proof layer, so a
2/3 validator majority was sufficient and that majority was rentable.

### V7: Missing or zero slippage parameter → sandwich

The contract calls `swapExactTokensForTokens(..., amountOutMin: 0, ...)` or
performs UniswapV3 swaps with `amountOutMinimum: 0`. An MEV bot (often
flash-loan-funded if the pool is deep) sandwiches the swap. Pashov / Yield
Ninja flagged this on `_swapFarmEmissionTokens`; the Cyfrin Beefy finding
flagged it on `UniV3Utils::swap` in fee swaps; Woofi's sPMM had a fallback
that didn't actually check WOO against Chainlink, so a flash-loan attacker
moved the WOO mark and drained the pool over three swaps.

### V8: Circular on-chain slippage protection

A slippage minimum is calculated *from the same pool the swap will hit*
(`get_dy`, `slot0`, `getAmountsOut`). After flash-loan front-run, both the
quote and the swap read the manipulated reserves, so the % tolerance is
applied to the already-depressed price and the swap passes its own check
while losing real value. Cyfrin's Sablier-Lido finding documents this for
Curve `get_dy` based `minEthOut`; Cyfrin's Thermae finding documents it for
`pool.slot0`-derived `calcMinAmount`. Recommended fix in both reports: derive
`minAmountOut` from an *external* price reference (Chainlink) or accept it
from the caller computed off-chain.

### V9: Oracle stale-but-silent → voting distortion

Adjacent to flash-loan oracle manipulation: when an oracle that powers
*voting weight* silently returns 0 on staleness (Cyfrin Symbiotic finding),
an attacker can coordinate a vote to land in a window where their opponents'
voting power evaluates to zero. Not a flash loan in the classical sense, but
the same architectural sin: governance-critical state derived from a feed
whose failure mode is undefined.

## Audit checklist

Price feeds and slippage:

- Does any code path read `slot0` / `sqrtPriceX96` / `getAmountsOut` /
  `getReserves` / `get_dy` / `calc_withdraw_one_coin` /
  `balanceOf(address(this))` and feed that into pricing, share-price,
  collateral valuation, fees, or liquidation logic?
- If a TWAP is used, is the window ≥ 30 minutes and is the pair deep enough
  that moving the cumulative price is uneconomical? Is the interval bounded
  by a minimum the owner cannot lower?
- Is the price source for `minAmountOut` *the same pool the swap will hit*
  (circular slippage), or is it an external reference (Chainlink, off-chain)?
- Are all external swaps called with a real, non-zero `amountOutMin` /
  `amountOutMinimum`? Are deadlines real?
- Does an L2 deployment account for Uniswap V3 oracles being weaker on
  rollups (Cyfrin Thermae note), and the existence of multi-block MEV?
- Is share price / `pricePerShare` resistant to a one-tx redemption +
  donation that changes `totalSupply` and balance ratios (Cream v2, Lodestar
  donate)?
- For LP/wrapper collateral, is the unit-price computed via a Chainlink-style
  fair-value formula (proof of reserves + composed feeds), not via spot LP
  state?
- Does any permissionless function (`updateTotalAum`, `update`, `harvest`,
  `checkUpkeep`, `accountForPosition`) cause a price/share write inside the
  same transaction as a deposit/withdraw/borrow? (Makina)

Governance and voting:

- Can voting power be acquired *and* exercised in the same transaction or
  same block? Does the protocol use a snapshot fixed before the proposal was
  created?
- Is there an execution delay (timelock) between proposal success and effect,
  long enough for monitoring? (Beanstalk had a ~24h proposal delay but its
  emergency-commit path skipped it.)
- Does a per-account "no deposit+vote+withdraw in one tx" guard also cover
  the **delegate / undelegate** path? (Dexe)
- Is "deposit + delegate" and "undelegate + withdraw" each blocked from
  occurring with vote() in between in a single transaction?
- Are governance proposals that add new collateral, change collateral
  factors, change oracle sources, or upgrade contracts gated by a higher
  quorum or longer delay than ordinary proposals? (Fortress, Atlantis, Mango)
- For abandoned / low-attention protocols, is governance pausable or quorum
  set high enough that flash-loaned attendance can't pass a proposal alone?
  (Atlantis Loans)
- If voting power is priced (e.g. stake × oracle), what does it do on stale
  data — silently zero, or revert? (Symbiotic)

Validator / bridge consensus:

- Is the validator set small enough that a fraction can be rented via flash
  loan / liquid staking? (Shibarium: 10/12)
- Are validator-signing tokens locked / non-borrowable, or is voting weight
  measured by an instantaneous balance/stake? Are checkpoints required to be
  separated from the same-block bridge withdrawals they authorize?
- Is there a fraud-proof or validity-proof layer, or does Ethereum just
  trust the signed checkpoint?

Defense-in-depth posture:

- Are oracle reads deduplicated across blocks via "interest-rate timestamp"
  or per-block guards, and is the guard itself griefable by dust txs?
  (Olympus/ZachObront finding)
- Are admin functions that can weaken oracle/manipulation defenses
  (`setTwapInterval`, `setDeviation`, `setSlippage`) timelocked or bounded?
  (Beefy)
- Does the protocol have a mempool exposure problem on L1 (sandwichable
  swaps) that doesn't exist on L2-with-private-mempool, and conversely is the
  team aware that this property does *not* generalize to public L2 sequencers
  or relayed transactions? (arXiv 2601.19570)

## Prior incidents

- **Beanstalk (2022-04-17) — $181M** [cites: rekt-beanstalk-rekt]: Attacker
  flash-loaned ~$1B of stables + Bean LP, deposited LP tokens with voting
  weight, called `emergencyCommit` on a previously-proposed malicious BIP
  that drained the protocol contract, unwound — all atomically. No execution
  delay on the emergency path.
- **Cream Finance v2 (2021-10-27) — $130M** [cites: rekt-cream-rekt-2]:
  Flash-loan-funded loop to accumulate yUSDVault collateral, then
  manipulated `pricePerShare` by redeeming most of `totalSupply` and dropping
  a small underlying deposit, doubling collateral value and borrowing out
  $130M.
- **Mango Markets (2022-10-11) — $115M** [cites: rekt-mango-markets-rekt]:
  Bought MNGO-PERP, counter-traded with own account to spike MNGO spot from
  $0.03 → $0.91, used unrealized PnL as collateral to drain lending pools;
  then voted on bailout proposal with the stolen governance tokens.
- **WooFi (2024-03-05) — $8.5M** [cites: rekt-woo-rekt]: Flash-loan
  manipulated WOO price in the sPMM oracle; Chainlink fallback didn't
  actually cover WOO; pool drained in three swaps.
- **Inverse Finance (2022-04-02) — $15.6M** [cites: rekt-inverse-finance-rekt]:
  SushiSwap TWAP on thinly-traded INV/WETH pair held above true value across
  blocks; attacker borrowed $15.6M against $644k of INV.
- **Lodestar Finance (2022-12-10) — $6.5M** [cites: rekt-lodestar-rekt]:
  `donate()` to the GlpDepositor inflated plvGLP price oracle; flash loan
  used to maximize the manipulation and drain lending pools.
- **Sturdy Finance (2023-06-12) — $0.8M** [cites: rekt-sturdy-rekt]:
  Balancer LP read-only reentrancy used by flash loan to return a manipulated
  collateral price to SturdyOracle. Same family as Midas, dForce.
- **Fortress Protocol (2022-05-08) — $3M** [cites: rekt-fortress-rekt]:
  Public `submit()` on the price oracle plus a passing malicious governance
  proposal to add FTS as collateral with a 70% factor. Attacker used 100 FTS
  (~$4.50) as collateral to drain all assets.
- **Atlantis Loans (2023-06-10) — $2.5M** [cites: rekt-atlantis-loans-rekt]:
  On an abandoned protocol, proposal 52 passed (because no one was watching)
  and the upgrade transferred tokens from any address with live approvals.
- **PancakeBunny (2021-05-19) — $45M** [cites: rekt-pancakebunny-rekt]:
  Eight flash loans across PancakeSwap pools manipulated LP valuation in
  `VaultFlipToFlip.getReward`, minting 6.97M BUNNY (≈ $1B notional) before
  the token collapsed.
- **Deus DAO (2022-03-15) — $3M** [cites: rekt-deus-dao-rekt]: Solidex
  USDC/DEI pool used as price oracle; flash loan drained DEI from that pool,
  pushed oracle, liquidated users.
- **Moola Markets (2022-10-19) — $8.4M** [cites: rekt-moola-markets-rekt]:
  Same shape as Mango — pumped MOO on thin Ubeswap liquidity, used inflated
  collateral to borrow out the platform. Most funds returned by whitehat.
- **Makina (2026-01-20) — $4.13M** [cites: rekt-makina-rekt]: Permissionless
  `updateTotalAum()` reading `calc_withdraw_one_coin()` on Curve; $280M
  flash-loaned to distort pools, AUM updated mid-transaction, share price
  redemption drained the DUSD/USDC pool. MEV bot front-ran the original
  attacker.
- **Shibarium (2025-09-12) — $3M** [cites: rekt-shibarium-rekt]: Flash-loaned
  4.6M BONE to gain 10/12 validator voting power within one block, signed a
  fraudulent bridge checkpoint, drained the bridge — all atomic.

## References

Corpus entries (these are the same IDs as `derives_from`, exposed here so
readers can dig in):

Rekt post-mortems (oracle / governance / sandwich):
- `rekt-beanstalk-rekt` — flash-loan governance, $181M
- `rekt-atlantis-loans-rekt` — abandoned-protocol governance takeover
- `rekt-fortress-rekt` — oracle + governance combo
- `rekt-makina-rekt` — permissionless AUM update, Curve spot manipulation
- `rekt-inverse-finance-rekt` — thinly-traded TWAP held across blocks
- `rekt-cream-rekt-2` — `pricePerShare` manipulation
- `rekt-pancakebunny-rekt` — eight-flash-loan LP valuation
- `rekt-woo-rekt` — sPMM oracle + missing Chainlink fallback
- `rekt-deus-dao-rekt` — Solidex pool as oracle
- `rekt-sturdy-rekt` — Balancer read-only reentrancy → manipulated price
- `rekt-mango-markets-rekt` — spot manipulation + governance vote on bailout
- `rekt-moola-markets-rekt` — collateral-asset price manipulation
- `rekt-lodestar-rekt` — `donate()` to inflate plvGLP oracle
- `rekt-shibarium-rekt` — flash-loan validator capture, fraudulent checkpoint

Solodit audit findings:
- `solodit-cyfrin-2023-11-10-cyfrin-dexe-0-1` — flashloan + delegated-vote
  bypass of per-account guard (PoC included)
- `solodit-cyfrin-2023-11-10-cyfrin-dexe-3-1` — `getAmountsOut` flash-loan
  manipulable
- `solodit-cyfrin-2024-01-10-cyfrin-thermae-0-0` — on-chain slippage from
  `pool.slot0` is manipulable
- `solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-0-1` — no slippage on
  UniV3 swap → MEV sandwich
- `solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-2-2` — owner weakens
  `onlyCalmPeriods`, then flash-loans to inflate `slot0` and mint shares
- `solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-1-1` —
  `sqrtPriceX96` triggers automation; TWAP recommended at ≥ 900s, ideally
  1800s; note V3 TWAP not multi-block-MEV-resistant
- `solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-1-0` — circular
  Curve `get_dy`-derived `minEthOut`; fixed by Chainlink reference
- `solodit-cyfrin-2023-06-16-beanstalk-wells-3-17` — general note: on-chain
  TWAPs are inherently manipulable
- `solodit-cyfrin-2025-09-04-cyfrin-symbiotic-v2-0-0-0` — stale oracle →
  voting power silently 0
- `solodit-pashov-audit-group-2022-11-01-yield-ninja-1-0` — `amountOutMin: 0`
  on harvest → flash-loan sandwich
- `solodit-zokyo-2024-06-09-elektrik-1-5` — TWAP `_period` must be ≥ 30 min
- `solodit-zokyo-2022-03-06-radiant-capital-0-5` — single-DEX price source
  manipulable by flash loan; fixed by V2/V3 TWAP
- `solodit-zachobront-2023-06-23-olympusdao-2-2` — per-block flash-loan
  guard can be DOS'd by dust deposits

Academic:
- `arxiv-2601.19570` — sandwich attacks in private-mempool L2s: sandwiching is
  endemic on L1 but rare and unprofitable on rollups with private mempools.
