---
id: synthesis-staking-accounting-slashing
source: synthesis
source_url: null
title: "Staking accounting and slashing math: pattern, variants, audit checklist"
ingested_at: 2026-05-18T00:00:00Z
vuln_class:
  - accounting
  - reward-distribution
  - slashing
  - staking
  - precision-loss
  - dos
protocol_category:
  - liquid-staking
  - restaking
  - staking
  - validator-middleware
tags:
  - synthesis
  - staking
  - slashing
  - rewards-per-share
  - unbonding
  - checkpoint
  - exchange-rate
derives_from:
  - solodit-cyfrin-2025-10-21-cyfrin-illuvium-stakingv3-v2-0-0-2
  - solodit-hans-2023-07-13-meta-0-1
  - solodit-hexens-2024-07-22-tokemak-1-3
  - solodit-0x52-2024-03-27-blueberry-staking-1-2
  - solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-1-16
  - solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-1-7
  - solodit-hexens-2025-05-26-zealous-1-1
  - solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-0-1
  - solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-0-6
  - solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-1-17
  - solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-1-11
  - solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-0-0
  - solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-1-2
  - solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-0-0
  - solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-2-1
  - solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-2-7
  - solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-1-2
  - solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-1-0
  - solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-1-4
  - solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-0-11
  - solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-0-8
  - solodit-zachobront-2023-09-01-obol-0-2
  - solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-1-0
  - solodit-cyfrin-2023-11-03-cyfrin-streamr-1-2
  - solodit-cyfrin-2025-05-19-cyfrin-stakedotlink-polygon-staking-v2-0-0-0
  - solodit-hexens-2024-01-12-persistence-2-2
  - solodit-hexens-2023-04-14-lido-0-0
  - rekt-theidolsnft-rekt
  - rekt-betterbank-rekt
  - rekt-ankr-helio-rekt
  - arxiv-2601.05827
---

# Staking accounting and slashing math

## Pattern

Staking systems implement three intertwined ledgers: (1) **principal /
share accounting** that tracks who is entitled to how much underlying,
(2) **reward accounting** that allocates emissions or fees pro-rata to
stakers over time, and (3) **slashing / unbonding accounting** that
deducts penalties and processes withdrawals across epochs. Bugs almost
always sit at the seam between these ledgers: a state mutation in one
must trigger a synchronised update in the others, and rounding,
boundary conditions, or paused side-effects on one side silently corrupt
the other.

The dominant attack patterns are: (a) *exchange-rate / share-price
manipulation* — donations or controlled empty-pool states ratchet the
share price so future depositors mint nothing or attackers withdraw
more than they deposited; (b) *stale or look-ahead snapshots* —
checkpoints are written for epochs that haven't happened, or operators
who were disabled at exactly the epoch boundary are still counted,
diluting honest stakers; (c) *reward-per-share update ordering* —
boost factors, lock changes, balance updates, or rewarder removal that
do not call the standard "update rewards first" pattern, letting users
re-apply a new multiplier retroactively to historical accruals; (d)
*slashing arithmetic and DoS* — per-distributor rounding compounds,
loops over user-registered objects can be ballooned to OOG, paused
sub-modules block the whole slash, and cascading "excess" slash flows
underflow on adjacent buckets; (e) *unbonding-queue and discount-factor
errors* — request indices, hint validation, or proportional dividing
let claimants take more than their share or starve other validators of
their turn.

Because liquid-staking tokens (LSTs) are themselves used as collateral,
oracle inputs, and governance weight elsewhere in DeFi, a small
accounting bug propagates: mis-minted shares get bridged, deposited as
collateral, and become an infinite-mint money-printer (Ankr/Helio).
A reward accumulator that double-counts a single transfer (The Idols
NFT) drains the underlying staking-yield reserve. Any audit of a
staking system must therefore reason about every state-change function
under three lenses: rewards-up-to-date, exchange-rate-invariant,
slash-still-possible.

## Variants

### V1: First-depositor / empty-pool exchange-rate ratchet

When the share supply transiently returns to zero (after full unstakes,
during recovery mode, or pre-launch), the next deposit is priced
against a "highest-ever" or stored rate rather than reseeding to 1:1.
In ZEALInfinityPool the attacker repeatedly stakes/unstakes when supply
is zero while seeding rewards, doubling the floor exchange rate each
cycle until any new deposit mints zero shares — pure DoS [cites:
solodit-hexens-2025-05-26-zealous-1-1]. The classic ERC4626 inflation
attack is the symmetric case during initial deposit (see
synthesis-erc4626-vault-inflation-attack).

