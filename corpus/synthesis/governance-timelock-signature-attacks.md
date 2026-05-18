---
id: synthesis-governance-timelock-signature-attacks
source: synthesis
source_url: null
title: "On-chain governance, timelock & signature-replay attacks: pattern, variants, audit checklist"
ingested_at: 2026-05-18T00:00:00Z
vuln_class:
  - governance
  - timelock
  - signature-replay
  - access-control
  - flash-loan
protocol_category:
  - dao
  - governance
  - timelock
tags:
  - synthesis
  - governance
  - timelock
  - signature-replay
  - voting
  - delegation
derives_from:
  - rekt-beanstalk-rekt
  - rekt-audius-rekt
  - rekt-atlantis-loans-rekt
  - rekt-tornado-gov-rekt
  - rekt-fortress-rekt
  - solodit-cyfrin-2023-11-10-cyfrin-dexe-0-1
  - solodit-cyfrin-2023-11-10-cyfrin-dexe-0-6
  - solodit-cyfrin-2024-04-14-cyfrin-goldilocks-v1-1-1-0
  - solodit-pashov-audit-group-2023-08-01-smoothly-0-0
  - solodit-cyfrin-2024-12-17-cyfrin-quantamm-v1-2-1-5
  - solodit-cyfrin-2026-03-12-cyfrin-shutter-security-council-v2-0-0-0
  - solodit-cyfrin-2026-03-12-cyfrin-shutter-security-council-v2-0-0-2
  - solodit-recon-audits-2025-03-23-kleidi-report-0-8
  - solodit-cyfrin-2023-09-12-cyfrin-beanstalk-1-0
  - solodit-cyfrin-2025-09-05-cyfrin-wlf-v2-1-1-2
  - solodit-cyfrin-2025-09-05-cyfrin-wlf-v2-1-0-3
  - solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-2-0
  - solodit-pashov-audit-group-2023-05-01-ambire-0-0
  - solodit-zachobront-2023-05-12-optimismgovernor-md-1-2
  - solodit-cyfrin-2024-09-27-cyfrin-bima-v2-0-2-5
  - solodit-cyfrin-2024-09-27-cyfrin-bima-v2-0-1-4
  - arxiv-2604.25959
---

# On-chain governance, timelock & signature-replay attacks

## Pattern

On-chain governance is the seam where economic security (token holdings,
delegation) and protocol authority (parameter changes, upgrades,
treasury moves) meet. Attackers exploit one of three things: (1) the
**voting-power accounting** that decides outcomes, (2) the **timelock
machinery** that is supposed to delay execution after a vote, or (3) the
**signatures** used to authenticate votes, recoveries, queued
operations, or admin acts. In several historical incidents these three
pillars failed in combination — a flash loan briefly inflated voting
power, the quorum check accepted the inflated supply, and the timelock
either did not exist or was bypassed entirely, so a malicious payload
executed in the same transaction as the vote.

The underlying invariant a healthy governor must enforce is roughly:
"the population whose tokens decided this proposal is the same
population that bears the consequences of executing it." Anywhere that
invariant slips — voting power that can be acquired and exercised in
one transaction (Beanstalk, Atlantis Loans, Fortress), delegation that
launders restricted voters into eligible ones (Dexe, WLF V2), excluded
voters who can re-route their balance through a delegatee, totalSupply
or treasury balances that move between snapshot and execution
(Goldilocks, StatusL2) — the governance contract becomes a free
authorizer for whatever the attacker wants to do.

Timelock failures form the second cluster. Timelocks are only useful if
(a) every privileged path actually goes through them, (b) the delay
parameter is the value the operator thinks it is, and (c) executors
cannot bypass the queue. Audits regularly find privileged
`onlyExecutor` modifiers that gate by role rather than by `msg.sender ==
timelock` (QuantAMM), `timelockPeriod` units mis-specified as seconds
vs. blocks (Shutter), guard / veto state that is silently reset by
admin rotation (Shutter council rotation), or `execute()`
re-entrancy / cross-operation race conditions inside the timelock itself
(Kleidi). Beanstalk shows the extreme end of the spectrum: the
attacker pre-staged proposals, waited out the delay, and used a single
flash-loan tx to vote-and-execute.

