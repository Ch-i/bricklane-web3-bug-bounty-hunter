---
id: synthesis-delegation-voting-power-math
source: synthesis
source_url: null
title: "Delegation & Voting Power Math: pattern, variants, audit checklist"
ingested_at: 2026-06-04T21:09:46+00:00
vuln_class:
  - governance
  - accounting
  - flash-loan
  - reentrancy
  - precision-loss
  - access-control
protocol_category:
  - governance
  - dao
  - staking
tags:
  - synthesis
  - delegation
  - voting-power
  - checkpoint
  - snapshot
  - quorum
derives_from:
  - solodit-cyfrin-2025-09-05-cyfrin-wlf-v2-1-0-4
  - solodit-cyfrin-2025-09-05-cyfrin-wlf-v2-1-0-3
  - solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-2-0
  - solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-0-1
  - solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-0-2
  - solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-1-4
  - solodit-cyfrin-2023-11-10-cyfrin-dexe-0-1
  - solodit-cyfrin-2023-11-10-cyfrin-dexe-0-6
  - solodit-cyfrin-2023-11-10-cyfrin-dexe-0-11
  - solodit-cyfrin-2023-11-10-cyfrin-dexe-1-7
  - solodit-cyfrin-2023-11-10-cyfrin-dexe-2-0
  - solodit-cyfrin-2024-09-27-cyfrin-bima-v2-0-1-0
  - solodit-cyfrin-2025-09-04-cyfrin-symbiotic-v2-0-0-0
  - solodit-hexens-2022-11-04-1inch-0-0
  - rekt-beanstalk-rekt
  - arxiv-2604.25959
---

# Delegation & Voting Power Math

## Pattern

Token-weighted governance rests on one deceptively simple equation: at a
given point in time, *how much voting power does an account control?* In
practice that number is the output of a stack of bookkeeping —
per-account balance checkpoints, delegation checkpoints, a total-supply
checkpoint used as the quorum denominator, and any custom adjustments for
vesting, exclusion, blacklisting, NFT power, or oracle-priced stake. Bugs
in delegation & voting-power math are the gap between what the protocol
*thinks* an account can vote and what it *actually* can. When that gap is
attacker-controllable, it lets a malicious party manufacture, double, or
relocate voting power; when it is merely inconsistent, it produces wrong
quorum decisions, locked funds, or disenfranchised voters.

The canonical implementation (OpenZeppelin `ERC20Votes` /
`GovernorVotes`) reads weight from a historical snapshot:
`Governor._castVote` calls `_getVotes(account, proposalSnapshot)` which
calls `token.getPastVotes(account, timepoint)`, and quorum is computed
against `getPastTotalSupply(timepoint)`. Two structural properties make
this safe: weight is read *as of a past block*, so power must be held
before the proposal snapshot, and delegation is tracked with checkpoints
so the historical value cannot be retroactively changed. Every variant
below is a way that one of those properties is broken — by overriding
`getVotes` but not `getPastVotes`, by letting the total-supply checkpoint
drift from the real eligible supply, by double-counting a delegatee's own
balance, by acquiring power inside the same transaction as the vote, or by
corrupting the checkpoint arithmetic with downcasts and reentrancy.

A second, structural lens (arxiv-2604.25959) is that the very mechanisms
introduced to make delegation "work" — token registration, staking, and
delegation — systematically concentrate voting power in a small set of
addresses. An auditor should treat voting-power math not only as a
correctness problem but as an *adversarial* one: assume a whale or a
flash-borrower will try to make the math produce the largest number it
legally can, and that a delegate will try to make it produce a number it
should not.

## Variants

### V1: Snapshot/live inconsistency — `getVotes` overridden, `getPastVotes` not

A protocol customizes `getVotes` (e.g. to add vested tokens and to zero
out blacklisted/excluded accounts) but leaves `getPastVotes` — the
function the Governor actually uses for vote weight — on the default
implementation. The UI shows one number; the on-chain tally uses another,
and blacklisted/excluded accounts retain real voting power because the
historical path never learned about the exclusion. The fix is to override
*both* read paths consistently. (`...wlf-v2-1-0-4`)

### V2: Quorum-denominator drift — checkpointed total supply ≠ eligible supply

Quorum is computed against a total-supply figure that diverges from the
truly eligible supply. In Status/Karma, `ERC20VotesUpgradeable` checkpoints
total supply by bumping it on every `_mint`/`_burn`, but the token's real
`totalSupply()` subtracts undistributed reward-distributor balances, so
`getPastTotalSupply` *overestimates* the denominator and quorum is wrong
(`...statusl2-v2-0-2-0`). In DeXe, the quorum denominator adds
`_nftInfo.totalPowerInTokens`, a value set once at initialization; when
ERC721 NFT power decays to zero the denominator stays inflated and quorum
can become *impossible to reach* (`...dexe-0-11`). Any static or
stale value in the quorum denominator is suspect.

### V3: Double-counting & self-delegation accounting

