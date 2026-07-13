---
id: synthesis-liquidity-bootstrapping-fair-launch
source: synthesis
source_url: null
title: "Liquidity Bootstrapping & Fair Launch: pattern, variants, audit checklist"
ingested_at: 2026-06-04T20:48:30Z
vuln_class:
  - price-manipulation
  - front-running
  - mev
  - flash-loan
  - first-depositor
  - access-control
  - slippage
  - rug-pull
protocol_category:
  - launchpad
  - amm
  - dex
  - token-sale
tags:
  - synthesis
  - liquidity-bootstrapping
  - fair-launch
  - lbp
  - token-launch
  - bonding-curve
  - graduation
derives_from:
  - solodit-hexens-2025-05-26-moonbound-0-0
  - solodit-hexens-2025-05-26-moonbound-1-1
  - solodit-hexens-2025-05-26-moonbound-1-2
  - solodit-zokyo-2024-07-06-zap-0-0
  - solodit-hexens-2025-02-03-rush-trading-0-0
  - solodit-hexens-2025-02-03-rush-trading-0-1
  - solodit-trust-security-2023-05-15-timeswap-0-1
  - solodit-trust-security-2023-05-15-timeswap-0-0
  - solodit-naman-2024-08-07-hyacinth-1-0
  - solodit-hexens-2023-04-17-astrolab-3-0
  - solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-0-7
  - rekt-punkprotocol-rekt
  - rekt-snowdog-rekt
  - rekt-merlin-dex-rekt
  - arxiv-2603.11324
  - arxiv-2603.24625
  - swc-114
---

# Liquidity Bootstrapping & Fair Launch

## Pattern

"Liquidity bootstrapping" and "fair launch" cover the mechanisms a protocol uses to
distribute a brand-new token and seed its first market: Balancer-style Liquidity
Bootstrapping Pools (LBPs) with shifting weights, bonding-curve launchpads that sell on a
curve and then "graduate" the token into a real DEX pool, Liquidity Generation Events
(LGEs) / "free launches" / presales, and fair-launch token sales gated by allow/blocklists.
The stated goal is *fairness and manipulation resistance*: no privileged early access, and
an initial price that nobody can cheaply skew.

The danger lives almost entirely in the **bootstrap window**. During this window the pool
is empty or thinly capitalized, the initial price/rate is derived from manipulable spot
state (reserves, an order book, `last_px`, `balance`), and the launch contract runs a
fragile state machine (selling → graduating → finalizing → enabling transfers). Because
everything is new and permissionless, an attacker can race the honest first transaction.
Recurring root causes across the corpus: (a) the *empty/first state* of a pool can be set
by whoever moves first — first-depositor, first-LP, and pool-initialization manipulation;
(b) the *graduation/finalization handoff* from launchpad to DEX is front-runnable and often
done with zero slippage protection or with the wrong order of operations; (c) launch
*economic incentives* (fees, utilisation ratios, share prices) can be gamed inside a single
block, frequently with a flash loan; (d) the instant liquidity goes live invites
*MEV/sniping*, and "anti-bot" countermeasures often become insider-information vectors; and
(e) the launch contract concentrates privilege, enabling an outright *operator rug*
(missing initializer modifier, infinite approvals to a fee address, unlocked LP).

An auditor reading launch code should treat "this only runs once, at genesis, so it doesn't
need hardening" as a red flag. The single genesis transaction is exactly where value is
densest and adversaries are most attentive. Read the empty-pool branch, the graduation
function, and every place where an initial price is *read* rather than *chosen by the
honest depositor*.

## Variants

### V1: Pre-emptive / early DEX pair creation before graduation

The launchpad assumes it will be the first to create the DEX pair, but pair creation is
permissionless. In Moonbound, an attacker buys curve tokens, then creates the
`ZealousSwap` pair himself with a wildly skewed reserve ratio (e.g. `1e10` of the base asset
to `1 wei` of the new token). When the launchpad later graduates and calls
`addLiquidityKAS`, the router uses the existing reserve ratio —
`amountB = (amountA * reserveB) / reserveA` — so it pulls in nearly all of the collected
base asset against a negligible amount of token; the attacker then swaps out and drains the
pool. Fix: only allow pair creation after the token is flagged graduated, and set the
graduated state *before* adding liquidity [cites: solodit-hexens-2025-05-26-moonbound-0-0].

### V2: Graduation / finalization handoff bugs (no slippage, wrong ordering, griefable)

The handoff from launchpad to live DEX pool is a fragile multi-step external interaction.
Three failure modes appear:

