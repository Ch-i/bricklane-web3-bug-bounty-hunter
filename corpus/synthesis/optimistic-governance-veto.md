---
id: synthesis-optimistic-governance-veto
source: synthesis
source_url: null
title: "Optimistic Governance & Veto Mechanisms: pattern, variants, audit checklist"
ingested_at: 2026-06-04T00:00:00Z
vuln_class:
  - governance
  - access-control
  - authorization
  - timelock
  - flash-loan
protocol_category:
  - dao
  - governance
  - timelock
  - bridge
tags:
  - synthesis
  - optimistic-governance
  - veto
  - security-council
  - guardian
  - emergency-pause
derives_from:
  - solodit-cyfrin-2026-03-12-cyfrin-shutter-security-council-v2-0-0-0
  - solodit-cyfrin-2026-03-12-cyfrin-shutter-security-council-v2-0-0-2
  - solodit-cyfrin-2026-03-12-cyfrin-shutter-security-council-v2-0-0-1
  - solodit-cyfrin-2025-09-05-cyfrin-wlf-v2-1-1-3
  - solodit-cyfrin-2026-03-27-cyfrin-linea-mixed-upgrade-v2-0-1-0
  - solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-4-7
  - solodit-0x52-2023-10-07-dynamo-0-3
  - solodit-zachobront-2023-05-12-optimismgovernor-md-0-0
  - solodit-zachobront-2023-05-12-optimismgovernor-md-1-2
  - solodit-zachobront-2023-05-12-optimismgovernor-md-1-0
  - solodit-cyfrin-2024-09-27-cyfrin-bima-v2-0-2-5
  - solodit-cyfrin-2024-04-14-cyfrin-goldilocks-v1-1-1-2
  - solodit-recon-audits-2025-03-23-kleidi-report-0-8
  - solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-0-17
  - rekt-beanstalk-rekt
  - rekt-tornado-gov-rekt
  - rekt-atlantis-loans-rekt
  - arxiv-2604.25959
---

# Optimistic Governance & Veto Mechanisms

## Pattern

**Optimistic governance** inverts the usual affirmative model. Instead of a
proposal needing an active quorum of *yes* votes before it can act, the
proposal is assumed to pass and **executes by default after a delay unless a
trusted party intervenes** to stop it. The trusted party is typically a
**security council**, **guardian**, or **veto multisig** that watches a
challenge/timelock window and can veto, cancel, or pause a queued action. The
canonical implementation in the corpus is the Shutter Security Council, built
on the Zodiac **Azorius** module: a proposal moves through
`votingEndBlock → TIMELOCKED → execution window`, and a guard contract holds a
`vetoedTxHash` mapping that blocks execution of any hash the council marked
during the window [solodit-cyfrin-2026-03-12-cyfrin-shutter-security-council-v2-0-0-0,
solodit-cyfrin-2026-03-12-cyfrin-shutter-security-council-v2-0-0-2].

The security of this model rests on three legs, and almost every bug in the
corpus is one of them failing:

1. **A real, non-bypassable delay** between a proposal passing and executing.
   If there is no delay — or an "emergency" path that skips it — there is no
   window in which anyone can veto. Beanstalk is the archetype: a flash-loan
   acquired the votes and executed a malicious emergency proposal with no
   execution delay, draining $181M [rekt-beanstalk-rekt].
2. **Veto/pause power that is correctly scoped and survives state changes.**
   Veto state that is wiped on council rotation, pauses whose expiry is reset
   by an unrelated unpause, or cancel functions guarded by the wrong condition
   all silently re-enable an action the operators believed was stopped
   [solodit-cyfrin-2026-03-12-cyfrin-shutter-security-council-v2-0-0-0,
   solodit-cyfrin-2026-03-27-cyfrin-linea-mixed-upgrade-v2-0-1-0].
3. **A coherent authority hierarchy.** Multiple parties may *pause* (a cheap
   defensive action), but unpausing/overriding is a higher-risk operation that
   must sit with the highest authority. Inverting this — letting a guardian
   unpause something the owner deliberately paused — hands an attacker a way to
   defeat the emergency response [solodit-cyfrin-2025-09-05-cyfrin-wlf-v2-1-1-3].

Optimistic governance exists precisely *because* on-chain governance is hard to
keep both decentralized and safe. Empirical study of 48 large Ethereum DAOs
finds that token registration, staking, and delegation systematically
concentrate voting power, so in practice a small set of actors already controls
outcomes [arxiv-2604.25959]. Veto councils and guardians are an attempt to add
a safety brake on top of that reality — but each brake is itself a privileged,
centralized component an auditor must scrutinize for both *failure to stop a bad
action* and *abuse of the stop power*.