Signature-replay bugs are usually a more local class of vulnerability,
but they bleed into governance in three ways. First, governance and
admin actions are increasingly authenticated by EIP-712 signatures
(castVoteBySig, queued-operation signatures, recovery signatures,
relayed permits) — and any signature scheme without (i) a nonce,
(ii) a deadline, (iii) `block.chainid` baked into the domain separator,
and (iv) every semantically distinct flag included in the hash is
replayable. Second, hard forks or proxy redeployments duplicate the
domain and let mainnet signatures be replayed on the fork (Beanstalk
permit). Third, attacker-controlled state changes mid-execution
(metamorphic contracts via CREATE2+selfdestruct, as in the Tornado Cash
governance takeover) effectively "replay" an already-approved
identifier with new payload — the on-chain check sees the same address
the DAO whitelisted, but the bytecode is now hostile.

## Variants

### V1: Flash-loan governance takeover with no execution delay

Voting power is read from a token whose balance / delegated weight can
be acquired with a single-block flash loan. The proposal can be both
submitted/voted *and* executed inside the same transaction, so the
attacker never has to hold real economic exposure. Beanstalk lost
$181M this way: the attacker pre-deployed proposals BIP-18 (steal
treasury) and BIP-19 (Ukraine donation as cover) and then, after the
1-day proposal-creation delay had matured, used Aave/Curve/Sushi flash
loans to acquire enough BEAN3CRV-f and BEANLUSD-f, deposit into the
Diamond, `vote(bip=18)` and `emergencyCommit(bip=18)` in the same
transaction [cites: rekt-beanstalk-rekt]. The same shape with weaker
quorums also hit Fortress (passed a malicious collateral-factor
proposal using flash-acquired FTS, $3M loss)
[cites: rekt-fortress-rekt] and Atlantis Loans (abandoned project,
attacker pushed proposal 52 to gain control of token contracts and
drained users with outstanding approvals, $2.5M)
[cites: rekt-atlantis-loans-rekt].

### V2: Flash-loan + delegation to bypass per-account locks

Some governors try to mitigate V1 by locking deposited tokens for the
duration of the proposal. Dexe shipped this defense; an attacker
defeated it by depositing flash-loaned tokens, **delegating** voting
power to a slave contract, having the slave vote, then **undelegating**
and withdrawing — all in one transaction — because the lock only
applied to the depositor's personal balance, not their delegated
weight. A separate Dexe finding shows the dual: voters restricted from
a proposal can launder their power by delegating to an unrelated
address that then votes for them
[cites: solodit-cyfrin-2023-11-10-cyfrin-dexe-0-1,
solodit-cyfrin-2023-11-10-cyfrin-dexe-0-6]. WLF V2 has the same shape
in reverse: `_excludedVotingPower` accounts get their direct `getVotes`
zeroed but can re-delegate to address X (whose
`_delegateCheckpoints[X].latest()` then includes the excluded balance)
or transfer tokens to a fresh address Y, regaining voting power they
were supposed to lose [cites: solodit-cyfrin-2025-09-05-cyfrin-wlf-v2-1-0-3].

### V3: Live-read totalSupply / treasury for quorum

A governor that compares `forVotes` to `IERC20(token).totalSupply()` at
state-read time (rather than to a snapshotted `getPastTotalSupply`) can
have its quorum check flip mid-flight. In Goldilocks,
`_getProposalState` divides the live `Goldiswap.totalSupply()` by 20
for quorum, so a Queued proposal can transition to Defeated purely
because more tokens were minted after the vote
[cites: solodit-cyfrin-2024-04-14-cyfrin-goldilocks-v1-1-1-0]. A
related accounting bug at StatusL2: `ERC20VotesUpgradeable` writes
total-supply checkpoints on raw `_mint`/`_burn` and ignores the
custom `totalSupply()` override that excludes
not-yet-distributed reward tokens — so `getPastTotalSupply`
overestimates and quorum becomes incorrect
[cites: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-2-0].

