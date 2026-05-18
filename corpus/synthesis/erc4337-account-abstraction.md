---
id: synthesis-erc4337-account-abstraction
source: synthesis
source_url: null
title: "ERC-4337 & EIP-7702 account abstraction: pattern, variants, audit checklist"
ingested_at: 2026-05-18T00:00:00Z
vuln_class:
  - account-abstraction
  - signature-replay
  - signature-validation
  - paymaster
  - gas-griefing
  - access-control
protocol_category:
  - account-abstraction
  - wallet
  - paymaster
tags:
  - synthesis
  - erc-4337
  - eip-7702
  - smart-wallet
  - paymaster
  - bundler
  - entrypoint
  - erc-1271
derives_from:
  - solodit-cyfrin-2025-03-18-cyfrin-metamask-delegationframework1-v2-0-0-0
  - solodit-cyfrin-2025-03-18-cyfrin-metamask-delegationframework1-v2-0-2-0
  - solodit-cyfrin-2025-03-18-cyfrin-metamask-delegationframework1-v2-0-3-0
  - solodit-cyfrin-2025-03-18-cyfrin-metamask-delegationframework1-v2-0-1-0
  - solodit-cyfrin-2025-03-18-cyfrin-metamask-delegationframework1-v2-0-1-1
  - solodit-cyfrin-2025-04-01-cyfrin-metamask-delegationframework2-v2-0-0-0
  - solodit-cyfrin-2025-09-01-cyfrin-metamask-totalbalanceenforcer-v2-0-0-0
  - solodit-zokyo-2024-01-11-zimzam-0-0
  - solodit-zokyo-2024-01-11-zimzam-2-5
  - solodit-pashov-audit-group-2023-11-01-ambire-0-1
  - solodit-zokyo-2022-08-07-boba-2-2
  - solodit-zokyo-2023-08-07-boba-network-0-0
  - solodit-cyfrin-2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1-1-1
  - solodit-cyfrin-2025-06-02-cyfrin-evo-soulboundtoken-v2-0-0-4
  - solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-2-3
  - solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-1-0
  - solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-3-6
  - solodit-cyfrin-2025-11-06-cyfrin-securitize-global-registry-v2-0-2-2
  - solodit-cyfrin-2026-01-10-cyfrin-boundary-v2-2-1-3
  - solodit-cyfrin-2026-01-10-cyfrin-boundary-v2-2-1-6
  - solodit-zokyo-2024-07-01-heurist-2-0
  - arxiv-2604.10160
  - rekt-gana-payment-rekt
---

# ERC-4337 & EIP-7702 account abstraction

## Pattern

ERC-4337 reframes the meaning of "an Ethereum transaction." Instead of an
EOA-initiated tx, a user signs a `UserOperation` (sender, nonce, callData,
gas fields, paymasterAndData, signature). A **bundler** packs many UserOps
into a single on-chain call to a singleton **EntryPoint** contract, which
in turn invokes `validateUserOp` on the user's **smart account** and, if a
sponsor is involved, `validatePaymasterUserOp` on a **paymaster**. The
account decides what counts as a valid signature (it may use a custom
scheme, multisig, ERC-1271, passkeys, ZK proofs, or an aggregator), the
EntryPoint handles nonces and deposits, and the paymaster optionally pays
gas. EIP-7702 layers on top by letting an EOA temporarily set delegated
code so that an EOA can behave like a smart account within a transaction.

This architecture moves the trust boundary from "Solidity contract +
caller" to a multi-actor pipeline ("user → bundler → EntryPoint → account
→ paymaster → target"). Each actor has its own incentive, its own
deposit/stake, and its own simulation/execution distinction. The bugs
that cluster here come from a few recurring confusions: (i) developers
assume the EntryPoint's invariants (nonce uniqueness, replay protection,
sender authentication) cover their account contracts when they don't;
(ii) developers assume `msg.sender == tx.origin` or `code.length == 0`
still distinguishes "real" EOAs after EIP-7702; (iii) developers assume
the user's wallet address is the same on every chain even though
counterfactual deployment via factories with chain-specific salts
guarantees it generally is not; (iv) developers validate signatures with
raw `ecrecover` even though every smart account in scope can only sign
via ERC-1271; and (v) account / paymaster / enforcer authors write state
that is mutated in the "validation" or "before" hook but never reconciled
against the actual outcome of execution.