## Variants

### V1: Missing or bypassable execution delay (no veto window at all)

If a passing proposal can execute in the same transaction or block it is
finalized, no veto is physically possible. Beanstalk had a ~1-day delay for
normal governance actions but the malicious proposal rode an emergency
execution path that needed no delay; combined with flash-loan-acquired voting
power it drained the protocol instantly [rekt-beanstalk-rekt]. The lesson is
that the delay must apply to *every* execution path, including "emergency" and
admin shortcuts — any unguarded fast path is the path an attacker will take.

### V2: Veto/pause state lost or reset across an admin operation

The veto is only as durable as the storage that records it. In Shutter's
`SecurityCouncilAzorius`, `council` is immutable and rotation requires deploying
a new guard and calling `Azorius.setGuard(newGuard)`; the new guard starts with
an empty `vetoedTxHash` mapping, so any proposal that was vetoed under the old
guard but still inside its execution window becomes instantly executable the
moment the guard is swapped — a front-runnable race condition
[solodit-cyfrin-2026-03-12-cyfrin-shutter-security-council-v2-0-0-0]. The same
class appears in Linea's `PauseManager`: when the `SECURITY_COUNCIL_ROLE`
unpauses one pause type it resets `pauseExpiryTimestamp` globally, marking every
other active pause as expired so it can be immediately unpaused — even pauses
the council never lifted [solodit-cyfrin-2026-03-27-cyfrin-linea-mixed-upgrade-v2-0-1-0].

### V3: Miscalibrated challenge / timelock window (units & block-time)

A veto window is useless if it is the wrong length. Shutter documented
`timelockPeriod` as *seconds* using `block.timestamp`, but Azorius actually adds
it to `votingEndBlock` and compares against `block.number` — so the
recommended `259,200` produced a ~36-day timelock (proposals would expire before
becoming executable) instead of the intended 3 days; the correct value is
`21,600` blocks [solodit-cyfrin-2026-03-12-cyfrin-shutter-security-council-v2-0-0-2].
Block-number-vs-timestamp confusion and wrong block-time assumptions recur in
governor implementations and quietly make windows far too long (DoS) or far too
short (no time to veto).

### V4: Optimistic approval that lets a minority pass

