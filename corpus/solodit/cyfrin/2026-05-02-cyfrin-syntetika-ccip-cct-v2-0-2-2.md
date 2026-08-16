---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-2-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-05-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-02-cyfrin-syntetika-ccip-cct-v2-0
title: Direct `grantRole, revokeRole` bypasses the 2-step role mechanism across `Minter,
  HilToken, StakingVault, Distributor`
vuln_class: []
---

# Direct `grantRole, revokeRole` bypasses the 2-step role mechanism across `Minter, HilToken, StakingVault, Distributor`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** The protocol's stated threat model - "the 2-step admin system prevents a leaked admin private key from destroying the protocol in a single transaction" - relies on role transitions going through per-contract request/execute pairs (e.g. `HilToken::requestMinterChange` -> wait -> `setMinter`). Each setter pair updates both a storage pointer and the corresponding OZ role behind a 1-day waiting period.

However, the role itself is grantable through the standard OpenZeppelin surface: `AccessControlUpgradeable::grantRole` is `public`, gated only by `onlyRole(getRoleAdmin(role))`, and every custom role's admin is `DEFAULT_ADMIN_ROLE`. No in-scope contract overrides `grantRole`/`revokeRole`, calls `_setRoleAdmin`, or uses `AccessControlDefaultAdminRulesUpgradeable`. Because role membership - not the storage pointer - is what authorizes `HilToken::mint`, `Minter::transferToCustody, pause`, `Distributor::realizeLosses`.

`DEFAULT_ADMIN_ROLE` itself is the least protected role - no delay, no 2-step, no acceptance step. A compromised admin can grant it to an attacker in one tx, or renounce it and permanently brick every `onlyRole(DEFAULT_ADMIN_ROLE)` function (including `_authorizeUpgrade`, freezing the UUPS proxy forever).

Proof - `HilToken` mint-and-drain, single block, single leaked admin key:

```
Tx1: HilToken.grantRole(MINTER_ROLE, attackerEOA)       // passes: onlyRole(DEFAULT_ADMIN_ROLE)
Tx2: HilBTC.mint(attackerEOA, type(uint128).max)        // passes: onlyRole(MINTER_ROLE)
Tx3: Minter.whitelistAddress(attackerEOA, true)         // single-step admin
Tx4: Minter.redeem(type(uint128).max)                   // drains wBTC/USDC in Minter
```

The same pattern unlocks every other role-gated capability across `Minter, StakingVault, Distributor`.

Off-chain monitoring built around the 2-step events (`MinterChangeRequested`/`MinterChanged`) misses this entirely - only the raw OZ `RoleGranted` event fires, and `$.minter`/`$.distributor` pointers stay stale.

Sources: `Minter.sol:15,34-41`; `HilToken.sol:7,126-141`; `StakingVault.sol:26,138-148`; `Distributor.sol:4`; `deposit-registry/contracts/ComplianceCheckerUpgradeable.sol:6`.

**Impact:** Categorical violation of the stated "leaked admin key cannot destroy the protocol in a single tx" invariant. Every role-gated capability is reachable in a single transaction after an admin-key compromise.

**Recommended Mitigation:** Gate the role grant itself, not just the storage pointer. Any of the following (ideally combined):

1. Override `grantRole`/`revokeRole` for protected roles to either reject direct calls (forcing management through the 2-step `set*` functions) or enforce the same waiting-period check before calling `super`.
2. Migrate `DEFAULT_ADMIN_ROLE` handling to `AccessControlDefaultAdminRulesUpgradeable` - 2-step + delay on admin transfer, blocks naive `renounceRole`.
3. Use `_setRoleAdmin` to route every custom role through a `ROLE_ADMIN_ROLE` held by a timelock contract.
4. Hold the admin key in a multisig + on-chain timelock at deployment level, so the timelock provides the delay the 2-step pattern was intended to provide.

**Syntetika:** Fixed in commit [`5a7840a`](https://github.com/SyntetikaLabs/monorepo/commit/5a7840a3033753e5504d581d9e362d4454fb7f62)

**Cyfrin:** Verified. 2-step change process for all roles implemented.
