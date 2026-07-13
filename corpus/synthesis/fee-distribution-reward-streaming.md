---
id: synthesis-fee-distribution-reward-streaming
source: synthesis
source_url: null
title: "Fee Distribution & Reward Streaming: pattern, variants, audit checklist"
ingested_at: 2026-06-04T00:00:00Z
vuln_class:
  - accounting
  - rounding
  - reentrancy
  - dos
  - mev
  - front-running
  - access-control
protocol_category:
  - staking
  - yield
  - dex
  - tokenomics
tags:
  - synthesis
  - fee-distribution
  - reward-streaming
  - staking-rewards
  - dividends
  - reward-per-share
derives_from:
  - solodit-trust-security-2023-02-24-satin-exchange-1-3
  - solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-0-6
  - solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-3-8
  - solodit-cyfrin-2025-09-05-cyfrin-stbl-v2-0-0-2
  - solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-0-6
  - solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-1-10
  - solodit-guardian-audits-2022-05-21-bridges-1-4
  - solodit-guardian-audits-2022-05-21-bridges-1-1
  - solodit-hexens-2024-07-22-tokemak-1-1
  - solodit-0x52-2024-03-27-blueberry-staking-1-2
  - solodit-hexens-2025-02-03-rush-trading-2-0
  - solodit-trust-security-2023-01-08-ninja-yield-farming-v3-1-4
  - solodit-hexens-2024-09-19-stakewise-1-1
  - solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-1-2
  - solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-2-0
  - solodit-pashov-audit-group-2023-06-01-topiastaking-0-0
  - solodit-cyfrin-2025-10-21-cyfrin-illuvium-stakingv3-v2-0-0-0
  - solodit-cyfrin-2025-11-17-cyfrin-remora-final-v2-0-0-0
  - solodit-zokyo-2022-06-15-fndz-0-0
  - solodit-zokyo-2024-04-11-zap-2-11
  - solodit-zokyo-2024-03-25-stratis-0-0
  - rekt-safedollar-rekt
  - rekt-bent-finance
  - swc-128
  - swc-101
---

# Fee Distribution & Reward Streaming

## Pattern

Most DeFi protocols that share protocol fees, emissions, or yield with
participants converge on the same accounting trick: instead of looping over
every holder to pay them (which does not scale), they maintain a single
monotonically-increasing global accumulator — `accRewardPerShare`,
`rewardPerToken`, `rewardIndex`, `cumulativeFeePerShare`,
`dividendsPerShare` — that records the cumulative reward owed *per unit of
stake* since inception. A user's claimable balance is then
`stake * (globalAccumulator - userCheckpoint)`, where `userCheckpoint`
(`userRewardPerTokenPaid`, `rewardDebt`, `lastPayoutIndex`) is the value of
the accumulator the last time that user's position changed. "Streaming"
rewards add a time dimension: the accumulator grows by
`rewardRate * elapsedSeconds / totalSupply` on every interaction, where
`rewardRate` is funded by `notifyRewardAmount`-style deposits that distribute
a lump sum over a fixed `DURATION`.

This design is correct in the steady state but is extremely sensitive at its
edges, and almost every bug in the class is an edge-case in one of four
quantities: **the accumulator itself** (overflow, manipulation via a moving
token balance, stale reads), **`totalSupply`/`totalStake` in the denominator**
(zero supply, inflated by not-yet-removed positions), **`elapsedTime`/the
distribution window** (rate dilution, lost emissions while supply is zero,
per-second truncation), and **the checkpoint update ordering** (reentrancy and
front-running of the snapshot). Because reward math is "off to the side" of the
core token transfers, it is frequently under-tested and the rounding direction
is rarely chosen deliberately.

The attacker's leverage comes from the fact that distribution is usually
**proportional to an instantaneous balance at distribution time** rather than
time-weighted. If voting/holding power for a payout can be acquired in the same
block the payout is computed — by depositing right before a public
`distribute*` call, or even with a flash loan — an attacker captures a slice of
rewards that long-term participants funded, then exits. The defender's job is
to make reward eligibility a function of *duration held*, not *balance at a
snapshot an adversary can predict and straddle*.