### V4: Vote-counting double-counts or extends arbitrarily

If the vote tally is incremented before the previous vote is removed,
the same address can vote twice and tip a small-operator quorum. In
Smoothly's `PoolGovernance::proposeEpoch`, `count = ++voteCounter[…]`
ran before `--voteCounter[prevVote]`, so an operator re-casting an
identical vote silently incremented their weight from 1 to 2 — enough
for a single operator to single-handedly execute a proposal in groups
of up to three
[cites: solodit-pashov-audit-group-2023-08-01-smoothly-0-0]. Optimism's
governor exposes a related shape on the deadline side: a Manager-only
`setProposalDeadline()` with no `block.timestamp` guard can extend
voting indefinitely — or even reopen a Defeated vote — until the
desired outcome materialises
[cites: solodit-zachobront-2023-05-12-optimismgovernor-md-1-2].

### V5: Timelock bypass — direct path around the queue

The timelock contract is properly delayed, but the protected
contract accepts calls from anyone with `EXECUTOR_ROLE` instead of
requiring `msg.sender == address(timelock)`. QuantAMM's
`onlyExecutor` modifier did exactly this: any executor could invoke
state-changing functions on `QuantAMMBaseAdministration` immediately,
making the timelock cosmetic
[cites: solodit-cyfrin-2024-12-17-cyfrin-quantamm-v1-2-1-5]. The
generic shape is "any role that *can* execute through the timelock is
implicitly granted unrestricted access to the target".

### V6: Timelock parameter / unit confusion

`timelockPeriod` is documented as seconds but compared against
`block.number`. In Shutter's Azorius integration the recommended
`259_200` was meant as 3 days; treated as blocks at 12s, it produces
a ~36-day timelock — long enough that proposals expire before they can
be executed, making the DAO practically unusable
[cites: solodit-cyfrin-2026-03-12-cyfrin-shutter-security-council-v2-0-0-2].
Equivalent classes of bug: voting delays measured in the wrong unit,
expiry windows that exclude weekends, or constants assuming Ethereum
12s block time on a different L1/L2.

### V7: Veto / guard state lost across rotation

Vetoes or other "no-execute" flags live in a guard contract whose
deployment is rotated periodically. The new guard ships with empty
state, so any proposal that was vetoed under the old guard but is still
inside its execution window becomes silently executable the instant
`setGuard(newGuard)` is called. Shutter's security-council guard had
exactly this race: the procedure required re-vetoing *after* setting
the new guard, opening a front-runnable window
[cites: solodit-cyfrin-2026-03-12-cyfrin-shutter-security-council-v2-0-0-0].

### V8: Cross-operation reentrancy in the timelock executor

A timelock that prevents replay of an individual operation (by removing
its id from a `_liveProposals` set and asserting `isOperationReady`)
can still be re-entered *across* operations: while executing
operation A, a malicious target can call back into the timelock to
execute operation B if it is ready. Kleidi audit flagged this on
`Timelock.execute` — no general `nonReentrant`, only per-id
removal — leaving cross-operation reentrancy possible when the
timelock interacts with untrusted targets
[cites: solodit-recon-audits-2025-03-23-kleidi-report-0-8].

### V9: Trojan-horse proposals / metamorphic contracts

The proposal payload links to an address that, at vote time, holds
benign code matching a previous "safe" proposal. After the vote and
before execution, the attacker uses `selfdestruct` to clear the
bytecode (resetting the deployer-contract nonce) and then redeploys
hostile code at the same address via CREATE / CREATE2. The governance
contract executes whatever now lives at the whitelisted address. This
is how Tornado Cash governance was taken over: a "fix the cheating
relayers" proposal pointed at a contract whose deployer was
self-destructable, allowing the attacker to mint themselves 1.2M votes
and seize the DAO [cites: rekt-tornado-gov-rekt].