Delegation cycles and mishandled self-delegation corrupt the per-account
math. In TempleDAO, `getDelegatedVoteWeight` adds the delegatee's own
`ownVoteWeight` on top of delegated balances; with a cycle (Alice→Bob,
Bob→Alice) both balances are counted twice, doubling power
(`...templedao-v2-1-0-1`). Separately, resetting self-delegation is not
revalidated across state changes: it can underflow (subtracting a
delegated balance from zero) and be abused to accumulate *infinite*
voting power via repeated stake/redelegate/withdraw cycles
(`...templedao-v2-1-0-2`), or it can wrongly reset a delegate's stake-time
to zero and wipe out legitimate voting power (`...templedao-v2-1-1-4`).

### V4: Flash-acquired voting power (snapshot timing)

If voting power is measured at a timepoint an attacker can satisfy *within
the voting transaction*, governance can be hijacked with a flash loan:
borrow tokens → deposit/stake → (delegate) → vote to quorum → undelegate /
withdraw → repay, all atomically. This is the Beanstalk class
(`rekt-beanstalk-rekt`). DeXe shows the delegation twist: even when direct
flash-vote mitigations exist, an attacker routes the borrowed power through
*delegation* to a slave contract, votes the proposal into the Locked
state, then undelegates and withdraws while still locked — bypassing the
mitigation in one transaction (`...dexe-0-1`). The defense is a real
past-block snapshot plus an execution delay between snapshot and execution.

### V5: Delegation as an authorization bypass

Delegation moves the *exercise* of voting power to a different address,
which silently defeats per-account restrictions. In DeXe a user barred
from a specific proposal delegates to a controlled "slave" address that
votes the borrowed power, bypassing the restriction (`...dexe-0-6`). In
WLFI an account explicitly *excluded* from voting power re-gains it simply
by re-delegating to another address (whose `getVotes` reads the delegation
checkpoint that now includes the excluded balance) or by transferring the
tokens to a fresh address — because `_delegate` and `_update` (transfer)
are not gated by the exclusion check the way they are for blacklisting
(`...wlf-v2-1-0-3`). Exclusion/restriction must be enforced on *every*
path that can relocate power: delegate, transfer, and the historical read.

### V6: Multi-tier delegation not flowing through

When delegation chains are allowed but the re-vote logic only follows one
hop, delegated votes get silently lost. In DeXe, `revoteDelegated()` does
not propagate through multiple tiers: if A delegates to B and B has
delegated to C, A's votes never reach C, so the final voter's tally is
short (`...dexe-1-7`). The accounting must either follow the chain to the
terminal voter or forbid chained delegation outright.

### V7: Integer downcast / overflow in checkpoint math

Checkpoint and lock structs frequently pack balances or snapshot IDs into
small integer types, and an unchecked downcast silently truncates. DeXe
downcasts a `uint256` to `uint56` for a proposal `snapshotId`, which on
overflow yields an incorrect snapshot and wrong validator voting power
(`...dexe-2-0`). Bima stores `locked/unlocked/frozen` lock balances as
`uint32` and downcasts the deposited amount into `uint32`, so large locks
overflow and users get back far fewer (or zero) tokens than they locked —
a direct loss of locked voting tokens (`...bima-v2-0-1-0`). Every cast into
a narrower type in vote-power code should go through `SafeCast`.

### V8: Reentrancy corrupting delegation balances

Delegation updates done inside ERC20 transfer hooks can be reentered to
double-mint delegation. In 1inch's `ERC20Pods`, `_beforeTokenTransfer`
reads the sender's and receiver's pod arrays then calls
`pod.updateBalances`; a malicious `from` pod reenters `addPod` mid-loop,
mutating the `_pods` mapping so the hook double-mints delegation to `to`.
Both parties end up with valid delegation that should have moved only once
(`...1inch-0-0`). Delegation bookkeeping in hooks must be reentrancy-safe
and must not trust array snapshots taken before an external call.

### V9: Derived voting power that fails open to zero

When voting power is computed from an external input (price oracle, stake
conversion), silent failure skews outcomes. Symbiotic's
`PricedTokensChainlinkVPCalc.stakeToVotingPowerAt` multiplies stake by an
oracle price, and the price feed returns `0` on stale/failed data instead
of reverting — so an operator with active stake silently loses *all*
voting power at the vote timestamp (`...symbiotic-v2-0-0-0`). Derived
voting-power calculations should fail closed (revert) rather than return
zero.

## Audit checklist

- Are `getVotes` and `getPastVotes` (plus any custom overrides for
  vesting/exclusion/blacklist) implemented consistently, and does the
  Governor read the *same* source the UI displays? (V1)
- After an account is excluded or blacklisted, can it re-acquire voting
  power by re-delegating or by transferring tokens to a fresh address? Are
  `_delegate` and `_update`/transfer gated by the same check as
  blacklisting? (V5)
- Does the checkpointed `totalSupply` used as the quorum denominator match
  the actually eligible/circulating supply (undistributed tokens, excluded
  balances)? (V2)
- Is any quorum/denominator term set once at initialization and never
  updated as voting power decays (e.g. NFT power → 0)? (V2)