## Variants

### V1: Reward-per-share accumulator manipulation

The accumulator is derived from a token balance the attacker can move. In
**SafeDollar**, the staking pool incentivised a fee-on-transfer token (`PLX`);
on withdrawal the transfer fee was deducted from the *rewarder's* balance
instead of the user's. A deposit/withdraw loop (101 txs) gradually depleted the
pool balance, which inflated `accSdoPerShare` to ~1.14e18 SDO per token, after
which a single claim minted ~8.3e17 SDO. The general rule: any accumulator
computed from `token.balanceOf(this)` or any externally-mutable quantity is an
oracle the attacker controls. A degenerate sibling is unbounded growth —
**Ninja Yield Farming** stored `accRewardPerShare` in `uint128`; continuous
incrementation can overflow and freeze withdrawals (see SWC-101).

### V2: Snapshot / "dividend sniping" timing manipulation

Distribution is proportional to balance at the moment a public `distribute*`
function runs, and that moment is observable. In **Bridges (GG-5)** bots
front-run `distributeDividends`, sandwiching a deposit + withdrawal around the
call to collect dividends without ever really holding the token. **Deriverse**
allocates dividends on a predictable hourly cadence to whoever has deposited
DRVS at allocation time — an attacker can deposit (or flash-loan/borrow/swap
into DRVS) immediately before allocation, claim, and withdraw in one
transaction. **STBL** distributes 30-day yield proportional to stake regardless
of deposit duration, letting an MEV searcher deposit just before
`distributeYield` (whose size is driven by an oracle price update) and steal
accrued rewards from earlier depositors.

### V3: Rounding & precision loss in per-second streaming

Per-second `rewardRate` math truncates. In **TopiaStaking** the formula
`(unaccountedTime * rate) / totalWeight` rounds to zero once `totalWeight`
(18-decimal) outgrows `rate * seconds`, permanently freezing accrual at ~0
rewards. **TempleDAO** distributes over 604800 seconds, so a remainder
`< 604800 wei` is stranded each round (recommendation: roll dust into the next
period). **Stratis** loses `wei` on `amount / totalRegistrations`, breaking the
invariant "claimed == funded". **StakeWise** uses `Math.Rounding.Floor` in
`mintShares`/`cumulativeFeePerShare`, consistently rounding *in the user's
favour* and under-crediting the treasury — rounding direction must favour the
protocol.

### V4: Lost or stuck rewards when totalSupply == 0

Streaming contracts special-case an empty pool to avoid divide-by-zero by
returning early in `rewardPerToken()` — but if `lastUpdateTime` is still
advanced, the rewards that "streamed" while supply was zero become unbacked and
stuck. **Rush Trading** and **Blueberry Staking** both lose the emissions
accrued before the first deposit (timestamp advances while no one can be
credited). **Illuvium** transfers ILV to the vault and then calls
`notifyRewardAmount`, which returns early when `totalStaked == 0`, leaving the
ILV un-accounted with no sweep. The mirror image is **Tokemak**: `lastUpdateBlock`
is *not* advanced while supply is zero, so the first staker, after staking,
re-triggers `_updateReward()` and harvests all `elapsed * rewardRate` accrued
before they existed.

### V5: Reward dilution via rate/window extension or stake inflation

`notifyRewardAmount` typically resets `periodFinish = now + DURATION`. In
**Satin Exchange** anyone could call it with a reward of `1`, repeatedly
extending the window and dragging rewards-per-second toward zero
(`periodFinish[token] = block.timestamp + DURATION`); fix was to permission the
caller. **Suzaku** dilutes from the denominator side: a `>=` vs `>` boundary in
`_wasActiveAt` counts an operator as active at the exact timestamp it was
disabled, so `calcAndCacheStakes` returns an inflated `totalStake` and active
operators are under-paid.

### V6: Denial of service of distribution

