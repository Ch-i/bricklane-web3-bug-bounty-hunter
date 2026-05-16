---
id: synthesis-proxy-and-upgradeability-pitfalls
source: synthesis
source_url: null
title: "Proxy and upgradeability pitfalls: pattern, variants, audit checklist"
ingested_at: 2026-05-16T00:00:00Z
vuln_class:
  - upgradeable-proxy
  - delegatecall
  - storage-collision
  - initialization
  - access-control
protocol_category:
  - infrastructure
  - defi
  - bridge
tags:
  - synthesis
  - proxy
  - upgradeability
  - uups
  - transparent-proxy
  - beacon-proxy
  - diamond
  - storage-gap
  - erc-7201
  - initializer
derives_from:
  - rekt-audius-rekt
  - swc-112
  - solodit-trust-security-2023-01-19-lyra-finance-2-0
  - solodit-cyfrin-2025-01-20-cyfrin-stakedotlink-stakingproxy-v2-0-1-1
  - solodit-pashov-audit-group-2023-12-01-vetenet-0-0
  - solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-2-0
  - solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-3-13
  - solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-3-0
  - solodit-cyfrin-2025-06-11-cyfrin-strata-v2-1-2-0
  - solodit-cyfrin-2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2-1-1
  - solodit-zokyo-2022-07-08-stablr-0-0
  - solodit-zokyo-2022-11-15-taunt-token-0-0
  - solodit-zachobront-2023-11-01-fungify-3-1
  - solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-2-0
  - solodit-cyfrin-2025-06-30-cyfrin-linea-spingame-v2-v2-1-1-4
  - solodit-cyfrin-2023-09-12-cyfrin-beanstalk-2-1
  - solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-34
  - solodit-cyfrin-2025-11-03-cyfrin-linea-burn-v2-2-1-1
  - solodit-cyfrin-2024-11-28-cyfrin-linea-v2-0-2-4
  - solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-0-2
  - solodit-cyfrin-2025-10-08-cyfrin-strata-tranches-v2-0-2-3
  - solodit-zokyo-2024-06-30-devve-2-0
  - solodit-auditone-2023-04-06-soonaverse-0-0
  - solodit-zokyo-2023-06-09-narwhal-finance-1-12
  - solodit-cyfrin-2024-04-11-cyfrin-wormhole-evm-ntt-v2-2-0
---

# Proxy and upgradeability pitfalls

## Pattern

Upgradeable contracts split the on-chain identity (the **proxy**, holding
storage and address/value) from the executable code (the **implementation**
/ **logic** contract). The proxy `delegatecall`s into the implementation,
which means the implementation's bytecode runs against the proxy's
storage layout, `address(this)`, and `msg.value`/`msg.sender`. Every
upgrade pattern in production — Transparent (EIP-1967), UUPS, Beacon
(EIP-1822), Diamond/Multi-facet (EIP-2535), and minimal clones / EIP-1167
— shares this same `delegatecall` substrate, and therefore shares the
same fundamental hazards (swc-112).

Three structural assumptions have to hold for the system to be safe and
auditors should treat each as a separate axis:

1. **Storage layout discipline.** Two implementations sharing one proxy
   must agree, byte-for-byte, on what each storage slot means. Append-only
   layouts, storage gaps, and EIP-7201 "namespaced" storage are the
   industry mechanisms for enforcing this; without them, an upgrade that
   adds a state variable to a base contract can silently overwrite child
   storage (solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-2-0,
   solodit-cyfrin-2025-01-20-cyfrin-stakedotlink-stakingproxy-v2-0-1-1,
   solodit-cyfrin-2025-06-11-cyfrin-strata-v2-1-2-0). Worse, *the proxy
   itself* can write to slots that collide with logic-contract state, as
   in Audius — the proxy's `proxyAdmin` slot collided with OpenZeppelin's
   `Initializable._initialized` slot, letting the attacker re-run
   initialization and seize governance (rekt-audius-rekt).