When "no opposition" is treated as approval, the threshold to pass must be at
least as strict as the affirmative path — otherwise a minority wins by default.
In the Optimism Governor's `ApprovalVotingModule` there was no way to vote
*against* a module proposal, so `proposeWithModule()` loosened the bar: only
quorum (~3%) plus one vote on an option was needed, letting ~10% of the
community pass something 90% opposed [solodit-zachobront-2023-05-12-optimismgovernor-md-0-0].
The arithmetic version is Dynamo's guard quorum: `len(VotesEndorse) >=
len(LGov)/2` truncates with an odd guard count, so with 3 guards a single
endorsement (`3/2 = 1`) approved a proposal — one compromised guard could pass a
vault-draining action; the fix required `len/2 + 1`
[solodit-0x52-2023-10-07-dynamo-0-3].

### V5: Veto / cancel authority misconfigured

The functions that *stop* a proposal are themselves access-controlled state
machines and are frequently mis-specified. Goldilocks' `Goldigovernor.cancel()`
used `&&`-vs-`||` logic that reverted whenever the proposer still held more than
`proposalThreshold`, making proposals effectively un-cancellable by their author
[solodit-cyfrin-2024-04-14-cyfrin-goldilocks-v1-1-1-2]. Bima allowed a guardian
to "cancel" already-executed or already-cancelled proposals (misleading the
guardian about real state) while carving out a non-cancellable
`setGuardian` payload [solodit-cyfrin-2024-09-27-cyfrin-bima-v2-0-2-5].
Deriverse's `voting_reset` checked that the supplied admin key *matched* the
operator address but never that the account actually *signed* the transaction,
so anyone could reset critical voting parameters without the operator's key
[solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-0-17]. Authorization on the
veto/cancel/reset path must be as strong as on execution.

### V6: Authority inversion / asymmetric pause hierarchy

Pausing is a low-risk defensive action many parties should hold; unpausing is a
high-risk action that should sit with the top authority only. World Liberty
Financial gave guardians a symmetric `guardianUnpause()` so a guardian could
unpause a contract the owner had deliberately paused for an active incident —
overriding the owner's emergency decision [solodit-cyfrin-2025-09-05-cyfrin-wlf-v2-1-1-3].
Whenever multiple roles can pause/unpause, confirm the lift-the-brake direction
is monotonic toward the highest authority.

### V7: Veto exists but doesn't actually protect the asset

A veto guard that isn't enforced on the real execution path, or that protects
something the attacker can route around, is theater. StatusL2's emergency mode
let guardians flip a flag so users could exit a malicious `StakeManager` — but
if the attacker controls the upgrade they can remove or falsify
`emergencyModeEnabled`, bricking withdrawals despite the "emergency" mechanism
[solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-4-7]. Operationally, the same
gap appears as execution-path bugs: Optimism's manager could reopen or
indefinitely extend a vote deadline (even moving a `Defeated` proposal back to
`Active`), breaking finality assumptions [solodit-zachobront-2023-05-12-optimismgovernor-md-1-2];
the module's `propose()` could be front-run with the same `proposalId` to DoS
all legitimate proposals [solodit-zachobront-2023-05-12-optimismgovernor-md-1-0];
and timelock executors can suffer cross-operation reentrancy mid-execution
[solodit-recon-audits-2025-03-23-kleidi-report-0-8]. The veto is only meaningful
if it sits on the *single* path through which value actually moves.

### V8: Trojan-horse / opaque proposals that pass scrutiny

The veto window assumes reviewers can *see* what a proposal does. A proposal can
be crafted to look like benign, previously-seen logic while smuggling hidden
behavior. Tornado Cash's governance was hijacked by a "penalise cheating
relayers" proposal that reused trusted-looking code but quietly granted the
attacker control of the DAO via metamorphic/self-destruct trickery
[rekt-tornado-gov-rekt]. Atlantis Loans, an abandoned protocol with no one
actively watching, had proposal #52 pass and upgrade its token contracts to
malicious implementations, draining anyone with live approvals
[rekt-atlantis-loans-rekt]. A timelock/veto window only works if someone with
veto power actually decodes and understands the payload during it — including
proxy upgrades and code that deploys further code.

## Audit checklist

- Does **every** execution path (including "emergency"/admin shortcuts) pass
  through the same mandatory delay, or is there a fast path with no veto window?
  [rekt-beanstalk-rekt]
- Can voting power be acquired and used to push a proposal to execution within a
  single transaction (flash-loan governance)? [rekt-beanstalk-rekt]
- Is veto/pause state stored so it **survives** council rotation, guard
  replacement, and re-deployment — i.e. is there a gap where in-flight vetoes
  become unenforceable? [solodit-cyfrin-2026-03-12-cyfrin-shutter-security-council-v2-0-0-0]
- When one pause/veto is lifted, are the expiry/state of *other* active
  pauses/vetoes left untouched (per-type tracking, no global reset below
  `block.timestamp`)? [solodit-cyfrin-2026-03-27-cyfrin-linea-mixed-upgrade-v2-0-1-0]
- Are timelock/challenge-window units consistent between code and docs
  (`block.number` vs `block.timestamp`, blocks vs seconds), and does the
  configured value match the intended real-world duration at the chain's block
  time? [solodit-cyfrin-2026-03-12-cyfrin-shutter-security-council-v2-0-0-2]
- For optimistic/approval voting, is the bar to pass **at least as strict** as
  the affirmative path — i.e. is there a way to express opposition and does the
  proposal fail if opposition exceeds support? [solodit-zachobront-2023-05-12-optimismgovernor-md-0-0]
- Do council/guard quorum thresholds round **up** (`n/2 + 1`), so an odd member
  count can't let a minority (or single compromised signer) approve?
  [solodit-0x52-2023-10-07-dynamo-0-3]
- Is the cancel/veto function gated by correct logic, and does it reject
  already-executed/already-cancelled proposals so guardians can't be misled
  about state? [solodit-cyfrin-2024-04-14-cyfrin-goldilocks-v1-1-1-2,
  solodit-cyfrin-2024-09-27-cyfrin-bima-v2-0-2-5]
- Do veto/reset/admin entry points verify the caller is an actual **signer**
  (not merely that a supplied key matches an expected address)?
  [solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-0-17]
- Is the pause/unpause hierarchy monotonic — many can pause, only the highest
  authority can unpause — so a lower role can't override an owner's emergency
  pause? [solodit-cyfrin-2025-09-05-cyfrin-wlf-v2-1-1-3]
- Can a manager/owner extend, reopen, or re-activate a vote after it should be
  final, collapsing the finality the veto window depends on?
  [solodit-zachobront-2023-05-12-optimismgovernor-md-1-2]
- Can proposal creation/registration be front-run or its `proposalId` squatted
  to permanently DoS legitimate proposals? [solodit-zachobront-2023-05-12-optimismgovernor-md-1-0]
- Is the veto guard enforced on the **actual** value-moving execution path, and
  does the emergency mechanism still work if the very contract being protected
  is upgraded maliciously? [solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-4-7]
- Is the timelock executor protected against cross-operation reentrancy during
  execution of a queued action? [solodit-recon-audits-2025-03-23-kleidi-report-0-8]
- Does the review/veto process require decoding the full payload — including
  proxy upgrades and code that deploys further code — rather than trusting a
  proposal's title or apparent similarity to a prior one?
  [rekt-tornado-gov-rekt, rekt-atlantis-loans-rekt]

## Prior incidents

- **Beanstalk (2022-04-17) — $181M**: A flash loan supplied the BEAN/Curve
  voting power to pass and instantly execute a malicious emergency governance
  proposal; the absence of an execution delay on that path meant there was no
  veto window [rekt-beanstalk-rekt].
- **Tornado Cash Governance (2023-05-20) — ~$750K (full DAO control)**: A
  trojan-horse proposal disguised as a routine "penalise cheating relayers"
  change smuggled in code that handed the attacker control of the TORN
  governance token and router admin — the timelock existed but the malicious
  effect was hidden from reviewers [rekt-tornado-gov-rekt].
- **Atlantis Loans (2023-06-10) — $2.5M**: On an abandoned BSC lending protocol
  with no active guardian, proposal #52 passed and upgraded the token contracts
  to attacker-controlled implementations, draining users with live approvals —
  optimistic governance with nobody left to veto [rekt-atlantis-loans-rekt].

## References

- corpus entries (also in `derives_from`):
  - `solodit-cyfrin-2026-03-12-cyfrin-shutter-security-council-v2-0-0-0` — Veto state reset on Azorius guard rotation (Shutter Security Council)
  - `solodit-cyfrin-2026-03-12-cyfrin-shutter-security-council-v2-0-0-2` — `timelockPeriod` blocks-vs-seconds miscalibration (~36d vs 3d)
  - `solodit-cyfrin-2026-03-12-cyfrin-shutter-security-council-v2-0-0-1` — Use dedicated `getProposalTxHashes()` view in the veto guard
  - `solodit-cyfrin-2025-09-05-cyfrin-wlf-v2-1-1-3` — Guardian can override owner's emergency pause (authority inversion)
  - `solodit-cyfrin-2026-03-27-cyfrin-linea-mixed-upgrade-v2-0-1-0` — Security council unpause resets expiry of unrelated pauses
  - `solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-4-7` — Emergency mode defeated by malicious StakeManager upgrade
  - `solodit-0x52-2023-10-07-dynamo-0-3` — Guard approval threshold rounding lets a minority pass
  - `solodit-zachobront-2023-05-12-optimismgovernor-md-0-0` — Approval module lets a minority pass (no "against" votes)
  - `solodit-zachobront-2023-05-12-optimismgovernor-md-1-2` — Manager can extend/reopen vote deadlines, breaking finality
  - `solodit-zachobront-2023-05-12-optimismgovernor-md-1-0` — `proposalId` front-run DoS on proposal creation
  - `solodit-cyfrin-2024-09-27-cyfrin-bima-v2-0-2-5` — Guardian can cancel finalized proposals; cancel-state hygiene
  - `solodit-cyfrin-2024-04-14-cyfrin-goldilocks-v1-1-1-2` — Wrong validation in `Goldigovernor.cancel()`
  - `solodit-recon-audits-2025-03-23-kleidi-report-0-8` — Timelock executor cross-operation reentrancy
  - `solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-0-17` — `voting_reset` missing signer verification
  - `rekt-beanstalk-rekt` — Flash-loan governance, no execution delay ($181M)
  - `rekt-tornado-gov-rekt` — Trojan-horse governance proposal (DAO takeover)
  - `rekt-atlantis-loans-rekt` — Malicious proposal on abandoned protocol ($2.5M)
  - `arxiv-2604.25959` — On the Centralization of Governance Power in DAOs (motivation/trade-offs)