Beyond the spec-level bugs, the operational risk surface is wide. A
paymaster that mis-prices token-to-ETH using `latestAnswer` becomes a
free-gas faucet ([Boba](solodit-zokyo-2023-08-07-boba-network-0-0)). A
paymaster that has no `withdrawTo` becomes a graveyard for the operator's
stake ([Ambire](solodit-pashov-audit-group-2023-11-01-ambire-0-1)). A
bundler that trusts a UserOp hash computed against the wrong EntryPoint
will reject everything ([Boba EntryPointWrapper](solodit-zokyo-2022-08-07-boba-2-2)).
And the rapid rollout of EIP-7702 means any contract that uses `onlyEOA`,
`tx.origin`, `code.length == 0`, or unbounded callback gas to a recipient
is now suddenly attackable by a delegated EOA — as
[GANA Payment learned the hard way for $3.1M](rekt-gana-payment-rekt).

## Variants

### V1: UserOpHash missing EntryPoint / chainId → cross-EntryPoint or cross-chain replay

EIP-4337 explicitly requires the `userOpHash` to depend on both `chainid`
and the EntryPoint address so a UserOp valid on one EntryPoint cannot be
replayed against another. Custom accounts often roll their own
`getPackedUserOperationHash()` (or override `validateUserOp` and ignore
the `userOpHash` argument passed in by the EntryPoint) and forget the
EntryPoint binding. The Metamask `DeleGatorCore` /
`EIP7702DeleGatorCore` case is the canonical example: the account hashed
only the UserOp fields and the EIP-712 domain (chain + `address(this)`)
but not the EntryPoint, so simply upgrading or pointing the account at a
second EntryPoint and re-submitting the same signed UserOp re-executed
the transfer
([Cyfrin/Metamask](solodit-cyfrin-2025-03-18-cyfrin-metamask-delegationframework1-v2-0-0-0)).

### V2: Custom `validateUserOp` skipping nonce check → in-EntryPoint replay

A second class of "rolled my own validator" bug: the account overrides
`validateUserOp` but never calls a nonce check, on the theory that "the
EntryPoint will check the nonce." That's true *for the EntryPoint's own
`NonceManager`*, but only if the account doesn't manage its own nonce
namespace and only if `_requireFromEntryPoint()` is enforced. If the
account exposes any non-EntryPoint signature entry point, or if it ever
ships behind a misconfigured/compromised EntryPoint, the same signed
UserOp can be re-executed
([Zokyo/ZimZam](solodit-zokyo-2024-01-11-zimzam-0-0),
[follow-up](solodit-zokyo-2024-01-11-zimzam-2-5)).

### V3: Wrong return convention from `validateUserOp` / `_isValidSignature`

EIP-4337 distinguishes between a *signature mismatch* (return
`SIG_VALIDATION_FAILED`, do **not** revert) and any other error
(revert). Returning `SIG_VALIDATION_FAILED` for malformed signatures or
wrong-length data hides bundler-side problems and makes account behavior
diverge from other 4337-compliant wallets, breaking aggregators and
batching. Cyfrin flagged this in
`EIP7702StatelessDeleGator._isValidSignature`, which returned the
"signature mismatch" code on length errors instead of reverting
([Cyfrin/Metamask](solodit-cyfrin-2025-03-18-cyfrin-metamask-delegationframework1-v2-0-2-0)).

### V4: ECDSA-only signature checks excluding smart accounts

Protocols that gate behavior on a signed message (orders, claims,
permits, delegated execution, KYC attestations, gasless minting) often
use `ECDSA.recover` / `tryRecover`. That works for EOAs but silently
excludes every 4337 wallet, Safe multisig, Argent, and most institutional
custodians — none of which can produce an ECDSA signature that recovers
to their contract address. The fix everywhere in the corpus is the same:
delegate to OpenZeppelin's `SignatureChecker.isValidSignatureNow`, which
transparently handles ECDSA + ERC-1271. Examples:
[Myriad CLOB](solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-2-3),
[Evo Soulbound](solodit-cyfrin-2025-06-02-cyfrin-evo-soulboundtoken-v2-0-0-4),
[Securitize GlobalRegistry](solodit-cyfrin-2025-11-06-cyfrin-securitize-global-registry-v2-0-2-2),
[Remora Pledge](solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-3-6).
On zkSync the equivalent guidance is to use native AA helpers instead of
`ecrecover` because EOAs there are smart accounts
([Heurist](solodit-zokyo-2024-07-01-heurist-2-0)).