2. **Initialization is single-shot, atomic, and authenticated.** Because
   constructors don't run against proxy storage, all state must be set by
   an `initialize` function. Anyone who reaches that function before the
   legitimate deployer becomes the contract's "owner". Two distinct
   surfaces leak this property: (a) the *proxy*, if the deployer doesn't
   atomically combine `deploy` + `initialize` in one transaction
   (solodit-auditone-2023-04-06-soonaverse-0-0); and (b) the *implementation
   itself*, if its constructor does not call `_disableInitializers()` —
   attackers can take ownership of the live logic contract, and if any
   future upgrade adds a `delegatecall`, they can `SELFDESTRUCT` it and
   brick every proxy that points there (solodit-trust-security-2023-01-19-lyra-finance-2-0,
   solodit-zokyo-2023-06-09-narwhal-finance-1-12,
   solodit-cyfrin-2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2-1-1).

3. **The execution context is the proxy, not the implementation.** Logic
   that touches `address(this)`, `msg.value`, `block.chainid`, or even
   `immutable`/constructor state can behave correctly when tested in
   isolation but break under a proxy — constructor-set variables live on
   the implementation, not the proxy (solodit-zokyo-2024-06-30-devve-2-0,
   solodit-zachobront-2023-11-01-fungify-3-1). `msg.value` is persisted
   across nested `delegatecall`s and can be weaponized inside loops
   (solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-34).

These three failure modes are the spine of almost every proxy bug
reported in the corpus.

## Variants

### V1: Storage collision between proxy admin/implementation slots and logic state

The proxy writes some control state (admin, implementation pointer,
initialized flag) at a fixed slot; the logic contract independently
declares state at a slot that happens to overlap. EIP-1967 specifies
keccak-based slots specifically to avoid this. Custom proxies that use
slot 0/1 for the admin and implementation pointer (as in
`AudiusAdminUpgradeabilityProxy`) collide with OZ `Initializable._initialized`
at slot 0, allowing re-initialization (rekt-audius-rekt).
solodit-zachobront-2023-11-01-fungify-3-1 explicitly calls out the same
anti-pattern: "It is not generally recommended to use standard storage
slots (like 0 and 1) for the implementation and owner addresses … it is
recommended to use non-standard slots (such as the hashes of obscure
values)."

### V2: Storage collision between base and child implementations on upgrade

The upgrade itself is the trigger. An inherited "Initializable"
parent — for example `StratFeeManagerInitializable`,
`StakingProxy`, or a third-party dependency like `GelatoVRFConsumerBase` —
adds a new state variable in a later release. Without a reserved
`uint256[N] __gap` at the end of the parent (or ERC-7201 namespaced
storage), every storage slot in child contracts shifts down by one,
silently corrupting state
(solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-2-0,
solodit-cyfrin-2025-01-20-cyfrin-stakedotlink-stakingproxy-v2-0-1-1,
solodit-cyfrin-2025-06-30-cyfrin-linea-spingame-v2-v2-1-1-4). The
modern preferred remedy is ERC-7201 "namespaced storage" — each
contract derives its storage root from
`keccak256(abi.encode(uint256(keccak256("example.location")) - 1)) & ~bytes32(uint256(0xff))`
(solodit-cyfrin-2025-06-11-cyfrin-strata-v2-1-2-0,
solodit-cyfrin-2024-04-11-cyfrin-wormhole-evm-ntt-v2-2-0). Storage gaps
are still acceptable but no longer the OpenZeppelin recommendation.

### V3: Implementation contract left initializable / `_disableInitializers()` missing

After deploy, anyone calls `initialize()` directly on the implementation
contract and becomes its owner. The proxy is unaffected because it has
its own storage, but the implementation is now an attacker-controlled
contract. In transparent proxies the impact is low (cosmetic); the real
danger is if the implementation contains a `delegatecall` to an
arbitrary target — the attacker, now owner, points it at a contract that
runs `SELFDESTRUCT`, destroying the code at the implementation address
and bricking the proxy until governance can ship a new implementation
(solodit-trust-security-2023-01-19-lyra-finance-2-0). The canonical fix
is calling `_disableInitializers()` from the implementation's constructor
with `/// @custom:oz-upgrades-unsafe-allow constructor`
(solodit-cyfrin-2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2-1-1,
solodit-cyfrin-2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1-3-3,
solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-3-0).

### V4: Initializer front-running (deploy ≠ initialize in same tx)