### V2: Future-epoch / look-ahead checkpoint poisoning

`calcAndCacheStakes(futureEpoch, ...)` writes the current stake into a
cache keyed by a future epoch; once the flag is set, the real stake at
that epoch is ignored forever. Attackers freeze in a high stake before
withdrawing, then collect rewards as if they had never withdrawn
[cites: solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-0-1]. The fix
is to reject `epoch > currentEpoch` in cache writes.

### V3: Inclusive boundary on enabled/disabled timestamps

`_wasActiveAt(enabled, disabled, ts)` returning `disabled >= ts` instead
of `disabled > ts` makes operators "active" at the exact timestamp they
were disabled. If they are disabled at the epoch-start tick, their
stake is still counted in `totalStake`, diluting all honest operators'
reward shares for that epoch [cites:
solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-0-6]. A symmetric
bug is operators legitimately active during epoch N being purged from
`getAllOperators()` before rewards for N are distributed because the
slashing window is shorter than the reward-distribution delay
[cites: solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-1-11].

### V4: Missing stake-locking allows double-allocation

`addNode()` computed "available stake" without ever incrementing
`operatorLockedStake`, so the same collateral could back N validators
in a single epoch. Reward shares for that operator exceed 100% of their
legitimate weight, and totalShares for the epoch sum >10000 bp,
diluting everyone else [cites:
solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-1-17].

### V5: Reward accumulator not updated before parameter change

`rewardPerToken` / `accRewardPerShare` style accumulators require that
any function changing a user's effective weight (balance, boost,
lock-status, delegation) first call the "update rewards" hook. When it
doesn't, the new multiplier is retroactively applied to all historical
accruals — e.g. enabling a lock-boost on day 90 retroactively boosts
the first 90 days of rewards [cites: solodit-hans-2023-07-13-meta-0-1].
Same class: removing an `ExtraRewarder` from a `MainRewarder` stops
balance-change hooks but `earned(user)` still reads MainRewarder state,
so a withdraw/re-stake on a fresh account claims the full remaining
pool [cites: solodit-hexens-2024-07-22-tokemak-1-3]. Same class:
`getVoteWeight()` mixing a *current* balance with a *prior-week*
weight, inflating vote power 5x [cites:
solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-1-7].

### V6: Rewards lost / stuck when totalStaked is zero or precision is too low

`accIlvPerShare += rewardAmount * PRECISION / totalStaked` truncates if
`PRECISION` is only 1e12; on small total-stake balances dust rewards
get permanently locked [cites:
solodit-cyfrin-2025-10-21-cyfrin-illuvium-stakingv3-v2-0-0-2]. The
opposite failure mode: when `totalSupply == 0` the per-share rate
returns the stored value, but `lastUpdateTime` is still advanced —
rewards that accrued during the zero-supply window are silently lost
[cites: solodit-0x52-2024-03-27-blueberry-staking-1-2]. In epoch-based
systems the same truncation applied to uptime distribution
(`uptimeToDistribute / elapsedEpochs`) can drop a validator below the
`minRequiredUptime` threshold and zero their entire epoch's rewards
[cites: solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-1-16].

### V7: Slashing DoS via loops over user-controlled objects

`_slash()` iterates over `accountVaults` (or `rewardDistributors`,
or any other set the slashed user can grow). The attacker spams vault
registrations until the loop hits the block gas limit, making slashing
impossible [cites: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-0-0;
solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-1-0]. The same loop
construction breaks when *any* one of the iterated reward-distributors
is `whenNotPaused` and currently paused — the slash reverts wholesale
[cites: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-2-7]. Defence is
hard caps on the iterated set and skipping (not reverting on) paused
sub-modules.

### V8: Compounded slash rounding (overslashing)

`_calculateSlashAmount` floors to `MIN_SLASH_AMOUNT` when the
percentage-based slash would be tiny. Calling that helper once per
sub-balance and summing the results converts "50% of total" into a
multiple-of-MIN_SLASH penalty — users lose 2-3× the intended amount
[cites: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-2-1]. The
mitigation is to apply the minimum once on the *final* aggregated
amount. The symmetric arithmetic failure: cascading "excess" slash from
one withdrawal bucket into the next without verifying the destination
can absorb it causes underflow / revert and blocks the slash entirely
[cites: solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-1-2].

