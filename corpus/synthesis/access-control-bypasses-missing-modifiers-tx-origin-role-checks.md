---
id: synthesis-access-control-bypasses-missing-modifiers-tx-origin-role-checks
source: synthesis
source_url: null
title: "Access control bypasses: missing modifiers, tx.origin, role checks"
ingested_at: 2026-05-16T00:00:00Z
vuln_class:
  - access-control
  - authentication
  - tx-origin
  - visibility
  - upgradeable-proxy
protocol_category:
  - general
  - bridge
  - perp
  - vault
  - rwa
tags:
  - synthesis
  - access-control
  - onlyOwner
  - tx-origin
  - role-based-access-control
  - initializer
derives_from:
  - swc-115
  - swc-100
  - solodit-naman-2024-08-07-hyacinth-0-0
  - solodit-zokyo-2022-07-05-made-for-gamers-0-0
  - solodit-zokyo-2024-05-24-chainport-0-1
  - solodit-cyfrin-2025-07-17-cyfrin-octodefi-v2-0-0-0
  - solodit-cyfrin-2024-07-18-cyfrin-securitize-redemptions-v2-0-1-2
  - solodit-cyfrin-2024-07-13-cyfrin-zaros-1-4
  - solodit-zokyo-2024-05-24-hord-0-1
  - solodit-zokyo-2023-08-11-velocore-3-4
  - solodit-zokyo-2024-01-12-trzn-finance-0-0
  - solodit-zokyo-2024-01-12-trzn-finance-0-1
  - solodit-cyfrin-2025-09-25-cyfrin-button-basis-trade-v2-0-1-0
  - rekt-gana-payment-rekt
  - solodit-zokyo-2024-04-10-airpuff-0-2
  - solodit-cyfrin-2025-07-22-cyfrin-doryoku-v2-0-2-3
  - solodit-auditone-2023-04-06-soonaverse-0-0
  - rekt-mobytrade-rekt
  - solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-2-1
  - solodit-zokyo-2022-09-07-umami-1-0
  - solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-1-1
  - solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-0-17
  - solodit-zokyo-2024-10-24-beyond-1-6
  - solodit-cyfrin-2025-11-06-cyfrin-securitize-global-registry-v2-0-2-4
  - solodit-zokyo-2023-06-12-limit-break-0-1
  - solodit-cyfrin-2025-07-31-cyfrin-linea-tokens-v2-3-0-2
  - solodit-pashov-audit-group-2023-11-01-yhairvesting-1-0
  - solodit-zokyo-2024-06-30-devve-2-7
---

# Access control bypasses: missing modifiers, tx.origin, role checks

## Pattern

Access control bugs are the most prosaic and most frequent class of high/critical
findings in Solidity (and Solana program) audits. The pattern is simple: a
function changes privileged state — fees, ownership, addresses pointed to by
the protocol, balances, validator sets, role memberships — and either has no
authorization gate at all, has a gate that checks the wrong principal
(`tx.origin` instead of `msg.sender`, or the wrong role), has a gate that was
deleted during refactoring, or has a gate that is bypassable through an
inherited public function from a base contract. The result is always the
same: any EOA can call the function and either drain the protocol, brick it
permanently, or seize ownership.

The corpus shows three distinct failure modes that an auditor must check
separately. First, *missing modifiers*: a privileged setter is declared
`external` with no `onlyOwner`, no `onlyRole`, and no `require(...)` guard —
either because the modifier was forgotten or because it was removed during a
refactor and never re-added [solodit-zokyo-2024-05-24-chainport-0-1,
solodit-cyfrin-2025-07-17-cyfrin-octodefi-v2-0-0-0]. Second, *wrong principal*:
the function checks `tx.origin == owner` instead of `msg.sender == owner`,
so any contract that the owner is tricked into calling can pivot back and
pass the check [swc-115, solodit-zokyo-2023-08-11-velocore-3-4]. Third,
*structural role bypass*: the protocol wraps `grantRole`/`revokeRole` in
wrappers with extra checks, but inherits the public OpenZeppelin
`AccessControl.grantRole` unchanged, so a role-admin can route around the
custom wrappers entirely [solodit-cyfrin-2025-11-06-cyfrin-securitize-global-registry-v2-0-2-4,
solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-2-1].