### V10: Proxy / initializer storage collision granting governance to anyone

The governance proxy admin slot collides with an `Initializable`
storage slot. An attacker who can call `initialize()` re-defines the
voting and guardian addresses and mints themselves 10^13 delegated
votes via `Staking` / `DelegateManagerV2`, then transfers 18.5M AUDIO
out of the treasury. The vote is technically legitimate — it's the
authorization of *who* can vote that was broken
[cites: rekt-audius-rekt].

### V11: Vote-by-signature & queued-op signature replay

When governance / admin actions are authenticated by EIP-712
signatures, every defect in the signature scheme becomes a governance
risk:

* **No nonce / no deadline** → signatures replayable indefinitely; a
  one-time vote can be re-submitted (see the broader class catalogued
  in cross-chain-bridge-replay synthesis and the WLF V2 activation
  signature that bypasses EIP-712 in favour of a bare
  `keccak256(abi.encode(account))`
  [cites: solodit-cyfrin-2025-09-05-cyfrin-wlf-v2-1-1-2]).
* **Static chain ID in domain separator** → permits and signed
  governance acts on the mainnet contract replay on any forked chain
  (Beanstalk `LibTokenPermit` used the static `C.getChainId()`,
  enabling ETHPoW-style permit replay)
  [cites: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-1-0].
* **Mode/flag not in the hash** → an attacker mutates a single byte of
  the signature to flip the semantic. Ambire's wallet-recovery hash
  did not include the `isCancellation` flag, so anyone could turn a
  victim's `SIGMODE_RECOVER` signature into a `SIGMODE_CANCEL` and
  permanently grief their scheduled recovery
  [cites: solodit-pashov-audit-group-2023-05-01-ambire-0-0]. The same
  principle applies to any timelock action whose target/value/payload
  /salt is not fully bound into the signed digest.

### V12: Stale-vote / proposal-lifecycle state errors

Even after a vote ends, votes that were cast under one weight regime
must follow the user's state changes. Bima's `IncentiveVoting::unfreeze`
left an unfrozen user's previously cast votes in place even when they
asked to discard them — the vote weight persisted past the conditions
under which it was earned
[cites: solodit-cyfrin-2024-09-27-cyfrin-bima-v2-0-1-4]. Bima's
`AdminVoting::cancelProposal` also allowed the guardian to "cancel"
already-executed or already-cancelled proposals, corrupting the on-chain
state machine
[cites: solodit-cyfrin-2024-09-27-cyfrin-bima-v2-0-2-5].

### V13: Structural centralization that defeats the model

A separate but compounding concern: even well-implemented governance
contracts often have a *practically* small voter set. An empirical
study of 48 large public DAOs on Ethereum finds that token registration,
staking, and delegation — each individually security/UX features —
systematically reinforce voting-power concentration, so that the
"governance attack" surface is sometimes just "compromise one
delegate" [cites: arxiv-2604.25959]. Auditors should treat protocols
with a single-digit number of effective delegates as having a much
shorter path to the attack scenarios above.

## Audit checklist

Voting power & quorum:

- Can voting power be acquired and exercised in the same transaction
  (no deposit lock, no per-block snapshot, no `getPastVotes` with a
  snapshot block in the past)?
- Does the quorum check use `getPastTotalSupply(snapshotBlock)` or a
  live `totalSupply()` that can change after the snapshot?
- Does the `totalSupply` checkpoint accurately reflect the *effective*
  supply (e.g. excluding undistributed reward distributor balances)?
- Can delegation be used to (a) launder restricted voters into eligible
  voters, (b) re-route excluded voting power through a fresh delegatee,
  or (c) bypass per-account flash-loan locks?
- Can the same address vote twice (e.g. by re-casting an identical vote
  before the old one is decremented)?
- Can the Manager / proposer extend a proposal's deadline after voting
  has started — or, worse, after the vote has finished?
- Can already-executed or already-cancelled proposals be cancelled
  again, corrupting the state machine?