### V9: Slashing-related accounting forgotten on the recovery side

When slashed funds are restored from operator-collateral, the
`rewardStakeRatioSum` / `latestActiveBalanceAfterFee` accumulators must
be credited back; failing to do so leads to a permanent underflow that
freezes report finalisation and prevents new validators from being
activated [cites: solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-0-11].
Same family: `minimumContractBalance` decremented by deposit amount
rather than redemption amount after a partial slash, eventually
underflowing on the next legitimate redemption [cites:
solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-1-0].

### V10: Commit-reveal slashing bypass via unrelated account input

A commit-reveal designed to delay slashing rewards lets the slasher
commit with `(arbitraryAccount, hash(secret, reward))`; the
delay/timestamp is keyed on `arbitraryAccount` (which has none), so the
reveal is instant. The `account` parameter is never bound to the secret
[cites: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-1-2]. Fix: bind
the slashed account into the commitment.

### V11: Penalty bypass via partial-stake reduction or vault migration

Leave penalties computed as a percentage of *current* stake can be
shrunk by first calling `reduceStakeTo(minimum)` before `forceUnstake`,
paying 10% of the floor instead of the original deposit
[cites: solodit-cyfrin-2023-11-03-cyfrin-streamr-1-2]. Same family:
calling `leave()` to clean accounting and then `migrateToVault()` from
a freshly registered empty vault into the locked vault resets
`lockUntil = 0`, allowing immediate withdrawal of stake that was
nominally locked for 4 years — and earning the 6× boosted reward in
the meantime [cites:
solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-1-4].

### V12: Unbonding queue: uneven distribution, discount-factor bypass, forced exits

`PolygonStrategy::unbond` advanced `validatorWithdrawalIndex` on every
loop iteration, even when only rewards (not principal) were drained,
letting reward-rich validators "shield" their principal and pushing the
unbonding burden onto poorer validators [cites:
solodit-cyfrin-2025-05-19-cyfrin-stakedotlink-polygon-staking-v2-0-0-0].
On the claim side, Lido's withdrawal queue compared `_hint + 1`'s
`fromId` against `_hint` itself instead of `_requestId`, letting a
user pick any past checkpoint with a better discount factor and claim
full principal — stealing from other queued requests
[cites: solodit-hexens-2023-04-14-lido-0-0]. And on the request side,
`requestUnstake` priced expected withdrawable balance against the
prevailing state, letting an attacker stake 1 ETH then immediately
request 1 ETH back to force a 32 ETH validator exit, repeatedly
griefing operators [cites: solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-0-8].
The Cosmos-side analogue: `LiquidUnstake` allowed
`totalUnbondingAmount > totalLiquidTokens` because the NAV used unclaimed
rewards in the numerator [cites: solodit-hexens-2024-01-12-persistence-2-2].

### V13: Mass-slashing perverse incentive

