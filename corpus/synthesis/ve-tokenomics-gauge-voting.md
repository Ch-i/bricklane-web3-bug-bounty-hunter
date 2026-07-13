---
id: synthesis-ve-tokenomics-gauge-voting
source: synthesis
source_url: null
title: "veTokenomics & Gauge Voting: pattern, variants, audit checklist"
ingested_at: 2026-06-04T00:00:00+00:00
vuln_class:
  - governance
  - flash-loan
  - accounting
  - dos
  - access-control
protocol_category:
  - amm
  - lending
  - governance
tags:
  - synthesis
  - ve-tokenomics
  - gauge-voting
  - bribe-market
derives_from:
  - solodit-zachobront-2023-05-26-stakedao-0-0
  - solodit-zachobront-2023-05-26-stakedao-1-0
  - solodit-trust-security-2023-02-24-satin-exchange-1-5
  - solodit-trust-security-2023-02-24-satin-exchange-0-6
  - solodit-trust-security-2023-02-24-satin-exchange-0-3
  - solodit-trust-security-2023-02-24-satin-exchange-1-3
  - solodit-cyfrin-2025-11-10-cyfrin-benqi-governance-v2-0-1-3
  - solodit-cyfrin-2023-11-10-cyfrin-dexe-0-1
  - solodit-zokyo-2023-06-23-vesync-1-1
  - rekt-beanstalk-rekt
  - rekt-curio-rekt
  - rekt-mango-markets-rekt
  - rekt-atlantis-loans-rekt
  - arxiv-2604.25959
  - swc-128
  - swc-116
---

# veTokenomics & Gauge Voting

## Pattern

The Curve-style "vote-escrow" (ve) design has three coupled layers, and
each layer is its own attack surface. **Layer 1 — the escrow.** Users
lock a governance token (CRV, SATIN, CGT, etc.) into a `VotingEscrow`
for a chosen duration and receive *time-decaying* voting power, modelled
as a linear `bias = slope * (lock_end - now)` that ticks down toward zero
at unlock. The checkpoint math stores `bias`/`slope` as signed integers
and leans on `block.timestamp` as a clock. **Layer 2 — the gauge /
emissions router.** A `GaugeController`/`Voter` lets ve holders vote
weights onto liquidity gauges; every epoch, protocol token emissions are
split across gauges in proportion to votes and streamed to LPs. **Layer 3
— the bribe (incentive) market.** Third parties deposit "bounties" to pay
ve holders who vote for their gauge, so emission direction becomes a
priced, tradeable good.

The recurring bug classes track those layers. In the escrow, unchecked
`int128`/`int256` casts of `bias`/`slope` and timestamp-as-time
assumptions can corrupt voting-power accounting
(`solodit-zokyo-2023-06-23-vesync-1-1`, `swc-116`). In the router, votes
can be cast for pools with no valid gauge (emissions silently lost),
phantom votes can keep flowing to deactivated gauges, double-counted
`claimable` can render the voter insolvent, and an unbounded
loop-over-all-gauges distribution can be DoS'd past the block gas limit
(`solodit-trust-security-2023-02-24-satin-exchange-1-5` / `-0-6` / `-0-3`,
`solodit-cyfrin-2025-11-10-cyfrin-benqi-governance-v2-0-1-3`, `swc-128`).
In the bribe market, a bounty manager can shrink payouts to ~0 *after*
voters are locked in, and anyone can dilute reward-per-second by topping
up a stream (`solodit-zachobront-2023-05-26-stakedao-0-0`,
`solodit-trust-security-2023-02-24-satin-exchange-1-3`).

Cutting across all three layers is the **voting-power-as-leverage**
problem: if voting power can be acquired and exercised without a durable
lock or a flash-resistant snapshot, an attacker can rent it for a single
transaction. Beanstalk, Curio, Mango and Atlantis all turned transient
voting power into protocol control, and the DeXe finding shows that naive
flash-loan guards are bypassable via *delegation*
(`solodit-cyfrin-2023-11-10-cyfrin-dexe-0-1`). Academic measurement of 48
large Ethereum DAOs further finds that the very mechanisms meant to
secure ve governance — token registration, staking, and delegation —
systematically concentrate voting power into a few hands
(`arxiv-2604.25959`), which is the steady-state version of the same
risk: a small set of whales can dictate where emissions go.