- Are user-state transitions (freeze / unfreeze / unlock / transfer)
  required to invalidate stale votes?

Timelock & executor:

- Does *every* privileged path actually go through the timelock, or do
  any modifiers gate by role membership rather than `msg.sender ==
  address(timelock)`?
- Are `EXECUTOR_ROLE`/`PROPOSER_ROLE` grants kept out of accounts that
  also have direct privileges on the target contract?
- Are timelock periods measured in the unit (`block.number` vs
  `block.timestamp`) that the deployment scripts and docs assume?
- Does `execute()` carry a `nonReentrant` guard, or is cross-operation
  reentrancy possible when the target is untrusted?
- If guard/veto state lives in a separate contract, what happens to
  in-flight vetoes during a guard rotation? Is there an atomic
  re-veto step, or a front-run window?
- Is the `cancel()` path on a queued operation properly gated and
  consistent with what was queued (same hashing inputs)?

Proposal payload & code provenance:

- Does the proposal payload include the target address *and* the
  expected code hash, or only the address?
- Can the target address ever change its bytecode (CREATE+selfdestruct
  metamorphic contracts; upgradable proxies; CREATE2 redeployment)
  between snapshot and execution?
- Are token approvals to mutable-code addresses (proxies the DAO can
  upgrade) audited at the user level (Atlantis Loans pattern)?

Signatures (votes-by-sig, queued ops, recoveries, permits, relayed
admin):

- Does every signed payload include a per-signer nonce that is
  incremented on use?
- Is there a `deadline` that the contract checks against `block.timestamp`?
- Does the EIP-712 `DOMAIN_SEPARATOR` read `block.chainid` dynamically
  (or cache + invalidate on chain-ID change) rather than baking in a
  static constant?
- Does the signed digest include *every* semantically distinct flag
  (mode bytes, isCancellation, isRecovery, target, value, payload,
  salt)?
- Is the `verifyingContract` field set to the correct proxy /
  implementation (not the implementation if signatures should bind to
  the proxy)?
- Is `EntryPoint` / domain-specific data included where multiple
  EntryPoints or chains might host the same code?
- Are signatures bound to the specific proxy/EOA/contract that should
  consume them (no cross-deployment replay across forks or testnets)?

Proxy / initialization:

- Does the proxy admin slot collide with any inherited `Initializable`
  or storage layout (Audius pattern)?
- Is `initialize()` guarded such that re-initialization on a fresh
  implementation cannot grant governance authority to an attacker?

Structural / operational:

- How many effective delegates control >X% of voting power? (See
  arxiv-2604.25959 — even mechanically-correct governance can be one
  delegate compromise away from full takeover.)
- Is there a sentinel / off-chain monitor watching for unexpected
  proposals on abandoned or low-attention deployments?

## Prior incidents

- **Beanstalk (2022-04-17) — $181M**: pre-staged BIP-18/BIP-19, then a
  single-tx flash-loan-funded vote + `emergencyCommit` to drain
  treasury [cites: rekt-beanstalk-rekt].
- **Audius (2022-07-23) — $6M of AUDIO**: proxy admin storage slot
  collided with `Initializable`, attacker re-initialised governance and
  minted 10^13 delegated votes [cites: rekt-audius-rekt].
- **Tornado Cash governance (2023-05-20) — $750k extracted + DAO
  hostage**: trojan-horse proposal whose deployer contract was
  self-destructed and redeployed with malicious code at the same
  address via CREATE2 [cites: rekt-tornado-gov-rekt].
- **Atlantis Loans (2023-06) — $2.5M**: abandoned protocol, attacker
  passed proposal 52 to take ownership of token contracts and drained
  users with stale approvals [cites: rekt-atlantis-loans-rekt].
- **Fortress Protocol (2022-05-08) — $3M**: public `submit()` on oracle
  plus malicious collateral-factor proposal pushed through low-quorum
  governance using ~$4.50 of FTS as collateral
  [cites: rekt-fortress-rekt].
