---
id: synthesis-mev-sandwich-frontrun
source: synthesis
source_url: null
title: "MEV sandwich and frontrunning: pattern, variants, audit checklist"
ingested_at: 2026-05-18T00:00:00Z
vuln_class:
  - mev
  - frontrunning
  - sandwich
  - slippage
  - oracle-manipulation
protocol_category:
  - dex
  - amm
  - yield-aggregator
  - lst
  - bonding-curve
tags:
  - synthesis
  - mev
  - sandwich
  - frontrun
  - slippage
  - deadline
  - commit-reveal
  - jit-liquidity
derives_from:
  - solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-0-1
  - solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-1-0
  - solodit-zokyo-2023-11-09-vaultka-1-8
  - solodit-pashov-audit-group-2022-11-01-yield-ninja-1-0
  - solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-2-2
  - solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-1-0
  - solodit-cyfrin-2024-01-10-cyfrin-thermae-0-0
  - solodit-zachobront-2023-03-01-sound-xyz-1-0
  - solodit-zachobront-2023-03-01-sound-xyz-1-1
  - rekt-ripmevbot
  - rekt-ripmevbot2
  - solodit-trust-security-2023-05-15-brahma-0-0
  - solodit-zokyo-2023-10-20-ember-1-0
  - solodit-cyfrin-2025-06-10-cyfrin-bunni-v2-1-3-13
  - solodit-cyfrin-2025-06-10-cyfrin-bunni-v2-1-3-19
  - solodit-0x52-2024-05-03-adapterfi-0-0
  - solodit-guardian-audits-2023-05-01-key-finance-0-1
  - solodit-zokyo-2024-02-08-liquistake-0-0
  - solodit-guardian-audits-2022-05-21-bridges-1-4
  - solodit-pashov-audit-group-2023-11-01-nftcapsule-0-0
  - solodit-zokyo-2022-07-13-umami-0-0
  - solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-2-4
  - solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-1-1
  - arxiv-2601.19570
  - arxiv-2603.07716
  - arxiv-2602.15395
---

# MEV sandwich and frontrunning

## Pattern

Maximal Extractable Value (MEV) attacks exploit the ability of block
producers — or anyone competing for inclusion via priority fees or
private order flow — to *order* transactions in their favor. The
canonical sandwich is a three-step bundle around a victim swap: a
front-run that pushes the AMM price against the victim, the victim's
trade executing at the now-degraded price, and a back-run that
unwinds the front-run's position at a profit. The arxiv SoK
[arxiv-2603.07716] traces this from Era I (public mempools and
Priority Gas Auctions) through Proposer-Builder Separation and
MEV-Boost to cross-chain MEV; the BNB Smart Chain study
[arxiv-2602.15395] shows that even private/whitelisted PBS designs
concentrate extraction in latency-advantaged builders.

In smart-contract code, sandwichable surface area appears anywhere a
protocol calls an AMM router/pool with attacker-influenceable
parameters: `amountOutMinimum: 0` on Uniswap V2/V3 router calls
[solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-0-1,
solodit-pashov-audit-group-2022-11-01-yield-ninja-1-0,
solodit-zokyo-2022-07-13-umami-0-0], unlimited slippage on Curve
`exchange` [solodit-zokyo-2023-10-20-ember-1-0], or `block.timestamp`
used as the `deadline` field — which provides no protection at all
because the block the transaction lands in always satisfies the
constraint [solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-1-0,
solodit-zokyo-2023-11-09-vaultka-1-8,
solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-2-4]. The
combination — no slippage + `deadline = block.timestamp` — gives a
validator or MEV searcher permission to hold the transaction in
mempool and execute it whenever the price is most favorable to them.

A second, subtler family is **on-chain slippage calculation**: the
contract computes `minOut` from a pool quote (`pool.slot0`,
`get_dy`, `getAmountsOut`, `calc_token_amount`, `previewRedeem`) in
the *same transaction* as the swap. Because the attacker manipulates
the same reserves both the quote and the swap read, the slippage
tolerance is applied to an already-depressed price — the protection
is circular [solodit-cyfrin-2024-01-10-cyfrin-thermae-0-0,
solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-1-0,
solodit-pashov-audit-group-2023-11-01-nftcapsule-0-0,
solodit-zokyo-2024-02-08-liquistake-0-0]. The fix in every case is
the same: take `minAmountReceived` (and `deadline`) as a user
parameter computed off-chain, or anchor it to a manipulation-
resistant external oracle (Chainlink, TWAP with a sufficiently large
window — Uniswap V3 oracles need ≥900s and are still not multi-block
MEV resistant per
[solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-1-1]).