An auditor reading ve/gauge code for the first time should treat every
hop — *lock → voting power → gauge weight → emission amount → bribe
payout* — as a place where value can be lost, double-counted, frozen, or
captured, and should always ask whether voting power is durable or
rentable within one block.

## Variants

### V1: Flash-acquired / same-transaction voting power

Voting power that can be obtained and used in the same transaction (or
within one short window) with no real lock collapses ve security.
Beanstalk's attacker flash-loaned hundreds of millions, LP'd into Curve
to mint vote-bearing tokens, voted through a pre-seeded malicious
proposal, executed it, and unwound — all atomically
(`rekt-beanstalk-rekt`). Critically, **delegation defeats naive
flash-loan guards**: in DeXe the attacker deposited flash-loaned tokens,
*delegated* to a slave contract that cast the deciding vote, then
undelegated and withdrew while the proposal was still locked, all in one
tx (`solodit-cyfrin-2023-11-10-cyfrin-dexe-0-1`). Curio shows the
small-stake version: acquire a modest amount of CGT, lock and vote to
gain control, then `delegatecall` into a malicious contract and mass-mint
(`rekt-curio-rekt`). Defenses that worked: snapshot voting power at a
past block/epoch, require a multi-day lock between deposit and vote, and
forbid delegate/undelegate + deposit/withdraw in the same block.

### V2: Vote → gauge routing errors (lost or phantom emissions)

Votes can be misrouted. In Satin, `_vote()` did not check the target pool
had a valid associated gauge, so weight given to a gaugeless pool meant
those emissions were lost (`solodit-trust-security-2023-02-24-satin-exchange-1-5`).
The inverse also exists: in Benqi's gauge system, votes are *automatically
recast* in the absence of a reset, so a gauge deactivated on the voter
(without being unregistered from the registrar) keeps "phantom" voting
power and continues drawing a share of rewards
(`solodit-cyfrin-2025-11-10-cyfrin-benqi-governance-v2-0-1-3`). The fix
in both cases is keeping vote weight and the live gauge set strictly in
sync — validate the gauge before counting a vote, and never let a gauge
be deactivated/removed on one component while another still attributes
weight to it.

### V3: Emission distribution accounting (double-count / insolvency)

The split-and-stream step can leak or duplicate value. In Satin's
`_distribute()`, when a guard condition was false the `claimable[gauge]`
accumulator was *not* zeroed, so the next `veShare` calculation re-counted
already-distributed emissions, potentially making the voter contract
insolvent; the fix both adjusts `claimable` correctly and restricts the
sensitive path to the trusted minter to stop attacker-driven re-entry of
the calculation (`solodit-trust-security-2023-02-24-satin-exchange-0-6`).
The lesson: any per-gauge "claimable/owed" accumulator must be settled to
zero exactly once per distribution, and emission math should not be
callable by arbitrary actors.

### V4: Distribution DoS via unbounded gauge loop

When weekly distribution loops over *all* gauges in one call, a
sufficiently large gauge set makes the call exceed the block gas limit
and revert permanently — bricking emissions and, transitively, the whole
protocol (`solodit-trust-security-2023-02-24-satin-exchange-0-3`). This
is the ve-specific instance of SWC-128 (DoS with block gas limit, `swc-128`):
looping across a data structure that grows over time. Remediation is to
avoid the global loop (Satin narrowed distribution to a single gauge) or
move to a pull/per-gauge pattern that can span multiple transactions.

### V5: Bribe / incentive-market manipulation