A related but distinct case is the *unprotected initializer*: an upgradeable
contract's `initialize()` function (or `_authorizeUpgrade`) is callable by
anyone, which means whoever wins the race after deployment becomes the
owner and can do anything an owner can do — including authorize a malicious
upgrade [solodit-zokyo-2022-07-05-made-for-gamers-0-0,
solodit-auditone-2023-04-06-soonaverse-0-0]. The same pattern appears on
Solana programs whose `initialize` instruction lacks a signer/PDA constraint
[solodit-cyfrin-2025-07-22-cyfrin-doryoku-v2-0-2-3].

Finally, the rekt corpus shows that even when on-chain access control is
correct, the off-chain authentication that produces the privileged
`msg.sender` (i.e. the private key for the owner address) is a single point
of failure. Stolen-key incidents [rekt-mobytrade-rekt, rekt-gana-payment-rekt]
read as access-control vulnerabilities from the attacker's side: ownership
is transferred to the attacker's EOA and every `onlyOwner` function then
opens for them. EIP-7702 makes this worse by letting EOAs temporarily behave
like contracts, which can defeat naive `tx.origin == msg.sender` EOA-only
guards [rekt-gana-payment-rekt].

## Variants

### V1: Setter with no modifier at all

A state-changing `external` function is declared without `onlyOwner`,
`onlyRole`, `onlyAdmin`, or any other authorization. The function changes
fees, addresses, oracle pointers, fairness flags, or critical configuration.
Cyfrin's OctoDeFi review documents three such setters in `FeeController`:
`setFunctionFeeConfig`, `setTokenGetter`, and `setGlobalTokenGetter`, all
public and unguarded [solodit-cyfrin-2025-07-17-cyfrin-octodefi-v2-0-0-0].
`Hyacinth::updateFairLaunchProperties` has the same shape — anyone can
toggle whether the token is tradeable
[solodit-naman-2024-08-07-hyacinth-0-0]. Securitize's
`CollateralLiquidityProvider::setExternalCollateralRedemption` lets anyone
swap in a malicious redemption contract that bricks the core `supplyTo`
flow [solodit-cyfrin-2024-07-18-cyfrin-securitize-redemptions-v2-0-1-2].

### V2: Modifier silently deleted in refactor

The function originally had a modifier; it was removed during an upgrade or
refactor and never replaced. ChainPort's `setAddressLength()` had the
`onlyClassifiedAuthority` modifier removed during a code upgrade and
shipped wide-open [solodit-zokyo-2024-05-24-chainport-0-1]. This is a
distinct review signal: diff the function against its prior version when a
contract has been upgraded — modifiers disappear during merges far more
often than you'd expect.

### V3: Missing per-account ownership check on user-data mutators