The deployer sends two transactions: deploy proxy, then call `initialize`.
Anyone watching the mempool can squeeze in between, calling `initialize`
with their own arguments — owner, admin role, fee receiver — and stealing
the contract before legitimate use begins
(solodit-auditone-2023-04-06-soonaverse-0-0,
solodit-zokyo-2023-06-09-narwhal-finance-1-12,
solodit-zokyo-2022-07-08-stablr-0-0,
solodit-zokyo-2022-11-15-taunt-token-0-0). The same issue applies to
**newly cloned EIP-1167 minimal proxies** — every `clone()` that doesn't
initialize in the same tx becomes a free-for-all
(solodit-pashov-audit-group-2023-12-01-vetenet-0-0). Defenses: atomic
deploy-and-initialize (use `TransparentUpgradeableProxy`'s constructor
`_data` argument, or `upgradeToAndCall`, or wrap clone + initialize in
one factory function), and protect any post-deploy `initializeV2`/
`initializeVN` migration functions with `onlyOwner` or `reinitializer(N)`
(solodit-zokyo-2022-07-08-stablr-0-0,
solodit-cyfrin-2025-11-03-cyfrin-linea-burn-v2-2-1-1).

### V5: `reinitializer(N)` versioning errors during multi-step upgrades

Once a proxy is initialized, `_initialized` is set and the `initializer`
modifier can never run again. New state needed by an upgrade must be
seeded via `reinitializer(N)` where `N > _initialized`. Two failure
modes show up: shipping an upgrade with `initializer` instead of
`reinitializer`, which reverts on-chain and forces emergency redeploy
(solodit-cyfrin-2025-11-03-cyfrin-linea-burn-v2-2-1-1); and choosing
the wrong `N`, e.g. using `reinitializer(6)` on a proxy whose stored
version is `1`, which silently skips state and breaks cross-chain
parity with sibling contracts that did do it correctly
(solodit-cyfrin-2024-11-28-cyfrin-linea-v2-0-2-4). A related class of
mistake is editing on-chain `Init` migration contracts after they have
executed — the on-chain state is no longer reproducible from source
(solodit-cyfrin-2023-10-13-cyfrin-beanstalk-bip-38-3-0,
solodit-cyfrin-2023-10-13-cyfrin-beanstalk-bip-38-3-1).

### V6: Constructor-set state on an upgradeable contract