- **Dexe (2023-11, pre-fix)**: combined flash loan + delegation
  bypassed deposit lock, allowing single-tx decide-and-withdraw
  attacks; separately, delegation laundered restricted voters
  [cites: solodit-cyfrin-2023-11-10-cyfrin-dexe-0-1,
  solodit-cyfrin-2023-11-10-cyfrin-dexe-0-6].
- **QuantAMM (2024-12, pre-fix)**: timelock cosmetic — any
  `EXECUTOR_ROLE` holder could call the protected admin contract
  directly [cites: solodit-cyfrin-2024-12-17-cyfrin-quantamm-v1-2-1-5].
- **Smoothly (2023-08, pre-fix)**: vote double-count via re-cast in
  `proposeEpoch` allowed single operator to execute proposals
  [cites: solodit-pashov-audit-group-2023-08-01-smoothly-0-0].
- **Beanstalk permit (2023-09 audit)**: static chain-ID in EIP-712
  domain separator → permit signatures replayable across any hard
  fork [cites: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-1-0].
- **Ambire (2023-05, pre-fix)**: signed recovery's `isCancellation`
  flag wasn't bound into the hash; anyone could mutate the mode byte
  and cancel any user's pending recovery
  [cites: solodit-pashov-audit-group-2023-05-01-ambire-0-0].

## References

Corpus entries used as direct sources for this note:

- rekt-beanstalk-rekt — Beanstalk governance flash-loan attack ($181M)
- rekt-audius-rekt — Audius proxy-collision governance takeover ($6M)
- rekt-atlantis-loans-rekt — Atlantis Loans abandoned-protocol
  governance attack ($2.5M)
- rekt-tornado-gov-rekt — Tornado Cash trojan-horse + metamorphic
  contract governance takeover
- rekt-fortress-rekt — Fortress malicious-proposal + oracle ($3M)
- solodit-cyfrin-2023-11-10-cyfrin-dexe-0-1 — flash loan + delegation
  bypass of deposit lock
- solodit-cyfrin-2023-11-10-cyfrin-dexe-0-6 — delegation bypass of
  voting restriction
- solodit-cyfrin-2024-04-14-cyfrin-goldilocks-v1-1-1-0 — live
  `totalSupply` used in quorum
- solodit-pashov-audit-group-2023-08-01-smoothly-0-0 — operator
  double-vote
- solodit-cyfrin-2024-12-17-cyfrin-quantamm-v1-2-1-5 — `onlyExecutor`
  bypasses timelock
- solodit-cyfrin-2026-03-12-cyfrin-shutter-security-council-v2-0-0-0
  — guard rotation resets veto state
- solodit-cyfrin-2026-03-12-cyfrin-shutter-security-council-v2-0-0-2
  — timelock period unit confusion (seconds vs blocks)
- solodit-recon-audits-2025-03-23-kleidi-report-0-8 — cross-operation
  reentrancy in `Timelock.execute`
- solodit-cyfrin-2023-09-12-cyfrin-beanstalk-1-0 — static chain-ID in
  EIP-712 domain separator → hard-fork replay
- solodit-cyfrin-2025-09-05-cyfrin-wlf-v2-1-1-2 — weak signature
  validation, EIP-712 bypass
- solodit-cyfrin-2025-09-05-cyfrin-wlf-v2-1-0-3 — excluded voting
  power re-gained via delegation / transfer
- solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-2-0 —
  `getPastTotalSupply` overestimates → wrong quorum
- solodit-pashov-audit-group-2023-05-01-ambire-0-0 — recovery hash
  missing mode flag, signature mutation
- solodit-zachobront-2023-05-12-optimismgovernor-md-1-2 — Manager can
  extend deadline arbitrarily
- solodit-cyfrin-2024-09-27-cyfrin-bima-v2-0-2-5 — cancelling
  executed/cancelled proposals
- solodit-cyfrin-2024-09-27-cyfrin-bima-v2-0-1-4 — stale votes after
  unfreeze
- arxiv-2604.25959 — structural centralization of DAO voting power