The bribe layer lets the briber rug the voters. In StakeDAO, a bounty
manager could call `increaseBountyDuration()` with
`maxRewardPerVote = 1` *after* voters had locked their Curve votes for 10
days; since payout is `min(bias*rewardPerVote, bias*maxRewardPerVote)`,
the payout collapses to ~0 and the manager reclaims almost the full
bounty — "free votes" (`solodit-zachobront-2023-05-26-stakedao-0-0`). The
recommendation: only allow `maxRewardPerVote` to be *increased*
mid-stream (`new >= old`). A related dilution exists at the stream level:
`notifyRewardAmount()` extends `periodFinish = now + DURATION` on every
call, so an attacker spamming a reward of `1` stretches the duration and
drives reward-per-second toward zero for gauge/bribe users; the fix is to
restrict `notifyRewardAmount()` to trusted callers
(`solodit-trust-security-2023-02-24-satin-exchange-1-3`). Bribe accounting
must also handle blacklist/adjusted-bias edges precisely: a blacklisted
voter who re-votes right after a period rollover can still be counted in
the gauge bias because the adjustment only subtracts when
`period > lastVote` (`solodit-zachobront-2023-05-26-stakedao-1-0`).

### V6: Escrow checkpoint math (unsafe casts, timestamp-as-clock)

The decay model relies on signed-integer `bias`/`slope` arithmetic and on
`block.timestamp`. veSync's `VotingEscrow` casts repeatedly without range
validation — e.g. `upoint.bias -= upoint.slope * int128(int256(block_time - upoint.ts))`
and `_locked.amount += int128(int256(_value))` — a discouraged pattern
that can silently misvalue voting power; the fix is SafeCast
(`solodit-zokyo-2023-06-23-vesync-1-1`). Because the same math uses
`block.timestamp`/`block.number` as a time proxy, epoch-boundary and
decay logic inherit SWC-116's caveats: miners/validators can nudge
timestamps and block times are not constant, so tight time-delta
assumptions around lock expiry and epoch flips deserve scrutiny
(`swc-116`).

### V7: Structural voting-power centralization

Even with correct code, ve designs trend toward concentration. A study of
48 large Ethereum DAOs finds that token registration, staking, and
delegation — each introduced for security or participation — systematically
reinforce the concentration of voting power
(`arxiv-2604.25959`). For an auditor this is a design-review flag: a
handful of ve whales (or a cartel coordinating bribes) can durably
control which gauges receive emissions, so "decentralized" emission
direction may in practice be steerable by a small group.

## Audit checklist

- Can voting power be acquired and *exercised* in the same transaction,
  or without a durable time lock between deposit and vote?
  (Beanstalk/Curio — `rekt-beanstalk-rekt`, `rekt-curio-rekt`)
- Does the system snapshot voting power at a past block/epoch rather than
  reading a live, flash-loanable balance?
- Do flash-loan / lock guards also cover the **delegation** path
  (delegate → vote → undelegate → withdraw in one block)?
  (`solodit-cyfrin-2023-11-10-cyfrin-dexe-0-1`)
- Does `_vote()` reject (or skip) votes for pools that have no valid
  registered gauge, so weight can't be sent into the void?
  (`solodit-trust-security-2023-02-24-satin-exchange-1-5`)
- Are gauge deactivation/removal and the vote-weight bookkeeping kept in
  sync, so a deactivated gauge cannot keep auto-recast "phantom" votes or
  lose weight mid-epoch? (`solodit-cyfrin-2025-11-10-cyfrin-benqi-governance-v2-0-1-3`)
- Is every per-gauge `claimable`/owed accumulator zeroed exactly once per
  distribution, with no branch that leaves it stale and double-countable?
  (`solodit-trust-security-2023-02-24-satin-exchange-0-6`)
- Is the sensitive emission/`veShare` math restricted to the trusted
  minter/voter rather than callable by arbitrary addresses?
- Does the weekly distribution avoid an unbounded loop over all gauges
  that could exceed the block gas limit and brick emissions?
  (`solodit-trust-security-2023-02-24-satin-exchange-0-3`, `swc-128`)
- Can a bribe/bounty manager reduce `maxRewardPerVote` (or otherwise cut
  payouts) *after* voters are locked in? Is `maxRewardPerVote` increase-only?
  (`solodit-zachobront-2023-05-26-stakedao-0-0`)
- Is `notifyRewardAmount()` permissioned so an attacker can't extend the
  reward period with dust and dilute reward-per-second?
  (`solodit-trust-security-2023-02-24-satin-exchange-1-3`)