Variables assigned in the constructor live on the implementation, not
the proxy. Calling them via the proxy returns the zero value
(solodit-zokyo-2024-06-30-devve-2-0,
solodit-zachobront-2023-11-01-fungify-3-1: "FungToken uses the
non-upgradeable OpenZeppelin ERC20 contract, which sets the `name` and
`symbol` storage slots in the constructor. As a result, these values
will be set on the implementation contract, rather than the proxy.").
The systemic version of this bug is using a *non*-upgradeable OpenZeppelin
base contract (e.g. `ERC20`, `AccessControl`) where the upgradeable
sibling exists
(solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-2-0).

### V7: Implementation contract is itself self-destructible / upgrade-frozen

If an implementation is or becomes capable of `SELFDESTRUCT`, the
bytecode at that address can be erased. After that, every proxy pointing
to it becomes a `delegatecall` to empty code, which *returns success
silently* — payable functions accept ETH that goes nowhere; non-payable
functions look like they worked but did nothing. Diamond/EIP-2535 proxies
inherit the same failure mode if a facet address is wrong or the facet
was destroyed (solodit-cyfrin-2023-09-12-cyfrin-beanstalk-2-1, citing the
Trail of Bits Diamond critique). The Parity multisig wallet incident is
the historical archetype of this class of bug.

### V8: Proxy reuse / per-user proxies pointing to outdated implementations

When a factory maintains a pool of proxies/clones per user (e.g. Strata
`UnstakeCooldown::proxiesPool`), and the canonical implementation is
upgraded via `setImplementations`, **already-existing clones still point
at the old implementation** because the target is baked into a clone's
bytecode. Reusing them after an upgrade silently executes the old logic
— which may be the exact vulnerable version that motivated the upgrade
(solodit-cyfrin-2025-10-08-cyfrin-strata-tranches-v2-0-2-3). Symmetric
failure: a factory's `migrate(version)` path doesn't honor the
`blacklist[version]` check that `create(version)` enforces, allowing
existing vaults to be migrated *into* a blacklisted vulnerable
implementation (solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-0-2).

### V9: Wrong proxy pattern for the deployment topology

For a single instance: Transparent or UUPS. For many homogeneous
instances that should all upgrade atomically: **Beacon** is correct;
Transparent + a single `ProxyAdmin` forces the operator to iterate
through every proxy individually (solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-3-13).
The corollary: UUPS implementations must contain a working `_authorizeUpgrade`
or the proxy becomes un-upgradeable forever, and a UUPS upgrade *to* an
implementation that lacks `UUPSUpgradeable` is fatal — there is no second
chance.

### V10: `msg.value` persisted across `delegatecall` weaponized in loops

Because `delegatecall` does not reset `msg.value`, a payable function
that loops over user-supplied calls (e.g. a Diamond's `farm()` /
`multicall`) can let the caller "spend" the same ETH multiple times if
sub-calls naively trust `msg.value`. Beanstalk's auditors call this
out as a special hazard for any future upgrade that adds payable
multicall-style entry points (solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-34,
referencing samczsun's "two rights might make a wrong" write-up).

## Audit checklist

Storage layout
- Does every upgradeable parent contract end with a `uint256[N] __gap`
  *or* use ERC-7201 namespaced storage? (V2)
- If ERC-7201 is used, does every namespace literally implement
  `keccak256(abi.encode(uint256(keccak256("ns")) - 1)) & ~bytes32(uint256(0xff))`,
  not a hand-rolled hash? (V2; Wormhole NTT)
- Does the proxy avoid using slots `0` or `1` for admin/implementation
  pointers? Does it use EIP-1967 slots? (V1; Audius)
- Are inherited third-party libraries (non-OZ, e.g. `GelatoVRFConsumerBase`)
  upgrade-safe, and if not, is a buffer gap inserted in the consuming
  child contract? (V2)
- For every state variable: is it declared in the upgradeable variant of
  its parent (e.g. `ERC20Upgradeable`, not `ERC20`)? (V6)

Initialization
- Does every implementation's constructor call `_disableInitializers()`
  with the `oz-upgrades-unsafe-allow constructor` annotation? (V3)
- Is `initialize()` called atomically with proxy deployment (in the
  proxy constructor, via `upgradeToAndCall`, or wrapped in a single
  factory tx)? (V4)
- Are all `initializeV2` / `migrate*` post-deploy bootstrap functions
  either gated by `onlyOwner` or by the `reinitializer(N)` modifier? (V4, V5)
- Does the chosen `N` for `reinitializer(N)` strictly exceed the current
  on-chain `_initialized` value, verified by `cast storage`? (V5)
- For clone-factory patterns: does the factory call `initialize` in the
  same transaction as `clone()`/`cloneDeterministic`? (V4)

Implementation invariants
- Are there any `delegatecall`s whose target can be set by the implementation
  owner? If yes, combined with missing `_disableInitializers`, this is a
  brick-the-proxy chain. (V3, V7)
- Are storage variables ever assigned in the constructor of an upgradeable
  contract? They will be invisible through the proxy. (V6)
- For Diamond proxies and any fallback-`delegatecall` pattern: is the
  target's code size checked before the delegatecall, or is silent failure
  swallowed? (V7)
- For payable functions reachable via `delegatecall` loops/multicall:
  is `msg.value` consumed exactly once, or could nested `delegatecall`s
  see the same value? (V10)

Factory / lifecycle
- For per-user clones cached in a pool: when reusing a clone, is its
  implementation address compared against the current canonical
  implementation, and the clone discarded if stale? (V8)
- For factory `create` / `migrate` paths with a version blacklist: is
  the blacklist enforced on **both** entry points? (V8)
- Is the chosen proxy topology appropriate — beacon for many homogeneous
  instances, UUPS/transparent for singletons? (V9)
- For UUPS: is `_authorizeUpgrade` implemented with real access control
  on every implementation that will live behind the proxy? Is there any
  upgrade path that would point the proxy at a non-UUPS implementation?
  (V9)

Operational
- After a proxy is initialized on mainnet, are subsequent migrations
  reproducible from source, i.e. is the on-chain `Init*` contract
  ossified rather than silently edited in the repo? (V5; Beanstalk)

## Prior incidents

- **Audius (2022-07) — $6M**: A custom upgradeable proxy stored the
  proxyAdmin at slot 0, colliding with OpenZeppelin `Initializable._initialized`.
  The attacker re-ran `initialize` on governance, granted themselves
  voting power, and passed a malicious proposal to drain the treasury.
  Both pre-exploit audits (Kudelski, OpenZeppelin) missed it
  [cites: rekt-audius-rekt].
- **Parity multisig (2017) — ~$280M frozen** (historical archetype): an
  attacker took ownership of the un-`_disableInitializers`'d library
  contract behind every Parity multisig proxy and called `kill()`,
  selfdestructing the library and freezing every dependent wallet. The
  pattern is reproduced in modern audits' "implementation contract
  takeover + SELFDESTRUCT" warning
  [cites: solodit-trust-security-2023-01-19-lyra-finance-2-0].
- **Wormhole NTT (2024) — design issue, caught in audit**: Inconsistent
  ERC-7201 namespace derivation — using `Pause.pauseRole` strings rather
  than the EIP formula — would have weakened the collision-resistance
  guarantee for the namespaced storage roots
  [cites: solodit-cyfrin-2024-04-11-cyfrin-wormhole-evm-ntt-v2-2-0].
- **Strata UnstakeCooldown (2025) — design issue, caught in audit**:
  Per-user proxy pool reused clones pointing at outdated implementations
  after `setImplementations` updates, exposing users to deprecated logic
  even after an upstream fix
  [cites: solodit-cyfrin-2025-10-08-cyfrin-strata-tranches-v2-0-2-3].
- **Suzaku VaultFactory (2025) — design issue, caught in audit**:
  Blacklist enforced on `create` but not `migrate`, allowing vaults to
  migrate *into* a known-vulnerable implementation version
  [cites: solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-0-2].
- **Linea RollupRevenueVault (2025) — caught pre-deploy in audit**: New
  implementation shipped `initialize()` with `initializer` modifier, but
  the proxy was already initialized, so the upgrade tx would have
  reverted on mainnet. Fixed by switching to `reinitializer(2)` via a
  separate `initializeRolesAndStorageVariables`
  [cites: solodit-cyfrin-2025-11-03-cyfrin-linea-burn-v2-2-1-1].
- **Linea L2MessageService (2024) — caught pre-deploy in audit**:
  `reinitializePauseTypesAndPermissions` used `reinitializer(6)` on a
  proxy whose stored `_initialized` was 1, mismatched with the
  TokenBridge sibling that used `reinitializer(2)`
  [cites: solodit-cyfrin-2024-11-28-cyfrin-linea-v2-0-2-4].

## References

- corpus entries:
  - rekt-audius-rekt
  - swc-112 (SWC-112: Delegatecall to Untrusted Callee)
  - solodit-trust-security-2023-01-19-lyra-finance-2-0
  - solodit-cyfrin-2025-01-20-cyfrin-stakedotlink-stakingproxy-v2-0-1-1
  - solodit-pashov-audit-group-2023-12-01-vetenet-0-0
  - solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-2-0
  - solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-3-13
  - solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-3-0
  - solodit-cyfrin-2025-06-11-cyfrin-strata-v2-1-2-0
  - solodit-cyfrin-2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2-1-1
  - solodit-zokyo-2022-07-08-stablr-0-0
  - solodit-zokyo-2022-11-15-taunt-token-0-0
  - solodit-zachobront-2023-11-01-fungify-3-1
  - solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-2-0
  - solodit-cyfrin-2025-06-30-cyfrin-linea-spingame-v2-v2-1-1-4
  - solodit-cyfrin-2023-09-12-cyfrin-beanstalk-2-1
  - solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-34
  - solodit-cyfrin-2025-11-03-cyfrin-linea-burn-v2-2-1-1
  - solodit-cyfrin-2024-11-28-cyfrin-linea-v2-0-2-4
  - solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-0-2
  - solodit-cyfrin-2025-10-08-cyfrin-strata-tranches-v2-0-2-3
  - solodit-zokyo-2024-06-30-devve-2-0
  - solodit-auditone-2023-04-06-soonaverse-0-0
  - solodit-zokyo-2023-06-09-narwhal-finance-1-12
  - solodit-cyfrin-2024-04-11-cyfrin-wormhole-evm-ntt-v2-2-0