### V5: `code.length == 0` as EOA discriminator breaks after EIP-7702

The "if `signer.code.length == 0` use ECDSA, else use ERC-1271" pattern
used to be sound. EIP-7702 broke it: an EOA can have non-zero code (a
delegation designator) while still being able to ECDSA-sign with its
private key. The Boundary protocol case is precisely this: any EOA that
delegates via 7702 gets force-routed through the ERC-1271 branch and its
ECDSA signatures are rejected unless the delegated logic implements
1271 ([Cyfrin/Boundary](solodit-cyfrin-2026-01-10-cyfrin-boundary-v2-2-1-6)).
A safer pattern, used by Remora and Evo after audit, is:

> "Try ECDSA recovery first; if that fails or signer mismatches, fall
> back to `SignatureChecker.isValidERC1271SignatureNow`."
> ([Cyfrin/Remora](solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-3-6),
> [Cyfrin/Evo](solodit-cyfrin-2025-06-02-cyfrin-evo-soulboundtoken-v2-0-0-4))

### V6: EIP-7702 delegator bypassing `onlyEOA` / `tx.origin` gates

The GANA Payment exploit ($3.1M, BSC) shows the converse problem: a
contract that *relies* on `tx.origin == msg.sender` (or any "must be an
EOA" check) is now bypassable. The attacker rotated ownership across
eight pre-prepared EOAs, each of which had set an EIP-7702 delegation
designator pointing to a malicious delegator. That delegator could call
the staking contract while still passing the `onlyEOA` gate, manipulate
the reward rate, and drain it via repeated stake/unstake loops
([Rekt/GANA](rekt-gana-payment-rekt)).

### V7: Smart-contract callbacks forwarding unbounded gas to 7702 EOAs

`ERC1155.safeTransferFrom` and similar `onX` callbacks historically were
"safe-ish" against EOAs because `to.code.length == 0` skipped the
acceptance check. With EIP-7702, an EOA can have code, the callback
fires, and ~96% of remaining gas is forwarded. An attacker placed at
index 0 of a batched settlement can either siphon gas to subsidize their
own logic or burn enough to OOG-revert later iterations, falsely tagging
honest traders for blacklisting
([Cyfrin/Myriad](solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-1-0)).

### V8: Counterfactual AA wallet address ≠ same address on every chain

Bridges and cross-chain protocols often encode `msg.sender` as both the
source and destination address. For EOAs that's safe because keys map to
the same address everywhere. For 4337 / Safe / Argent wallets, the
factory salts, init code, and deployer addresses can differ per chain,
so the *same logical user* has *different addresses on different chains*.
Sending tokens to the source-chain address on the destination chain mints
into an address the user cannot control. Mitigation is an explicit
user-supplied `destinationWallet` parameter
([Cyfrin/Securitize bridge](solodit-cyfrin-2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1-1-1)).

### V9: Empty-signature pattern breaks Safe / pre-approved-hash flows

Some smart wallets (notably Safe) use the convention that an empty
`signature` argument to `isValidSignature` means "check pre-approved
hashes." Delegation managers / 4337 accounts that hard-revert on
`signature.length == 0` before calling 1271 lock out this entire class
of wallet from gas-efficient pre-approval. Fix: only enforce the empty
check for EOAs, then let the 1271 branch decide
([Cyfrin/Metamask DelegationManager](solodit-cyfrin-2025-03-18-cyfrin-metamask-delegationframework1-v2-0-3-0)).
A symmetric design pitfall is making ERC-1271 and "delegated signer"
modes mutually exclusive so a smart-account benefactor with one delegate
silently loses its 1271 verification path
([Cyfrin/Boundary](solodit-cyfrin-2026-01-10-cyfrin-boundary-v2-2-1-3)).

### V10: "validation/beforeHook updates state, execution may not happen" — allowance leakage

A 4337 / delegation pattern is to track spend limits in a `beforeHook`
("validation phase") and reconcile in an `afterHook`. If the execution
mode is `EXECTYPE_TRY` and the inner call fails, the EntryPoint does not
revert — but the spend counter has already been incremented. A malicious
delegate can repeatedly submit transfers designed to fail, draining the
delegator's allowance without moving tokens. Documented for
`ERC20TransferAmountEnforcer` and `NativeTokenTransferAmountEnforcer`
([Cyfrin/Metamask](solodit-cyfrin-2025-03-18-cyfrin-metamask-delegationframework1-v2-0-1-0))
and again for `ERC20StreamingEnforcer` /
`NativeTokenStreamingEnforcer` / `ERC20PeriodTransferEnforcer`
([Cyfrin/Metamask follow-up](solodit-cyfrin-2025-04-01-cyfrin-metamask-delegationframework2-v2-0-0-0)).
A related but distinct bug: a `TotalBalanceChangeEnforcer` placed *after*
a state-modifying enforcer (`NativeTokenPaymentEnforcer`) hits an early
return in `afterAllHook` because the shared balance tracker has already
been cleaned up by an earlier enforcer in the chain — so the final
validator never sees the payment-induced balance change
([Cyfrin/Metamask TotalBalanceEnforcer](solodit-cyfrin-2025-09-01-cyfrin-metamask-totalbalanceenforcer-v2-0-0-0)).

### V11: Paymaster economic / operational bugs

Paymasters are gas-sponsorship contracts with their own stake. Recurring
issues: (a) no `withdrawTo` path, so the operator's stake is stranded
unless an arbitrary-call admin function happens to exist
([Pashov/Ambire](solodit-pashov-audit-group-2023-11-01-ambire-0-1));
(b) using `latestAnswer` to price a sponsored token in ETH, returning
0 on a stale feed and quoting "free gas" to anyone who picks that token
([Zokyo/Boba](solodit-zokyo-2023-08-07-boba-network-0-0));
(c) wrong-EntryPoint helpers (`getUserOpHashes`) that revert when called
against the canonical chain EntryPoint, breaking off-chain bundling
flows ([Zokyo/Boba EntryPointWrapper](solodit-zokyo-2022-08-07-boba-2-2)).
Research-side, GasLiteAA proposes pushing paymaster state into a TEE
with on-chain attestations to cut the gas overhead of on-chain
sponsorship logic ([arXiv 2604.10160](arxiv-2604.10160)).

### V12: "EntryPoint is trusted, therefore my account is safe" assumption

Several audits flag that the in-scope account contract assumes any
nonce / replay / authentication guarantees come from the EntryPoint. If
the EntryPoint is ever upgraded, compromised, or if the account is also
callable via another path, those guarantees disappear. Defense in depth
— per-account nonces, EntryPoint address binding in the userOp hash,
explicit `_requireFromEntryPoint()` on every authority-sensitive entry
point — is the only way to survive a bad-EntryPoint world
([Zokyo/ZimZam Info](solodit-zokyo-2024-01-11-zimzam-2-5)).

## Audit checklist

Authentication & replay:

- Does the account's `getUserOpHash` / signature pre-image include
  **both** `chainid` **and** the EntryPoint address per EIP-4337?
- If `validateUserOp` is overridden, is the `userOpHash` parameter from
  the EntryPoint *actually used*, or does the account re-hash and
  potentially drop fields?
- Does the account either (a) trust the EntryPoint's `NonceManager` and
  enforce `_requireFromEntryPoint()`, or (b) implement its own per-key
  nonce check inside `_validateNonce`?
- On signature *mismatch*, does the validator return
  `SIG_VALIDATION_FAILED` (not revert)? On *malformed / wrong-length*
  signatures, does it revert (not silently fail)?
- Is the account safe against an upgrade / migration to a new EntryPoint
  (no UserOp signed under the old EntryPoint can be re-executed under
  the new one)?

Signature recipient flexibility:

- Are all places that recover a signer using `SignatureChecker` (ECDSA +
  ERC-1271) instead of bare `ecrecover` / `ECDSA.tryRecover`?
- For EIP-7702 EOAs (non-zero code, still ECDSA-signing), is there a
  fallback path: try ECDSA first, then ERC-1271?
- Are smart-account wallets able to use both their own 1271 logic and
  any delegated-signer feature simultaneously, or is the design
  documented as mutually exclusive?
- On zkSync (or any chain with native AA), is `ecrecover` swapped for
  the native AA signature verifier?

EIP-7702 surface:

- Does the contract use `tx.origin == msg.sender`, `onlyEOA`, or
  `to.code.length == 0` as a security boundary? If so, can a delegated
  EOA bypass it?
- Are external calls to user-supplied addresses (ERC-1155 / 721 / 777
  callbacks, low-level `call` to recipient) gas-capped so a 7702
  delegator cannot griefingly burn the caller's gas?
- Is `address.code.length` used as an "EOA vs contract" discriminator
  for signature verification (broken under 7702)?

Cross-chain & counterfactual addresses:

- Does any function assume `msg.sender` is the same address on the
  destination chain? If yes, is there an explicit `destinationWallet`
  parameter for AA wallets?
- Are factory deployments, salts, or init-code differences between
  chains documented for users of counterfactual wallets?

Paymaster:

- Can the paymaster operator withdraw its EntryPoint deposit (direct
  `withdrawTo` or a guaranteed admin path)?
- Does any oracle call inside `validatePaymasterUserOp` use a freshness-
  checked feed (`latestRoundData`, not `latestAnswer`) and revert on 0 /
  stale data?
- Does `validatePaymasterUserOp` respect ERC-4337 forbidden-opcode and
  storage-access rules so it can pass the bundler's simulation?
- Are postOp accounting failures (revert paths) handled so the paymaster
  isn't drained or DOS'd?

Delegation / session-key style enforcers:

- For any "spend limit" tracked in a beforeHook, is the spend committed
  *only* after the corresponding execution actually succeeds — or is
  `EXECTYPE_TRY` disallowed entirely?
- When enforcers are composable (multiple in a chain), does each
  enforcer's `afterAllHook` see the *final* post-execution state, or
  can a state-modifying enforcer earlier in the chain blank out a
  shared tracker and trigger early returns in later enforcers?
- Are linear-search "allowed targets / allowed methods" lists protected
  against duplicate-entry gas-grief stuffing, e.g. by requiring
  strictly increasing entries?
- For Safe-style smart wallets, does the redemption path *only* reject
  empty signatures for EOA delegators (so that pre-approved-hash flows
  on contract wallets still work)?

## Prior incidents

- **GANA Payment (Nov 2025) — $3.1M (BSC)**: Attacker obtained owner
  key, rotated ownership across eight EOAs each delegating via EIP-7702
  to a malicious delegator that bypassed the staking contract's
  `onlyEOA` check, manipulated reward rates, and drained funds via
  repeated stake/unstake loops [cites: rekt-gana-payment-rekt].
- **Metamask DelegationFramework (Mar 2025, pre-deployment H-severity)**:
  `EIP7702StatelessDeleGator` omitted the EntryPoint address from its
  UserOp hash, so any UserOp signed before an EntryPoint migration could
  be replayed verbatim through the new EntryPoint
  [cites: solodit-cyfrin-2025-03-18-cyfrin-metamask-delegationframework1-v2-0-0-0].
- **Metamask DelegationFramework — TransferAmount/Streaming enforcers
  (2025)**: Spent-limit counters were incremented in the before-hook
  before the actual transfer; combined with `EXECTYPE_TRY` this let a
  delegate drain the allowance with deliberately-failing transfers
  [cites: solodit-cyfrin-2025-03-18-cyfrin-metamask-delegationframework1-v2-0-1-0,
  solodit-cyfrin-2025-04-01-cyfrin-metamask-delegationframework2-v2-0-0-0].
- **Metamask TotalBalanceEnforcer (Sep 2025, H-severity)**: A
  `NativeTokenPaymentEnforcer` placed between two
  `TotalBalanceChangeEnforcers` in a delegation chain caused the second
  total-balance check to be bypassed (shared tracker already cleaned
  up), letting the recipient lose 3.3 ETH instead of the 0.5 ETH cap
  [cites: solodit-cyfrin-2025-09-01-cyfrin-metamask-totalbalanceenforcer-v2-0-0-0].
- **Myriad CLOB (Mar 2026, M-severity)**: ERC-1155 `safeTransferFrom`
  callbacks during batched settlement forwarded ~96% of remaining gas
  to recipients; an EIP-7702-delegated EOA at index 0 could OOG-revert
  the whole batch and mis-attribute the failure to later honest traders
  [cites: solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-1-0].
- **Securitize on/off-ramp bridge (Jul 2025, M-severity)**: `bridgeDSTokens`
  encoded `msg.sender` as the destination address, sending tokens to an
  address the AA-wallet user did not control on the destination chain
  [cites: solodit-cyfrin-2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1-1-1].
- **Boba Deposit Paymaster (Aug 2023, M-severity)**: Pricing the sponsor
  token via `latestAnswer` returned 0 on stale feeds, quoting effectively
  free gas to whoever used that token
  [cites: solodit-zokyo-2023-08-07-boba-network-0-0].

## References

- corpus entries:
  - solodit-cyfrin-2025-03-18-cyfrin-metamask-delegationframework1-v2-0-0-0 — UserOpHash missing EntryPoint
  - solodit-cyfrin-2025-03-18-cyfrin-metamask-delegationframework1-v2-0-2-0 — `_isValidSignature` return-code violation
  - solodit-cyfrin-2025-03-18-cyfrin-metamask-delegationframework1-v2-0-3-0 — Empty-signature rejection breaks Safe approved-hashes
  - solodit-cyfrin-2025-03-18-cyfrin-metamask-delegationframework1-v2-0-1-0 — Transfer enforcer spend-leak with EXECTYPE_TRY
  - solodit-cyfrin-2025-03-18-cyfrin-metamask-delegationframework1-v2-0-1-1 — Gas griefing via duplicate enforcer terms
  - solodit-cyfrin-2025-04-01-cyfrin-metamask-delegationframework2-v2-0-0-0 — Streaming enforcer spend-leak
  - solodit-cyfrin-2025-09-01-cyfrin-metamask-totalbalanceenforcer-v2-0-0-0 — TotalBalanceEnforcer bypass via early return
  - solodit-zokyo-2024-01-11-zimzam-0-0 — Missing `_validateNonce` override → replay
  - solodit-zokyo-2024-01-11-zimzam-2-5 — "EntryPoint is trusted" assumption
  - solodit-pashov-audit-group-2023-11-01-ambire-0-1 — Paymaster `withdrawTo` missing
  - solodit-zokyo-2022-08-07-boba-2-2 — `getUserOpHashes` wrong-EntryPoint revert
  - solodit-zokyo-2023-08-07-boba-network-0-0 — Paymaster oracle `latestAnswer` returns 0
  - solodit-cyfrin-2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1-1-1 — AA cross-chain address mismatch
  - solodit-cyfrin-2025-06-02-cyfrin-evo-soulboundtoken-v2-0-0-4 — `_verifySignature` incompatible with smart accounts; EIP-7702 fallback
  - solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-2-3 — Missing ERC-1271 support on order signing
  - solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-1-0 — Unbounded-gas ERC-1155 callbacks vs EIP-7702 EOAs
  - solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-3-6 — `SignatureChecker` + EIP-7702 try-ECDSA-first pattern
  - solodit-cyfrin-2025-11-06-cyfrin-securitize-global-registry-v2-0-2-2 — Pre-approved tx flow incompatible with smart-wallet operators
  - solodit-cyfrin-2026-01-10-cyfrin-boundary-v2-2-1-3 — ERC-1271 vs delegated signer mutual exclusion
  - solodit-cyfrin-2026-01-10-cyfrin-boundary-v2-2-1-6 — ERC-7702 benefactors broken by `code.length` discriminator
  - solodit-zokyo-2024-07-01-heurist-2-0 — Use native AA over `ecrecover` on zkSync
  - arxiv-2604.10160 — GasLiteAA: TEE-offloaded ERC-4337 paymaster sponsorship
  - rekt-gana-payment-rekt — $3.1M EIP-7702 delegator bypass of `onlyEOA`