Frontrunning more broadly is any TOD (transaction-order-dependence)
exploit: artists changing fees moments before user mints
[solodit-zachobront-2023-03-01-sound-xyz-1-0], bots manipulating
`tx.gasprice` to inflate gas reimbursement
[solodit-trust-security-2023-05-15-brahma-0-0], snipers entering a
reward-bearing position seconds before a distribution
[solodit-guardian-audits-2023-05-01-key-finance-0-1,
solodit-guardian-audits-2022-05-21-bridges-1-4], or attackers
front-running a `reveal` step in a naive commit-reveal scheme
[solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-2-2]. And as
[arxiv-2601.19570] documents, L2 private mempools blunt — but do not
eliminate — sandwich profitability; the design assumption that
"private mempool = no sandwich" is wrong.

## Variants

### V1: Zero slippage / `amountOutMinimum = 0`

The most direct form. A contract calls an AMM router with
`amountOutMin = 0` (or its equivalents — `slippage = 100%`,
`MaxUint256` deadline), letting an MEV bot extract effectively all
of the trade's value. Examples in the corpus include
`StrategyPassiveManagerUniswap._chargeFees` and
`BeefyQIVault._swapRewardsToNative` on Uniswap V3
[solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-0-1],
`_swapFarmEmissionTokens` on SpookySwap V2
[solodit-pashov-audit-group-2022-11-01-yield-ninja-1-0],
`commitAndClose -> swapToStable` on Uniswap V3 with
`amountOutMinimum: 0, deadline: block.timestamp`
[solodit-zokyo-2022-07-13-umami-0-0], and Ember Vault's
`liquidateToken()` with zero slippage and `type(uint256).max`
deadline [solodit-zokyo-2023-10-20-ember-1-0]. The pattern is
endemic to protocol-controlled swaps (harvests, fee charging,
rebalances) where developers reasoned "the caller is us, so we
don't need user-supplied slippage" — forgetting the *pool* state is
attacker-controlled.

### V2: `block.timestamp` as deadline

Setting `deadline = block.timestamp` is a no-op: by definition the
deadline holds in whatever block the tx lands in. This lets a
validator (or organic mempool congestion / NFT-mint gas spike) hold
the transaction arbitrarily long and execute it when the price has
moved against the caller
[solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-1-0,
solodit-zokyo-2023-11-09-vaultka-1-8,
solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-2-4]. The fix is
to take a real future timestamp from the caller (off-chain backend),
not `block.timestamp` and not `type(uint256).max`.

### V3: Circular / on-chain slippage calculation

The contract reads a spot price from the pool to compute `minOut`,
then performs the swap on the same pool in the same transaction.
Because the attacker manipulates the reserves before the transaction
(typically via flash loan), `get_dy` / `slot0` / `getAmountsOut`
return a value reflecting the manipulated state, and `minOut =
quote * (1 - tolerance)` is anchored to a depressed price. The swap
then passes its own slippage check while still being sandwiched.
Documented in `SablierLidoAdapter._wstETHToWeth` with Curve stETH/ETH
`get_dy` [solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-1-0],
in `Portico::calcMinAmount` using Uniswap V3 `slot0`
[solodit-cyfrin-2024-01-10-cyfrin-thermae-0-0], in
`Capsule::tradeCRVtoWETH` using Curve `get_dy`
[solodit-pashov-audit-group-2023-11-01-nftcapsule-0-0], and in
LiquiStake's `oracleClaimRewards`
[solodit-zokyo-2024-02-08-liquistake-0-0]. Mitigation: take `minOut`
as a parameter computed off-chain, or use an independent oracle
(Chainlink feed, sufficiently long TWAP).

### V4: Sandwiching deposits/withdrawals via vault share math

Slippage protection over *token amounts* doesn't catch share-price
manipulation when the underlying vault is rehypothecating into an
external ERC4626. A malicious / manipulable vault can transiently
inflate `previewRedeem` so a victim's deposit mints a tiny share
balance even though `amount0Min/amount1Min` are satisfied — only a
`sharesMin` check catches this
[solodit-cyfrin-2025-06-10-cyfrin-bunni-v2-1-3-13]. Adapter vaults
that take attacker-supplied "pregen_info" choosing between swap
and mint paths are also sandwichable
[solodit-0x52-2024-05-03-adapterfi-0-0]. The same lesson applies to
LST adapters where a single sandwiched `unstakeFullAmount` writes
`_wethReceivedAfterUnstaking` as the denominator for *all*
subsequent user redemptions, amplifying a one-shot attack across the
entire vault [solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-1-0].