- Does adjusted-bias / blacklist accounting correctly exclude voters in
  the *current* period, not just past periods (`period > lastVote` edge)?
  (`solodit-zachobront-2023-05-26-stakedao-1-0`)
- Are all `int128`/`int256` casts of `bias`/`slope`/`amount` in the
  escrow range-checked (SafeCast) rather than raw?
  (`solodit-zokyo-2023-06-23-vesync-1-1`)
- Do epoch-boundary and lock-expiry checks tolerate the imprecision of
  `block.timestamp`/`block.number` as a clock? (`swc-116`)
- Could a small set of ve whales / a bribe cartel durably capture emission
  direction (centralization design risk)? (`arxiv-2604.25959`)

## Prior incidents

- **Beanstalk (2022-04-17) — $181M**: Attacker flash-loaned ~$1B,
  LP'd into Curve to mint vote-bearing tokens, and voted through a
  pre-seeded malicious emergency proposal (BIP-18) that drained the
  protocol atomically; root cause was flash-acquired voting power plus no
  delay on emergency execution. [cites: `rekt-beanstalk-rekt`]
- **Mango Markets (2022-10-11) — $115M**: After manipulating the MNGO
  price to inflate collateral and drain pools, the attacker used the
  freshly acquired governance tokens to vote on a proposal resolving the
  mess in their favor — voting power as post-exploit leverage.
  [cites: `rekt-mango-markets-rekt`]
- **Curio (2024-03-23) — $16M**: Attacker acquired a small amount of CGT,
  then locked and voted to elevate their voting power within the contract,
  using it to `delegatecall` a malicious contract and mass-mint tokens; a
  voting-power-privilege access-control flaw. [cites: `rekt-curio-rekt`]
- **Atlantis Loans (2023-06-10) — ~$2.5M**: An abandoned-but-live lending
  protocol whose only control surface was governance; an attacker pushed
  and voted through a proposal granting them control of the protocol's
  tokens and drained users. [cites: `rekt-atlantis-loans-rekt`]

## References

- corpus entries:
  - `solodit-zachobront-2023-05-26-stakedao-0-0` — bounty manager sets `maxRewardPerVote` to 1 after votes lock, stealing free votes
  - `solodit-zachobront-2023-05-26-stakedao-1-0` — blacklisted voters still counted in gauge bias on same-period re-vote
  - `solodit-trust-security-2023-02-24-satin-exchange-1-5` — `_vote()` accepts pools with no valid gauge → emissions lost
  - `solodit-trust-security-2023-02-24-satin-exchange-0-6` — `claimable` not zeroed → double-counted `veShare` → voter insolvency
  - `solodit-trust-security-2023-02-24-satin-exchange-0-3` — distribution loops over all gauges → block-gas-limit DoS
  - `solodit-trust-security-2023-02-24-satin-exchange-1-3` — unpermissioned `notifyRewardAmount()` dilutes reward-per-second
  - `solodit-cyfrin-2025-11-10-cyfrin-benqi-governance-v2-0-1-3` — deactivated gauges keep phantom auto-recast votes
  - `solodit-cyfrin-2023-11-10-cyfrin-dexe-0-1` — flash loan + delegation bypasses flash-loan mitigations to decide a proposal
  - `solodit-zokyo-2023-06-23-vesync-1-1` — unsafe `int128`/`int256` casts of `bias`/`slope` in `VotingEscrow`
  - `rekt-beanstalk-rekt` — $181M flash-loan governance takeover
  - `rekt-curio-rekt` — $16M voting-power-privilege exploit
  - `rekt-mango-markets-rekt` — $115M; governance tokens used as post-exploit leverage
  - `rekt-atlantis-loans-rekt` — ~$2.5M governance proposal takeover
  - `arxiv-2604.25959` — measurement of voting-power centralization via registration/staking/delegation in 48 DAOs
  - `swc-128` — DoS with block gas limit (unbounded gauge loop)
  - `swc-116` — block values as a proxy for time (decay/epoch clock caveats)