- Can a delegatee's own balance be double-counted with delegated balances
  via delegation cycles or by adding `ownVoteWeight` on top of delegated
  weight? (V3)
- Is self-delegation reset revalidated on stake/withdraw/redelegate so it
  cannot underflow (subtract from zero) or wrongly zero a delegate's
  stake-time? (V3)
- Can voting power be acquired and exercised in the same transaction
  (flash loan → deposit/stake → delegate → vote → undelegate → withdraw)?
  Do flash-loan mitigations also cover the *delegation* path, not just
  direct voting? (V4)
- Is there an enforced delay between the proposal snapshot and execution so
  flash-acquired power cannot immediately execute a proposal? (V4)
- Can a restricted account route votes through a delegatee/"slave" address
  to bypass per-account voting restrictions? (V5)
- Do multi-tier delegations propagate to the terminal voter, or is chained
  delegation forbidden so votes are not silently lost? (V6)
- Are all downcasts of balances and snapshot IDs into narrower integer
  types performed with `SafeCast` so overflow reverts? (V7)
- Are delegation balance updates inside transfer hooks reentrancy-safe, and
  do they avoid trusting array/state snapshots taken before an external
  call? (V8)
- Does any oracle- or price-derived voting-power calculation fail closed
  (revert on stale/failed data) instead of silently returning zero? (V9)

## Prior incidents

- **Beanstalk (April 17, 2022) — $181,000,000**: An attacker used a flash
  loan to temporarily acquire a supermajority of voting power and execute a
  malicious emergency governance proposal that drained the protocol; made
  possible by flash-acquirable power *and* the absence of an execution
  delay. [cites: rekt-beanstalk-rekt]

Audit-caught cases (found pre-deployment, not exploited) that demonstrate
the same math failures:

- **DeXe Protocol (Cyfrin, Nov 2023)**: flash loan combined with delegated
  voting to decide a proposal and withdraw while locked; delegation used to
  bypass voting restrictions; static NFT power inflating the quorum
  denominator; unsafe `uint56` snapshot downcast. [cites:
  solodit-cyfrin-2023-11-10-cyfrin-dexe-0-1,
  solodit-cyfrin-2023-11-10-cyfrin-dexe-0-6,
  solodit-cyfrin-2023-11-10-cyfrin-dexe-0-11,
  solodit-cyfrin-2023-11-10-cyfrin-dexe-2-0]
- **TempleDAO v2.1 (Cyfrin, Jun 2024)**: delegation cycles double voting
  power; self-delegation reset enabling infinite power or zeroed weight.
  [cites: solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-0-1,
  solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-0-2]
- **WLFI v2.1 (Cyfrin, Sep 2025)**: `getPastVotes` not overridden;
  excluded accounts re-gaining power via delegation/transfer. [cites:
  solodit-cyfrin-2025-09-05-cyfrin-wlf-v2-1-0-4,
  solodit-cyfrin-2025-09-05-cyfrin-wlf-v2-1-0-3]
- **Status L2 / Karma (Cyfrin, Jan 2026)**: `getPastTotalSupply`
  overestimates the quorum denominator. [cites:
  solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-2-0]
- **1inch ERC20Pods (Hexens, Nov 2022)**: cross-function reentrancy in the
  transfer hook double-mints delegation. [cites:
  solodit-hexens-2022-11-04-1inch-0-0]

## References

- corpus entries:
  - solodit-cyfrin-2025-09-05-cyfrin-wlf-v2-1-0-4 — `getPastVotes` not overridden; inconsistent voting power
  - solodit-cyfrin-2025-09-05-cyfrin-wlf-v2-1-0-3 — excluded accounts re-gain power via delegation/transfer
  - solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-2-0 — `getPastTotalSupply` overestimates quorum denominator
  - solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-0-1 — delegation cycle doubles voting power
  - solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-0-2 — self-delegation reset → infinite power / underflow
  - solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-1-4 — self-delegation reset zeroes vote weight
  - solodit-cyfrin-2023-11-10-cyfrin-dexe-0-1 — flash loan + delegated voting bypass
  - solodit-cyfrin-2023-11-10-cyfrin-dexe-0-6 — delegation bypasses per-proposal voting restriction
  - solodit-cyfrin-2023-11-10-cyfrin-dexe-0-11 — static NFT power inflates quorum denominator
  - solodit-cyfrin-2023-11-10-cyfrin-dexe-1-7 — multi-tier delegation votes not propagated
  - solodit-cyfrin-2023-11-10-cyfrin-dexe-2-0 — unsafe `uint56` snapshotId downcast
  - solodit-cyfrin-2024-09-27-cyfrin-bima-v2-0-1-0 — `uint32` downcast overflow loses locked voting tokens
  - solodit-cyfrin-2025-09-04-cyfrin-symbiotic-v2-0-0-0 — oracle-derived voting power silently returns zero
  - solodit-hexens-2022-11-04-1inch-0-0 — reentrancy double-mints delegation
  - rekt-beanstalk-rekt — flash-loan governance takeover ($181M)
  - arxiv-2604.25959 — registration/staking/delegation systematically centralize voting power