### V5: JIT (Just-in-Time) liquidity sandwich

A searcher adds concentrated liquidity in the block immediately
before a large swap and removes it immediately after, capturing the
fees while the victim suffers the price impact against a thin pool.
On rebalance flows, JIT can also inflate the size of a rebalance
order so the fulfiller has to provide its own JIT liquidity, with
spillover DoS risk to other pools
[solodit-cyfrin-2025-06-10-cyfrin-bunni-v2-1-3-19]. JIT also
amplifies V3 (vault inflation) and oracle manipulation by giving
the attacker arbitrary control over `pool.liquidity()` and
`sqrtPriceX96` for a single block
[solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-1-1].

### V6: Bonding-curve / msg.value sandwich

Bonding curves are inherently sandwichable: a Flashbots bundle
`buy X => victim buy => sell X` extracts the consumer surplus
between the user's `msg.value` cap and the true market price. Even
when `msg.value` and `minimumPayout` are present, periods of high
volatility force users to set looser caps which the searcher
captures [solodit-zachobront-2023-03-01-sound-xyz-1-1]. Mitigation:
a 1-block freeze between buy and sell (enforced via the ERC721A
last-mint timestamp).

### V7: Admin/operator frontrun of protocol-state changes

A privileged role front-runs user transactions by changing a fee,
royalty, merkle root, or oracle source moments before a user
operation, then reverts it. Sound.xyz artists could bundle
`raise fees → user buys → lower fees` via Flashbots and skim up to
15% of mint volume [solodit-zachobront-2023-03-01-sound-xyz-1-0].
Defenses: revert (not silently route to admin) on bad affiliate
proofs; rate-limit role-controlled parameter changes; force changes
through a timelock.

### V8: Gas-reimbursement frontrun (`tx.gasprice` inflation)

When a contract refunds the caller `gasUsed * tx.gasprice` (relayed
keeper / bot patterns), a malicious bot can submit with an enormous
EIP-1559 priority fee to drain user fee balances — the priority fee
is burned (or paid to the validator the bot operates) but the
contract still treats it as cost to reimburse
[solodit-trust-security-2023-05-15-brahma-0-0]. Mitigation: cap the
reimbursable priority fee or read gas price from an oracle.

### V9: Distribution / dividend sniping

Stake-for-rewards systems where there is no warmup period let an
attacker enter the stake position in the block immediately before a
`distributeDividends` / `updateAllRewardsForTransferReceiver` call,
collect a pro-rata share, and exit. The bot never holds real
exposure to the underlying token
[solodit-guardian-audits-2023-05-01-key-finance-0-1,
solodit-guardian-audits-2022-05-21-bridges-1-4]. Mitigation: warmup
period before reward eligibility, or stake/unstake fee.

### V10: Reveal frontrunning (broken commit-reveal)

A commit-reveal scheme only defends if the reveal payload is *not
exploitable on its own*. Status L2's RLN slashing used commit-reveal
to bind a slasher's reward recipient, but the reveal still
contained the private key used to slash — so an attacker watching
the mempool could simply front-run the *reveal* with their own
slash transaction using the just-revealed key
[solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-2-2]. The fix is
exclusivity: make the privileged action unreachable except through
the commit-reveal flow (or only callable while no commit is
outstanding).

### V11: Private-mempool / PBS does not eliminate sandwiching

L2 private mempools (Arbitrum, Optimism sequencer) reduce sandwich
profitability — `arxiv-2601.19570` finds median net return is
negative and most flagged patterns are false positives — but
sandwiching is still feasible via redundant submissions, priority
fee placement, and sequencer ordering. On BSC, whitelisted PBS
collapses into a duopoly (48Club + Blockrazor = 87% of blocks)
with latency advantages that exclude smaller searchers
[arxiv-2602.15395]. Audit implication: do not assume "we deploy
to L2/private mempool" relieves you of slippage discipline.

### V12: MEV-bot self-pwn (insecure searcher contracts)

Searcher infrastructure is a target. 0xbad (`rekt-ripmevbot`) lost
~$1.5M because its dYdX flash-loan callback `callFunction` allowed
arbitrary execution, letting an attacker approve and drain its
WETH. A second MEV bot (`rekt-ripmevbot2`) lost ~$2M when a public,
permissionless swap function let an attacker sandwich the bot
itself on Curve WETH/WBTC via a $50M flash loan. Lesson: the same
slippage / access-control hygiene applies to the searcher's own
contracts.