* **No slippage protection on the graduation add-liquidity.** Moonbound's `graduateToken()`
  calls `addLiquidityKAS(..., 0, 0, ...)` with zero minimums, so anyone can sandwich the
  graduation (buy the last tokens to trigger it, then front-run with an imbalanced pool)
  [cites: solodit-hexens-2025-05-26-moonbound-1-2].
* **Wrong order of operations bricks the launch.** Zap's `LiquidityFreeLaunch` calls
  `factory.getPair()` *before* the pair exists (returns address(0)) and sets `isFinalized`
  *after* `addLiquidity`; because the token blocks transfers until finalized, finalization
  reverts forever and every buyer's tokens are permanently frozen
  [cites: solodit-zokyo-2024-07-06-zap-0-0].
* **Griefing the graduation precondition.** Moonbound computes `kasCollected` from
  `address(this).balance`; an attacker force-sends dust (e.g. via `selfdestruct`, bypassing
  the missing `receive()`) so `tokenForLiquidity` exceeds the reserved supply and
  `addLiquidityKAS` reverts — the token can never graduate. Fix: cap `tokenForLiquidity` to
  the reserved amount; never derive accounting from raw balance
  [cites: solodit-hexens-2025-05-26-moonbound-1-1].

### V3: First-LP / pool-initialization price & rate manipulation

When a pool starts empty, whoever sets the first state sets the price — and that act is
front-runnable. Timeswap pools can be permissionlessly initialized multiple times, each
setting a different interest rate; an attacker sandwiches the honest LP's `addLiquidity` by
re-initializing the pool at a manipulated rate, forcing the LP to provide at a bad APR
[cites: solodit-trust-security-2023-05-15-timeswap-0-1]. A separate Timeswap bug shows the
*uninitialized default* hazard: `lastTimestamp` defaults to 0, so the first LP accrues 53+
years of returned shorts and can claim other LPs' tokens; the fix is to set `lastTimestamp`
to `block.timestamp` on the first mint
[cites: solodit-trust-security-2023-05-15-timeswap-0-0]. In Deriverse, when `ps == 0` the
first LP's deposit is priced from `last_px.max(best_bid).min(best_ask)`; an attacker plants a
1-wei ask before the LP, collapsing the computed price and making the LP overpay
[cites: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-0-7]. Defenses: make
initialize+mint atomic (single multicall), bound the initial rate/price to a sane range,
require a meaningful minimum initial liquidity, and — Uniswap-V2-style — let the depositor
choose the asset/currency amounts directly rather than reading a manipulable spot.

### V4: Flash-loan / single-block gaming of launch economics

Launch incentives that read pool state in the same block they mutate it can be drained with
a flash loan. In Rush, the per-launch fee is transferred as WETH straight into an *unlocked*
ERC4626 LiquidityPool; an attacker flash-loans WETH, deposits to own >99.99% of shares,
launches an ERC20 (which bumps the share rate), then withdraws — capturing the launch fees
as "yield." The mitigation is the canonical flash-loan defense: forbid deposit and withdraw
in the same block [cites: solodit-hexens-2025-02-03-rush-trading-0-0]. A sibling Rush bug
shows the *snapshot-vs-actual* mismatch: `calculateFee` uses a snapshotted `totalLiquidity`,
so a same-block deposit makes `outstanding + new > total`, inflating the utilisation ratio
(to `1e36`) and over-charging sponsored launches by orders of magnitude; the reverse
deflates fees. Fix: use `max(actual, snapshot)` for charging and `min(actual, snapshot)`
where under-charging is the risk [cites: solodit-hexens-2025-02-03-rush-trading-0-1].

### V5: Sniping / MEV at go-live and "anti-bot" theater

The moment liquidity is added, the first buys are the most profitable, so bots front-run
them — a textbook transaction-ordering / race-condition problem
[cites: swc-114]. Teams react with custom pools, password-gated front-ends, and on-chain
"challenge keys," but obscurity-based anti-bot measures convert MEV risk into
*insider-information* risk. Snowdog ran an 8-day accumulation then a buyback on a brand-new,
password-gated AMM "to stop bots"; the first two transactions — from fresh, exchange-funded
addresses that had pre-approved only the secret pool — captured ~40% of an $18M payout,
strongly suggesting privileged knowledge of the `challengeKey`
[cites: rekt-snowdog-rekt]. Lesson: prefer commit-reveal, snapshot-based eligibility, and
publicly verifiable fairness over secrecy that only the team controls.

### V6: Privileged-drain rug at launch (access control & approvals)