When slashing penalties scale with the fraction of validators slashed
in a window (Ethereum's correlated-slashing penalty), a node operator
sandwiched between a mass slash and the threshold can voluntarily get
slashed, exit with `< 16 ETH`, and have the OptimisticWithdrawalRecipient
mis-classify the withdrawal as *rewards*, stealing from principal
[cites: solodit-zachobront-2023-09-01-obol-0-2]. Worth flagging during
audits of any contract that treats "small withdrawal" as a reward.

### V14: Reward-distribution / mint logic abused via attacker-controlled inputs

Reward systems that mint or distribute based on *trades against any
registered token* (without restricting to canonical pools) are an
infinite-mint primitive. BetterBank let anyone create a PulseX LP
against the registered FAVOR token, swap through it, and harvest the
bonus mint with zero tax — $5M drained [cites: rekt-betterbank-rekt].
Reward accumulators that key off `(sender, receiver)` pairs without
sanity-checking self-transfers create echo loops: The Idols NFT lost
97 stETH because `_beforeTokenTransfer` would delete
`claimedSnapshots[sender]` before claiming, when sender == receiver and
balance == 1 [cites: rekt-theidolsnft-rekt]. The most catastrophic
expression of this class is upgrade-key compromise on a reward-bearing
LST: the Ankr deployer was phished and the upgraded aBNBc allowed
unlimited mint, draining $24M of liquidity across the dependent
Helio collateral [cites: rekt-ankr-helio-rekt].

## Audit checklist

Use these as concrete YES/NO questions while reading staking code.

**Exchange-rate / share-price integrity**

- When `totalSupply == 0`, does the contract reset its
  `highest-ever` / `stored` exchange rate to 1:1, or does it remember
  the prior high? [V1]
- Is there a permanent minimum share supply (dead-shares to address(0)
  or virtual-share offset) so the share price cannot be ratcheted by
  unstake-to-zero?
- Does `getExchangeRate()` consume any input the attacker controls
  (donated balance, claimable-but-unclaimed rewards, `totalAssets()`
  off-chain reads)?

**Snapshot / checkpoint correctness**

- Can `calcAndCacheStakes(epoch)` be called with `epoch > currentEpoch`?
  If yes, does the cached value get committed and never re-derived?
  [V2]
- Are `wasActiveAt(enabled, disabled, ts)` boundaries `<` / `>` (strict)
  rather than `<=` / `>=`? [V3]
- Is the reward-distribution delay `< slashing/removal window`, so
  legitimate-during-epoch-N operators can be purged before their epoch N
  rewards are paid? [V3]
- Is voting/reward weight derived from a balance and a time-weight from
  *consistent* snapshots (both current or both prior-period)? [V5]

**Stake-locking / per-operator capacity**

- Does any function that consumes operator capacity (`addNode`,
  `delegate`, `allocate`) update the corresponding `locked` /
  `consumed` counter atomically before returning? [V4]
- Is there a separate ceiling enforcing total per-operator allocations
  ≤ collateral?

**Reward accumulator update ordering**

- Does *every* function that mutates a user's effective weight
  (balance, lock, boost, delegation, multiplier) call the standard
  `updateReward(account)` hook *before* the mutation? [V5]
- If extra rewarders / sub-distributors can be added or removed, does
  removal block users from calling `earned()` against the removed
  rewarder, or is unclaimed value drained via withdraw-then-stake?
  [V5]

**Precision / dust / division**

- Is `ACC_PRECISION` (or equivalent reward-per-share scaler) ≥ 1e18 so
  rounding error is ≤ 1 wei? [V6]
- If reward accrual depends on `block.timestamp`, does `notifyReward` /
  `update` *not* advance `lastUpdateTime` when `totalStaked == 0`?
  [V6]
- Is any integer division applied to a quantity that is later compared
  against a threshold (e.g. `minRequiredUptime`)? Can truncation push
  the user below the threshold? [V6]

**Slashing soundness**

- Does `_slash()` iterate over any set the slashed user can extend
  (vaults, positions, sub-accounts, distributors)? Is there a hard cap?
  [V7]
- Does the slash revert if a sub-distributor / sub-module is paused?
  Is the per-iteration call wrapped in `try/catch` or guarded by
  `isPaused()`? [V7]
- Is a `MIN_SLASH_AMOUNT` floor applied once on the aggregated total,
  not per-bucket? [V8]
- Does cascading "excess" slashing into adjacent buckets check the
  destination can absorb it without underflow? [V8]
- After slashed funds are recovered from operator collateral, are
  reward-accumulator state variables credited back symmetrically?
  [V9]
- Are commit-reveal slashing inputs cryptographically bound to the
  slashed account (account ∈ hash preimage)? [V10]

**Lock & penalty bypass**

- Can a user reduce their effective stake before triggering a
  penalty function so the penalty is calculated on the reduced
  balance? [V11]
- Can `migrate` / `merge` / `consolidate` operations on vaults reset
  `lockUntil`, `depositedBalance`, or `hasLeft` flags? [V11]

**Unbonding queue / withdrawal**

- Does the queue advance its cursor only when actual principal was
  unbonded, not when only rewards were withdrawn? [V12]
- Are `_hint` parameters in checkpoint lookups validated against the
  user-supplied `_requestId`, not against the hint itself? [V12]
- Can `requestUnstake` force a validator exit on every call, given a
  minimal deposit, with no per-deposit cooldown? [V12]
- Does the NAV calculation feeding unbonding amount include unclaimed
  rewards that may not be liquid, leading to
  `totalUnbonding > totalLiquid`? [V12]

**Mass-slashing / classifier edge cases**

- Does any "is this a reward vs principal?" heuristic (e.g. balance
  threshold) hold under correlated mass slashing? [V13]

**Reward-mint / accumulator gating**

- Can rewards be minted in response to trades against any user-
  registered LP, or only against protocol-blessed pools? [V14]
- Does any reward-distribution branch trigger when `sender == receiver`
  or other degenerate cases? [V14]
- For upgradeable LSTs / reward tokens, is the upgrade key behind a
  timelock + multisig, given that infinite-mint via upgrade is the
  highest-impact class? [V14]

## Prior incidents

- **Ankr & Helio (2022-12) — $24M (plus 60T aBNBc theoretical)**: deployer
  private key compromised; malicious upgrade of the reward-bearing LST
  added an unrestricted mint function; depegged aBNBc was then used as
  collateral on Helio to drain $19M more [cites: rekt-ankr-helio-rekt].
- **The Idols NFT (2025-01) — $324k / 97 stETH**: `_beforeTokenTransfer`
  deleted `claimedSnapshots[sender]` before re-claiming the same reward
  on self-transfers with balance == 1, enabling an infinite-reward
  echo loop [cites: rekt-theidolsnft-rekt].
- **BetterBank on PulseChain (2025-08) — $5M**: bonus-mint logic paid
  out free ESTEEM for any swap involving the registered FAVOR token;
  attacker built their own LP with a worthless token, swapped through
  it, and dumped the mint — exact vector Zokyo had flagged and the
  team had downgraded to "Low" [cites: rekt-betterbank-rekt].
- **Lido withdrawal queue (2023-04) — pre-exploit fix, full-loss
  potential**: `_hint + 1` checkpoint comparison against `_hint` rather
  than `_requestId` would have let any claimant pick a checkpoint with
  no discount factor and steal queued ETH from other users [cites:
  solodit-hexens-2023-04-14-lido-0-0].
- **StatusL2 staking (2026-01) — pre-launch criticals**: any staker
  could spam vault registrations to OOG the slash loop and become
  un-slashable; in the same audit a `leave + migrate` chain reset
  `lockUntil` to bypass 4-year locks while keeping 6× boosted rewards
  [cites: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-0-0;
  solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-1-4].
- **Suzaku middleware (2025-07) — multiple pre-launch H/M**: future-
  epoch cache poisoning, inclusive boundary on disabled-time, missing
  per-operator stake locking on `addNode`, dust-limit DoS of
  `forceUpdateNodes`, and slash-cascade underflow — a near-complete
  catalogue of the V2/V3/V4/V7/V8 classes in one codebase [cites:
  solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-0-1;
  solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-0-6;
  solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-1-17;
  solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-0-0;
  solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-1-2].

## References

Core corpus entries grouped by sub-pattern (all in `derives_from`):

Reward-accumulator update ordering & precision:
`solodit-cyfrin-2025-10-21-cyfrin-illuvium-stakingv3-v2-0-0-2`,
`solodit-hans-2023-07-13-meta-0-1`,
`solodit-hexens-2024-07-22-tokemak-1-3`,
`solodit-0x52-2024-03-27-blueberry-staking-1-2`,
`solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-1-16`,
`solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-1-7`.

Exchange-rate / share-price / snapshot manipulation:
`solodit-hexens-2025-05-26-zealous-1-1`,
`solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-0-1`,
`solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-0-6`,
`solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-1-17`,
`solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-1-11`.

Slashing arithmetic, DoS, bypass:
`solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-0-0`,
`solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-2-1`,
`solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-2-7`,
`solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-1-2`,
`solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-1-0`,
`solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-1-4`,
`solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-0-11`,
`solodit-zachobront-2023-09-01-obol-0-2`,
`solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-1-2`,
`solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-1-0`,
`solodit-cyfrin-2023-11-03-cyfrin-streamr-1-2`.

Unbonding / withdrawal queue:
`solodit-cyfrin-2025-05-19-cyfrin-stakedotlink-polygon-staking-v2-0-0-0`,
`solodit-hexens-2024-01-12-persistence-2-2`,
`solodit-hexens-2023-04-14-lido-0-0`,
`solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-0-8`,
`solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-0-0`.

Historical incidents (rekt post-mortems):
`rekt-theidolsnft-rekt`, `rekt-betterbank-rekt`, `rekt-ankr-helio-rekt`.

Academic survey (taxonomy of logical defects in DeFi staking):
`arxiv-2601.05827`.