**Bridges (GG-1)** loops over an unbounded `usersBridges` array in
`distributeDividends`; an attacker registers many addresses with dust LP until
the loop exceeds the block gas limit and all dividends halt (classic SWC-128;
fix was a `pointsPerShare`/`dividendsPerShare` pull model). **Suzaku** lets
`REWARDS_MANAGER_ROLE` set per-asset-class shares and protocol/operator/curator
fees without checking the *cumulative* total ≤ 100%, enabling over-allocation,
insolvency, and DoS for later claimers. **TempleDAO** shares one
`lastRewardNotificationTimestamp` between the privileged `distributeRewards` and
the public `distributeGold`; front-running `distributeGold` keeps resetting the
cooldown and can block reward-rate updates indefinitely.

### V7: Reentrancy / double-claim on the claim path

Claim functions that make an external call (token transfer, swap with a
user-supplied route) before writing the claim checkpoint allow re-entry. **FNDZ**
swaps rewards via a user-supplied Uniswap path and updates `stakeUpdatedAt` /
`hasEarnedRewards` *after* the call — a malicious token in the route re-enters
and claims multiple times. **Zap** similarly does the external value transfer in
`claim()` before its state/balance updates. A related double-spend is **Remora**:
`seizeFrozenFunds` redirects a frozen holder's dividends to a custodian, but a
later distribution plus a `payoutBalance` call resets
`lastPayoutIndexCalculated` to `frozenIndex`, letting the unfrozen holder
re-claim the already-seized period.

### V8: Privileged / out-of-band balance manipulation

Even with sound math, an admin path that can write balances directly poisons
the accumulator. In **Bent Finance** the cvxCRV contract was updated to manually
adjust the exploiter's balance, assigning rewards exceeding the protocol's whole
TVL (~$1.75M drained, suspected inside job). Any function that can set staked
balance or reward debt outside normal deposit/withdraw is a reward-theft
primitive.

## Audit checklist

- Is the reward-per-share accumulator derived from a balance an actor can move
  in-transaction (e.g. `token.balanceOf(this)`), and is the staked token
  fee-on-transfer or rebasing? (SafeDollar)
- Is the accumulator width large enough to never overflow over the contract's
  lifetime (avoid `uint128` for `accRewardPerShare`)? (Ninja, SWC-101)
- Is payout proportional to balance *at a public distribution moment* rather
  than time-weighted, allowing deposit-before / withdraw-after sniping? Can the
  whole deposit→trigger→claim→withdraw loop run in one transaction or via a
  flash loan? (Bridges GG-5, Deriverse, STBL)
- Is there a warmup / lock / minimum-hold-duration before deposited stake is
  eligible for the next distribution? (Bridges GG-5, Deriverse)
- Does per-second `rate * elapsed / totalSupply` round to zero for realistic
  `totalSupply`/`rate`, and is leftover dust carried into the next period?
  (TopiaStaking, TempleDAO dust, Stratis)
- Is every rounding direction chosen to favour the protocol, not the user, in
  share/fee conversions? (StakeWise)
- When `totalSupply == 0`, is `lastUpdateTime`/`lastRewardBlock` *not* advanced,
  so no emissions are silently stranded, and is there a sweep for tokens sent to
  an empty pool? (Rush, Blueberry, Illuvium)
- Can the first staker capture rewards that accrued before any stake existed by
  toggling `lastUpdateBlock` state? (Tokemak)
- Can `notifyRewardAmount` (or equivalent) be called by anyone to extend
  `periodFinish` / dilute `rewardRate`? Is it access-controlled to the trusted
  distributor? (Satin)
- Do `>=`/`>` boundary conditions in active-at-timestamp checks include
  disabled/expired positions in the reward denominator? (Suzaku)
- Is distribution implemented as an unbounded loop over all users (gas-limit
  DoS), instead of a pull-based `pointsPerShare` model? (Bridges GG-1, SWC-128)
- Are cumulative reward shares / fees validated to sum to ≤ 100% to prevent
  over-allocation and later-claimer insolvency? (Suzaku 1-10)
- Does any public function share a state variable (e.g. last-distribution
  timestamp) with the privileged distributor such that front-running it can
  block distribution? (TempleDAO distributeGold)