## Audit checklist

Swap-call hygiene:

- Does every external swap call (`swapExactTokensForTokens`,
  `exactInput`, Curve `exchange`, `add_liquidity`,
  `remove_liquidity_one_coin`) pass a non-zero `amountOutMinimum` /
  `minOut` / `minLPOut`?
- Is `amountOutMinimum` supplied by the caller (off-chain compute),
  not computed from `pool.slot0`/`get_dy`/`getAmountsOut` in the
  same transaction?
- Is `deadline` a future timestamp supplied by the caller, not
  `block.timestamp` and not `type(uint256).max`?
- If the protocol must compute slippage on-chain, does it use a
  manipulation-resistant oracle (Chainlink stETH/ETH, Uniswap V3
  TWAP with ≥900s window) rather than the spot pool it is trading
  against?

Vault / share math:

- For deposits, is there a `minSharesOut` parameter (not just
  `minAmount0/1Out`) to defend against vault reserve inflation?
- For LST/yield adapters, is the result of a one-shot unstake/swap
  ever cached and re-used as a denominator for later user
  redemptions (amplified single-sandwich attack)?
- Is `pregen_info` / off-chain hints from a *non-trusted* caller
  ever used to choose execution paths that allow worse pricing?

Frontrunnable state changes:

- Can a privileged role change fees, royalties, merkle roots, fee
  recipients, or oracle sources in the same block as a user
  operation that reads those values? Is there a timelock or
  monotonic-only constraint?
- Can a function refund the caller `gasUsed * tx.gasprice` without
  capping `tx.gasprice` against an oracle? (EIP-1559 inflation
  drain pattern.)
- For reward distributions, is there a warmup / lock period before
  a fresh staker is eligible, or a fee on rapid stake-unstake?

Commit-reveal correctness:

- If the protocol uses commit-reveal to defeat frontrunning, is the
  revealed payload *useless on its own* — i.e. can an attacker
  observing the reveal in mempool perform the privileged action
  themselves before the original committer's tx lands?
- Is the privileged action callable *only* through the commit-reveal
  flow (make the direct entrypoint `internal` or guard it on
  outstanding commit)?

JIT-liquidity surface:

- Does the protocol rely on `pool.liquidity()` or `sqrtPriceX96` at
  a single block for sizing decisions (rebalances, redemptions,
  fee calculations)?
- Can a searcher cheaply mint a tight LP range immediately before a
  protocol action and remove it in the same block?

Bonding curves / NFT mints:

- Is `msg.value`-based slippage protection paired with a per-
  account or per-block cooldown to prevent same-block buy-then-sell
  by a searcher?
- On a faulty/missing affiliate proof, does the contract revert
  rather than silently routing the fee to the artist/operator?

Deployment context:

- For L2 deployments — does the design *assume* "private mempool
  means no sandwich"? The arxiv evidence
  [arxiv-2601.19570, arxiv-2602.15395] says don't.
- For high-frequency protocol swaps (harvests, rebalances), is
  there a private-mempool / whitelisted-caller path (Flashbots
  Protect, MEV-Share) instead of public-mempool execution?

Searcher-grade hygiene (for MEV-bot codebases):

- Are flash-loan callbacks (`callFunction`, `uniswapV2Call`,
  `executeOperation`) restricted to the expected lender?
- Are all swap-routing functions access-controlled to the bot
  operator's keys, not public?

## Prior incidents

- **0xbad MEV bot (Sep 27 2022) — $1.5M**: dYdX flash-loan
  callback `callFunction` allowed arbitrary execution; attacker
  forced bot to approve and drained its WETH. [cites:
  `rekt-ripmevbot`]
- **MEV Bot 2 / 0x05f0…24a5 (Nov 7 2023) — $2M**: unprotected
  public swap function on a Curve-arb bot let attacker sandwich
  the bot itself on WETH/WBTC using a $50M flash loan; ~$250k of
  fees accrued to Curve in the process. [cites: `rekt-ripmevbot2`]
- **BSC PBS duopoly (Apr 2025 – Feb 2026)**: 48Club + Blockrazor
  produced 87% of blocks and captured 90%+ of MEV profit on BNB
  Smart Chain, demonstrating that whitelisted PBS does not democra-
  tize extraction. [cites: `arxiv-2602.15395`]
- **L2 private-mempool study (2026)**: empirical sandwich profita-
  bility on Arbitrum/Optimism is rare and median net-negative —
  but not zero, and the result depends on naive heuristics
  understating false positives. [cites: `arxiv-2601.19570`]