Fair-launch contracts concentrate value and privilege, making operator rugs (intentional or
via a bug) a dominant loss mode. Punk Protocol's fair-launch `CompoundModel.initialize()`
was missing an initializer modifier, letting the attacker reinitialize the `forgeAddress` to
a malicious contract and `withdrawToForge` the stablecoin pools — $8.95M, and the lack of an
"initializer" guard is the textbook lesson [cites: rekt-punkprotocol-rekt]. Merlin DEX's LGE
pools granted *max approvals to the `feeTo` address* at deployment, so a privileged actor
simply drained user deposits — a Certik-audited "rug" of $1.82M
[cites: rekt-merlin-dex-rekt]. Academic work confirms the prevalence: rug pulls
("operators abruptly withdraw liquidity after artificially inflating token value") are a top
attack class, with detectors built on pre-withdrawal on-chain + OSINT signals
[cites: arxiv-2603.11324], and Solana's low issuance barrier produced ~76k rug tokens in
H1 2025 with extremely short lifecycles and organized group behavior
[cites: arxiv-2603.24625]. Defenses: initializer guards, renounced/timelocked/multisig
ownership, no infinite approvals to EOAs or fee addresses, and LP locking.

### V7: Inert participation controls (allowlist / blocklist not wired up)

Fairness sometimes depends on access lists that are declared but never made operational.
Hyacinth's `buy()` carries an `onlyNotBlacklisted` modifier checking a `BLACKLISTED_ROLE`,
but no function exists to assign or revoke that role, so the control is dead code and any
address can participate in the "fair" launch [cites: solodit-naman-2024-08-07-hyacinth-1-0].
Relatedly, "guarded launch" phases that allow only whitelisted addresses for
front-running mitigation must actually enforce the gate during the bootstrap window and be
clearly specified [cites: solodit-hexens-2023-04-17-astrolab-3-0]. Check that every
fairness/eligibility control has live management functions and is enforced on the
launch path.

## Audit checklist

- Can the DEX pair / pool be created by anyone *before* the launchpad graduates, and does
  graduation rely on creating that pair itself? (early-pair-creation hijack)
- Is the token marked graduated/finalized *before* liquidity is added, not after?
- Does the graduation/finalization `addLiquidity` call pass real `amountMin` values, or
  zeros (sandwichable)?
- Is the finalization order of operations correct — does it read the pair *after* creation,
  and flip the `isFinalized`/transfer-enable flag *before* the transfers that depend on it?
- Does graduation accounting derive amounts from `address(this).balance` (force-sendable
  via selfdestruct) instead of tracked internal accounting?
- On an empty pool, is the initial price/rate *chosen by the honest depositor*, or *read*
  from manipulable spot state (`reserves`, `best_bid`/`best_ask`, `last_px`, an oracle)?
- Can a pool be (re)initialized separately from its first liquidity add, allowing a
  front-run/sandwich of the rate/price? Is initialize+mint atomic (single multicall)?
- Are uninitialized defaults (e.g. `lastTimestamp == 0`) handled on the first mint so the
  first LP can't accrue an outsized share?
- Is there a minimum initial liquidity requirement that makes first-state manipulation
  prohibitively expensive, and a sane bound on the initial rate/price?
- Can launch fees / share price / utilisation be moved by depositing and withdrawing in the
  same block (flash-loan gameable)? Is same-block deposit+withdraw forbidden?
- Do fee/utilisation formulas mix a *snapshot* value with *current* values such that
  `outstanding + new > total` (or the reverse) can be forced in one block? Are
  `max()`/`min()` of snapshot-vs-actual used appropriately?
- Do launch fees flow into an *unlocked* ERC4626/staking vault whose share rate they bump?
- Is there a flash-loan-resistant, snapshot-based mechanism for any per-launch eligibility
  or reward, rather than reading instantaneous balances?
- Are anti-bot/anti-snipe measures (custom pools, password gates, challenge keys) free of
  privileged insider advantage? Would commit-reveal or a public snapshot be fairer?
- Does the launch/genesis function have an initializer guard so it cannot be re-run to
  hijack privileged addresses?
- Are any max/infinite approvals granted to a fee address, deployer, or EOA on pool
  deployment? Is privileged ownership renounced / behind a multisig + timelock?
- Is bootstrapped LP locked, and is liquidity-withdrawal authority constrained (no
  single-actor drain)?
- Do allow/blocklist or "guarded launch" eligibility controls have live management
  functions and get enforced on the actual buy/deposit path?

## Prior incidents