The function has a privileged feel (e.g. cancel an order, burn a token,
update a user's record) but the protection it needs is per-user, not
per-role. `OrderBranch::cancelMarketOrder` in Zaros lacked a check that the
caller owns the trading account being cancelled, so any address could clear
any trader's pending order [solodit-cyfrin-2024-07-13-cyfrin-zaros-1-4].
The TRZN `burn()` function lets any caller burn any address's tokens
[solodit-zokyo-2024-01-12-trzn-finance-0-0].

### V4: tx.origin used as the authorization principal

`require(tx.origin == owner)` looks like an `onlyOwner` check but is in
fact a phishing-equivalent gate: if the owner is ever induced to call a
malicious contract, that contract can then call the protected function and
pass [swc-115]. Velocore's `AdminFacet` used `tx.origin` because of a Forge
deploy script convention; Zokyo flagged it for replacement
[solodit-zokyo-2023-08-11-velocore-3-4]. Limit Break's PaymentProcessor had
business logic that trusted a `sellerAcceptedOffer` flag instead of
deriving identity from `msg.sender`/`tx.origin`, allowing a malicious
frontend to forge seller intent [solodit-zokyo-2023-06-12-limit-break-0-1].

### V5: tx.origin used as an EOA-only filter

Even when not used for authorization, `require(tx.origin == msg.sender)` is
frequently used to block smart-contract callers (anti-MEV, anti-flashloan,
mint-once-per-wallet). This has two failure modes: (a) it locks out
legitimate multisig and account-abstraction users
[solodit-zokyo-2022-09-07-umami-1-0]; and (b) under EIP-7702 an EOA can
temporarily delegate execution to contract code, so the check no longer
distinguishes EOAs from contracts — exploited live in the GANA Payment
drain [rekt-gana-payment-rekt]. Audits in 2024 still recommended adding
this modifier [solodit-zokyo-2024-04-10-airpuff-0-2]; the defensive value
of that recommendation has eroded post-7702.

### V6: Unprotected initializer (front-run takeover)

For upgradeable proxies, `initialize()` is the constructor analogue. If
deployment and initialization are not atomic, an attacker can front-run the
deployer's `initialize` call and set themselves as owner/admin
[solodit-auditone-2023-04-06-soonaverse-0-0,
solodit-zokyo-2024-06-30-devve-2-7]. The same pattern applies to Solana
programs whose initialize instruction is unconstrained
[solodit-cyfrin-2025-07-22-cyfrin-doryoku-v2-0-2-3]. A close cousin is the
unprotected `_authorizeUpgrade` on UUPS contracts — anyone can upgrade the
implementation if `_authorizeUpgrade` has no caller check
[solodit-zokyo-2022-07-05-made-for-gamers-0-0].

### V7: Inherited grantRole / renounceRole bypasses custom guards

Protocols that wrap OpenZeppelin's `AccessControl` with custom wrappers
(e.g. `addOperator`, `proposeAdmin` / `acceptAdmin`, zero-address checks)
often forget that the inherited public functions `grantRole`,
`revokeRole`, and `renounceRole` are still callable. A role-admin can
route around the wrapper entirely
[solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-2-1,
solodit-cyfrin-2025-11-06-cyfrin-securitize-global-registry-v2-0-2-4]. The
two-step admin handoff guarantee becomes illusory.

### V8: Default admin holds power over every role

If `DEFAULT_ADMIN_ROLE` is granted (often unintentionally, for a single
narrow purpose like pausing) but the role admins of other roles are never
reconfigured via `_setRoleAdmin`, that default-admin holder can mutate
membership of every role in the contract — even logically-isolated ones
that are supposed to belong to a different organization. BENQI's
`StakingContract` had this exact split: BENQI super-admin held
`DEFAULT_ADMIN_ROLE` for pausing, and could therefore grant or revoke the
Zeeve roles too [solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-1-1].

### V9: Mixing Ownable with AccessControl

When a contract inherits both `OwnableUpgradeable` and
`AccessControlUpgradeable`, admin wrappers gated by `onlyOwner` may
internally call `grantRole`, which requires `DEFAULT_ADMIN_ROLE`. After
ownership transfer (without an accompanying role transfer), the new owner
cannot manage roles and the old default-admin cannot upgrade — governance
deadlock with no on-chain remedy
[solodit-cyfrin-2025-09-25-cyfrin-button-basis-trade-v2-0-1-0].

### V10: Renounce-ownership / renounce-admin leaves contract permanently locked

`Ownable.renounceOwnership()` and `AccessControl.renounceRole(DEFAULT_ADMIN_ROLE, msg.sender)`
allow the last authority to remove itself, which can permanently brick
withdraw, pause, and upgrade paths [solodit-cyfrin-2025-07-31-cyfrin-linea-tokens-v2-3-0-2].
Two-step ownership transfers help but don't fix this — only an explicit
override of the renounce functions does.

### V11: One-step role transfer with no acceptance

Custom `transferAdmin` functions that flip ownership in a single
transaction with no two-step acceptance allow a typo in the new-owner
address to permanently brick the contract. The Beyond `BridgeRoles`
contract had a one-step `transferSuperAdmin` with no recovery
[solodit-zokyo-2024-10-24-beyond-1-6].

### V12: Wrong role used to gate a function

The function has a modifier, but the role chosen is conceptually wrong.
`yHairVesting`'s `setVTokenCost` / `setTokenCost` are gated by
`ROLE_CREATE_SCHEDULE` instead of `DEFAULT_ADMIN_ROLE` — the role that
creates schedules should not decide their prices
[solodit-pashov-audit-group-2023-11-01-yhairvesting-1-0]. TRZN's
`RM_UpdateReward` lacked a `RISK_MANAGER` role check that its sibling
`RM_UpdateDeposit` had [solodit-zokyo-2024-01-12-trzn-finance-0-1].

### V13: Default function visibility

A function declared without an explicit visibility specifier defaults to
`public` (pre-Solidity 0.5 — still relevant for legacy and forked code),
which exposes helpers that the author intended to be internal
[swc-100]. Always verify visibility of every function in a contract; the
audit smell is "helper that mutates state with no `_` prefix and no
visibility keyword."

### V14: Missing signer verification (Solana / non-EVM)

The EVM-shaped equivalent does not exist, but on Solana the program must
explicitly check `account.is_signer`; merely checking that the account
pubkey matches the expected admin is insufficient. Deriverse DEX's
`voting_reset` matched the operator address but never verified
`admin.is_signer`, so anyone could pass the admin account and trigger the
reset [solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-0-17].

## Audit checklist

- For every `external` / `public` state-changing function, can you identify
  the exact modifier or `require` that gates it? If the answer requires
  reading the parent contract, recheck V7.
- Does any function use `tx.origin` as an authorization principal? Replace
  with `msg.sender` [swc-115].
- Does any function use `require(tx.origin == msg.sender)` as an EOA-only
  filter? If so: (a) does it lock out multisigs and (b) is it still effective
  post-EIP-7702? [solodit-zokyo-2022-09-07-umami-1-0, rekt-gana-payment-rekt].
- Is `initialize()` callable by anyone after deployment? Is it called atomically
  with deployment, or could it be front-run? Is `_disableInitializers()` in
  the constructor of the implementation? [solodit-auditone-2023-04-06-soonaverse-0-0,
  solodit-zokyo-2024-06-30-devve-2-7].
- For UUPS proxies, does `_authorizeUpgrade` have an authorization check?
  [solodit-zokyo-2022-07-05-made-for-gamers-0-0].
- If the contract inherits `AccessControl`, are `grantRole`, `revokeRole`,
  and `renounceRole` either overridden or accepted as fully usable by the
  role-admin? Does any custom wrapper (`addOperator`, two-step admin
  handoff) exist that the inherited functions can bypass?
  [solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-2-1,
  solodit-cyfrin-2025-11-06-cyfrin-securitize-global-registry-v2-0-2-4].
- Is `DEFAULT_ADMIN_ROLE` granted to any account? If so, are role admins
  for every other role explicitly set with `_setRoleAdmin`, or does default
  admin implicitly control every role?
  [solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-1-1].
- Does the contract mix `Ownable` and `AccessControl`? If so, can owner
  and `DEFAULT_ADMIN_ROLE` diverge in a way that bricks role management?
  [solodit-cyfrin-2025-09-25-cyfrin-button-basis-trade-v2-0-1-0].
- Are `renounceOwnership` and `renounceRole(DEFAULT_ADMIN_ROLE, ...)`
  overridden to revert, or can the last authority irreversibly remove
  itself? [solodit-cyfrin-2025-07-31-cyfrin-linea-tokens-v2-3-0-2].
- Are admin / role transfers two-step (`propose` + `accept`)? Can the
  acceptance step verify the new admin actually controls the destination
  address? [solodit-zokyo-2024-10-24-beyond-1-6].
- For functions that mutate per-user data (cancel order, burn, withdraw to
  someone else, claim on behalf), does the function verify the caller owns
  that data? Not just "is the caller an admin," but "is the caller the
  per-user owner of the resource being mutated"?
  [solodit-cyfrin-2024-07-13-cyfrin-zaros-1-4,
  solodit-zokyo-2024-01-12-trzn-finance-0-0].
- For each role used to gate a function, is the *role itself* semantically
  correct for the action? (Pricing should not be gated by a
  schedule-creation role.) [solodit-pashov-audit-group-2023-11-01-yhairvesting-1-0,
  solodit-zokyo-2024-01-12-trzn-finance-0-1].
- For any contract that was upgraded or refactored: diff modifiers
  function-by-function against the prior version. Modifiers do disappear
  silently. [solodit-zokyo-2024-05-24-chainport-0-1].
- Are all functions explicitly declared with a visibility specifier?
  [swc-100].
- (Solana / non-EVM) For every privileged instruction, is there an explicit
  `account.is_signer` check in addition to address comparison?
  [solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-0-17].
- Is the owner/admin a single EOA? If so, the off-chain key custody is the
  real access-control boundary — multisig or threshold custody is the only
  defense against the GANA / Moby Trade class of incident
  [rekt-gana-payment-rekt, rekt-mobytrade-rekt].

## Prior incidents

- **GANA Payment (Nov 2025) — ~$3.1M**: Owner private key leaked; attacker
  used `transferOwnership` to rotate through eight pre-prepared addresses
  and authorized an EIP-7702 delegator to bypass the staking contract's
  `onlyEOA` (i.e. `tx.origin == msg.sender`) restriction on unstake.
  Demonstrates both the centralization-of-keys failure mode and the
  obsolescence of `tx.origin`-based EOA filters under EIP-7702.
  [cites: rekt-gana-payment-rekt]
- **Moby Trade (Jan 2025) — ~$1.0M stolen, $1.47M rescued by SEAL911**:
  Proxy admin private key compromise. The attacker `transferOwnership`'d
  the vaults and upgraded the implementations to drain WETH, WBTC, and
  USDC. SEAL911 noticed the new implementation had an unprotected
  `upgradeToAndCall` and counter-upgraded to rescue remaining USDC.
  Underscores that proxy admin key custody is access control.
  [cites: rekt-mobytrade-rekt]

## References

Audit-report findings (most-recent first):

- solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-2-1 — inherited
  grantRole/revokeRole bypass two-step transfer guard
- solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-2-7 —
  redundant access control check (duplicate guards)
- solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-0-17 — missing
  `is_signer` check on Solana
- solodit-cyfrin-2025-11-06-cyfrin-securitize-global-registry-v2-0-2-4 —
  inherited AccessControl bypasses custom wrappers
- solodit-cyfrin-2025-09-25-cyfrin-button-basis-trade-v2-0-1-0 — Ownable
  + AccessControl deadlock
- solodit-cyfrin-2025-07-31-cyfrin-linea-tokens-v2-3-0-2 — prevent
  accidental ownership/admin renouncement
- solodit-cyfrin-2025-07-22-cyfrin-doryoku-v2-0-2-3 — Solana initializer
  front-run
- solodit-cyfrin-2025-07-17-cyfrin-octodefi-v2-0-0-0 — missing access
  control on critical FeeController setters
- solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-1-1 — default admin
  controls all roles
- solodit-cyfrin-2024-07-18-cyfrin-securitize-redemptions-v2-0-1-2 —
  unprotected `setExternalCollateralRedemption`
- solodit-cyfrin-2024-07-13-cyfrin-zaros-1-4 — anyone can cancel any
  trader's market order
- solodit-zokyo-2024-10-24-beyond-1-6 — one-step role transfer mechanism
- solodit-zokyo-2024-08-07-hyacinth — missing access control on
  `updateFairLaunchProperties` (id: solodit-naman-2024-08-07-hyacinth-0-0)
- solodit-zokyo-2024-06-30-devve-2-7 — initialize missing access control
- solodit-zokyo-2024-05-24-hord-0-1 — missing access modifier on tolerance
  setter
- solodit-zokyo-2024-05-24-chainport-0-1 — modifier deleted during code
  upgrade
- solodit-zokyo-2024-04-10-airpuff-0-2 — recommendation to add
  tx.origin==msg.sender modifier
- solodit-zokyo-2024-01-12-trzn-finance-0-0 — missing access control on
  burn
- solodit-zokyo-2024-01-12-trzn-finance-0-1 — missing role check on
  RM_UpdateReward
- solodit-pashov-audit-group-2023-11-01-yhairvesting-1-0 — wrong role
  gates pricing setters
- solodit-auditone-2023-04-06-soonaverse-0-0 — initializers could be
  front-run
- solodit-zokyo-2023-08-11-velocore-3-4 — tx.origin used in AdminFacet
- solodit-zokyo-2023-06-12-limit-break-0-1 — business logic trusts a
  flag instead of msg.sender / tx.origin
- solodit-zokyo-2022-09-07-umami-1-0 — tx.origin==msg.sender blocks
  multisigs
- solodit-zokyo-2022-07-05-made-for-gamers-0-0 — unprotected
  `_authorizeUpgrade`

Foundational references:

- swc-115 — Authorization through tx.origin
- swc-100 — Function default visibility

Rekt post-mortems:

- rekt-gana-payment-rekt — GANA Payment, EIP-7702 + key compromise
- rekt-mobytrade-rekt — Moby Trade, proxy admin key compromise