- **Beefy Finance audit (Apr 2024)**: `UniV3Utils::swap` called
  with `amountOutMinimum: 0` and `deadline: block.timestamp`; fees
  drained on every harvest. [cites:
  `solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-0-1`,
  `solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-1-0`]
- **Sablier Lido adapter (Mar 2026, High)**: circular `get_dy`-
  based slippage check let attacker flash-loan-dump stETH into
  Curve, call permissionless `unstakeTokensViaAdapter`, and skim
  up to 5% from every adapter vault permanently. [cites:
  `solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-1-0`]
- **Status L2 RLN slashing (Jan 2026)**: commit-reveal scheme
  leaked the private key on reveal — attacker simply front-ran the
  reveal with their own slash. [cites:
  `solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-2-2`]
- **Sound.xyz (Mar 2023)**: artists could Flashbots-bundle
  `raise fees → user buy → lower fees`, extracting up to 15% of
  mint price; bonding curve also sandwichable without a buy-sell
  cooldown. [cites: `solodit-zachobront-2023-03-01-sound-xyz-1-0`,
  `solodit-zachobront-2023-03-01-sound-xyz-1-1`]
- **Brahma router (May 2023, High)**: malicious keeper bot
  inflates `tx.gasprice` to drain user fee-token balance via
  `gasUsed * tx.gasprice` reimbursement path. [cites:
  `solodit-trust-security-2023-05-15-brahma-0-0`]

## References

Audit findings (Solodit):

- `solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-0-1` — no
  `amountOutMinimum` on UniV3 swaps
- `solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-1-0` —
  `deadline: block.timestamp` offers no protection
- `solodit-zokyo-2023-11-09-vaultka-1-8` — same deadline footgun
- `solodit-pashov-audit-group-2022-11-01-yield-ninja-1-0` — MEV
  sandwich every harvest, 100% slippage
- `solodit-zokyo-2022-07-13-umami-0-0` — `commitAndClose`
  UniswapV3 swap sandwichable
- `solodit-zokyo-2023-10-20-ember-1-0` — `liquidateToken()` with
  unlimited slippage and deadline
- `solodit-cyfrin-2024-01-10-cyfrin-thermae-0-0` — on-chain
  slippage via `pool.slot0` manipulable
- `solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-1-0` —
  circular `get_dy` slippage, permissionless sandwich
- `solodit-pashov-audit-group-2023-11-01-nftcapsule-0-0` — Curve
  `get_dy` sandwich on protocol swaps
- `solodit-zokyo-2024-02-08-liquistake-0-0` — slippage computed
  in same tx as swap
- `solodit-cyfrin-2025-06-10-cyfrin-bunni-v2-1-3-13` — missing
  `sharesMin` lets vault inflation sandwich deposits
- `solodit-cyfrin-2025-06-10-cyfrin-bunni-v2-1-3-19` — JIT
  liquidity inflating rebalance orders
- `solodit-0x52-2024-05-03-adapterfi-0-0` — proposer-supplied
  `pregen_info` enables sandwich via Pendle adapter
- `solodit-guardian-audits-2023-05-01-key-finance-0-1` — reward
  compound sandwichable via instant stake
- `solodit-guardian-audits-2022-05-21-bridges-1-4` — dividend
  sniping via dist-distribution frontrun
- `solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-2-2` — broken
  commit-reveal: attacker frontruns the reveal
- `solodit-zachobront-2023-03-01-sound-xyz-1-0` — artist frontrun
  of fee/affiliate params
- `solodit-zachobront-2023-03-01-sound-xyz-1-1` — bonding-curve
  sandwich, 1-block buy/sell freeze fix
- `solodit-trust-security-2023-05-15-brahma-0-0` —
  `tx.gasprice` inflation drains fee balance
- `solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-2-4` —
  protocol-defined slippage and `block.timestamp` deadline
- `solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-1-1`
  — instantaneous `sqrtPriceX96` + JIT manipulation

Incidents (Rekt):

- `rekt-ripmevbot` — 0xbad lost $1.5M via unprotected dYdX flash
  callback
- `rekt-ripmevbot2` — MEV bot lost $2M to sandwich-on-sandwicher
  via permissionless swap function

Academic / SoK (arxiv):

- `arxiv-2603.07716` — SoK: evolution of MEV from PGAs through
  PBS to cross-chain
- `arxiv-2601.19570` — sandwich feasibility/profitability in L2
  private mempools (mostly net-negative, not zero)
- `arxiv-2602.15395` — MEV concentration in BSC's whitelisted PBS