- **Punk Protocol (Aug 10 2021) — $8.95M**: "Fair Launch" stablecoin pools drained because
  `CompoundModel.initialize()` lacked an initializer modifier; attacker reset `forgeAddress`
  to a malicious contract and withdrew (~$5M later returned by a whitehat frontrun)
  [cites: rekt-punkprotocol-rekt].
- **Snowdog (Nov 25 2021) — $18.1M**: OHM-fork buyback run on a secret, password-gated AMM
  "to stop bots"; the first two exchange-funded addresses with apparent prior knowledge of
  the `challengeKey` took ~40% of the payout — anti-bot theater as an insider-sniping vector
  [cites: rekt-snowdog-rekt].
- **Merlin DEX (Apr 25 2023) — $1.82M**: During a 3-day Liquidity Generation Event, LGE
  pools granted max approvals to the `feeTo` address on deployment; the privileged actor
  drained user deposits — a Certik-audited rug [cites: rekt-merlin-dex-rekt].
- **Moonbound (audit, 2025) — Critical/High**: Permissionless early pair creation let an
  attacker pre-skew reserves and drain nearly all collected base asset at graduation; sibling
  findings: no slippage on graduation add-liquidity, and force-send griefing that blocks
  graduation [cites: solodit-hexens-2025-05-26-moonbound-0-0,
  solodit-hexens-2025-05-26-moonbound-1-2, solodit-hexens-2025-05-26-moonbound-1-1].
- **Rush Trading (audit, 2025) — High**: Launch-fee bypass by flash-loan staking into an
  unlocked ERC4626 pool, and utilisation-ratio inflation via snapshot-vs-actual liquidity
  mismatch [cites: solodit-hexens-2025-02-03-rush-trading-0-0,
  solodit-hexens-2025-02-03-rush-trading-0-1].
- **Timeswap (audit, 2023) — High**: Pool initialization front-run to set a manipulated
  interest rate, and a first-LP `lastTimestamp == 0` default that let the first LP claim
  others' shorts [cites: solodit-trust-security-2023-05-15-timeswap-0-1,
  solodit-trust-security-2023-05-15-timeswap-0-0].
- **Deriverse (audit, 2025) — High**: First LP into an empty instrument priced from a
  manipulable order book (`last_px.max(best_bid).min(best_ask)`); a planted 1-wei ask made
  the honest LP overpay [cites: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-0-7].
- **Zap / Hyacinth (audits, 2024) — High/Medium**: Free-launch finalization order-of-ops bug
  permanently froze buyers' tokens; fair-launch blocklist with no management functions left
  the control inert [cites: solodit-zokyo-2024-07-06-zap-0-0,
  solodit-naman-2024-08-07-hyacinth-1-0].

## References

- solodit-hexens-2025-05-26-moonbound-0-0 — Early pair creation breaks fair launch, drains KAS (High)
- solodit-hexens-2025-05-26-moonbound-1-1 — Force-send KAS blocks token graduation (Medium)
- solodit-hexens-2025-05-26-moonbound-1-2 — No slippage protection during graduation (Medium)
- solodit-zokyo-2024-07-06-zap-0-0 — LiquidityFreeLaunch never finalizes; tokens frozen (High)
- solodit-hexens-2025-02-03-rush-trading-0-0 — Launch fee bypass via flash-loan stake of unlocked ERC4626 (High)
- solodit-hexens-2025-02-03-rush-trading-0-1 — Utilisation ratio >100% inflates/deflates launch fees (High)
- solodit-trust-security-2023-05-15-timeswap-0-1 — Pool init front-run to manipulate interest rate (High)
- solodit-trust-security-2023-05-15-timeswap-0-0 — First LP claims others' shorts via lastTimestamp=0 (High)
- solodit-naman-2024-08-07-hyacinth-1-0 — Fair-launch blocklist with no management functions (Medium)
- solodit-hexens-2023-04-17-astrolab-3-0 — Guarded-launch phase / front-running-mitigation parameter (Informational)
- solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-0-7 — Initial-mint price manipulation via order book (High)
- rekt-punkprotocol-rekt — Punk Protocol fair launch, missing initializer modifier ($8.95M)
- rekt-snowdog-rekt — Snowdog buyback on secret AMM, insider sniping ($18.1M)
- rekt-merlin-dex-rekt — Merlin DEX LGE rug via max approvals to feeTo ($1.82M)
- arxiv-2603.11324 — LROO Rug Pull Detector (leakage-resistant on-chain + OSINT framework)
- arxiv-2603.24625 — SolRugDetector (Solana rug-pull empirical study & detector)
- swc-114 — Transaction Order Dependence (race conditions / front-running)