- Is the user's claim checkpoint written *before* any external call/transfer/
  swap in the claim path (CEI)? (FNDZ, Zap)
- After a seizure/freeze, can index resets let a holder re-claim an
  already-redirected distribution period? (Remora)
- Are there privileged functions that can set staked balances or reward debt
  directly, bypassing deposit/withdraw accounting? (Bent Finance)

## Prior incidents

- **SafeDollar (2021-06-28) — $248k**: a fee-on-transfer reward token let a
  deposit/withdraw loop deplete the pool balance and inflate `accSdoPerShare`,
  enabling an effectively infinite reward claim. [cites: rekt-safedollar-rekt]
- **Bent Finance (2021-12-21) — ~$1.75M**: the cvxCRV contract was updated to
  manually adjust an address's balance, assigning rewards exceeding the
  protocol's TVL; suspected inside job, laundered via Tornado Cash.
  [cites: rekt-bent-finance]

## References

- corpus entries:
  - solodit-trust-security-2023-02-24-satin-exchange-1-3 — reward-per-second dilution via repeated `notifyRewardAmount` window extension
  - solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-0-6 — missing `ps==0` check misallocates fees away from dividends
  - solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-3-8 — predictable hourly dividend allocation gamed by deposit/flash-loan before allocation
  - solodit-cyfrin-2025-09-05-cyfrin-stbl-v2-0-0-2 — front-running 30-day yield distribution to steal accrued rewards
  - solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-0-6 — `>=` boundary includes disabled operator stake, diluting active operators
  - solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-1-10 — unchecked cumulative reward share / fee allocation > 100% → DoS/insolvency
  - solodit-guardian-audits-2022-05-21-bridges-1-4 — dividend sniping by sandwiching deposit/withdraw around distribution
  - solodit-guardian-audits-2022-05-21-bridges-1-1 — unbounded loop in `distributeDividends` enables gas-limit DoS
  - solodit-hexens-2024-07-22-tokemak-1-1 — first staker harvests rewards accrued while supply was zero
  - solodit-0x52-2024-03-27-blueberry-staking-1-2 — emissions lost for ibToken with no deposits (timestamp advanced)
  - solodit-hexens-2025-02-03-rush-trading-2-0 — rewards stranded when `totalSupply == 0`
  - solodit-trust-security-2023-01-08-ninja-yield-farming-v3-1-4 — `uint128 accRewardPerShare` overflow freezes withdrawals
  - solodit-hexens-2024-09-19-stakewise-1-1 — `Math.Rounding.Floor` in fee/share math under-credits the treasury
  - solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-1-2 — public `distributeGold` front-run blocks reward-rate distribution via shared timestamp
  - solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-2-0 — per-second streaming leaves sub-`DURATION` dust stuck
  - solodit-pashov-audit-group-2023-06-01-topiastaking-0-0 — `(time*rate)/totalWeight` rounds to zero, freezing accrual
  - solodit-cyfrin-2025-10-21-cyfrin-illuvium-stakingv3-v2-0-0-0 — `notifyRewardAmount` early-returns on empty vault, stranding transferred ILV
  - solodit-cyfrin-2025-11-17-cyfrin-remora-final-v2-0-0-0 — index reset after seizure enables double-claim of seized dividends
  - solodit-zokyo-2022-06-15-fndz-0-0 — reentrancy via user-supplied swap route claims rewards multiple times
  - solodit-zokyo-2024-04-11-zap-2-11 — external transfer before state update in `claim()` reentrancy
  - solodit-zokyo-2024-03-25-stratis-0-0 — `amount / totalRegistrations` truncation breaks claimed==funded invariant
  - rekt-safedollar-rekt — `accSdoPerShare` manipulation via fee-on-transfer token ($248k)
  - rekt-bent-finance — manual reward-balance manipulation / privileged abuse (~$1.75M)
  - swc-128 — DoS with block gas limit (unbounded distribution loops)
  - swc-101 — integer overflow/underflow (reward accumulator overflow)
