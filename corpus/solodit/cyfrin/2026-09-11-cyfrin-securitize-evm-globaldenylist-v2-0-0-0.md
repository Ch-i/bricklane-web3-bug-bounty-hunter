---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-11-cyfrin-securitize-evm-globaldenylist-v2-0-0-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-09-11T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-11-cyfrin-securitize-evm-globaldenylist-v2-0
title: '`GlobalDenyListManager::changeAdmin` zero-admin guard is bypassed by inherited
  `AccessControlUpgradeable::revokeRole, renounceRole`, permanently bricking admin-gated
  functions'
vuln_class: []
---

# `GlobalDenyListManager::changeAdmin` zero-admin guard is bypassed by inherited `AccessControlUpgradeable::revokeRole, renounceRole`, permanently bricking admin-gated functions

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md)_

---

**Description:** `GlobalDenyListManager::changeAdmin` enforces that a valid admin always exists: `addressNotZero` rejects `address(0)` and `CannotTransferAdminToSelf` rejects a self-target, with an in-code comment spelling out that zero admins would brick every gated function. `GlobalDenyListManager::grantRole` is likewise overridden to add `onlyRole` and `addressNotZero`.

`revokeRole` and `renounceRole` are inherited from `AccessControlUpgradeable` and are not overridden. `DEFAULT_ADMIN_ROLE` is its own role admin, so the sole admin can strip their own role through either path: `renounceRole` only requires `callerConfirmation` to equal `msg.sender`, and `revokeRole` only requires the caller to hold `getRoleAdmin(DEFAULT_ADMIN_ROLE)`, which the admin satisfies by definition. The invariant is enforced on one of the three paths that can remove it.

**Impact:** After either call, `GlobalDenyListManager::isAdmin` returns false for the former admin and no account holds `DEFAULT_ADMIN_ROLE`. Every admin-gated function becomes permanently unreachable: `changeAdmin`, `addOperator`, `revokeOperator`, `grantRole`, and `BaseRBACContract::pause, unpause, _authorizeUpgrade`. No admin can be reinstated, and because `_authorizeUpgrade` is itself admin-gated, no upgrade can be authorized to recover.

The worst case combines this with the pause state. An admin that pauses and then renounces leaves the contract permanently paused: operators cannot call `addToGlobalDenylist` or `removeFromGlobalDenylist` because of `whenNotPaused`, no admin exists to `unpause`, and no admin exists to authorize an upgrade out of that state. The global denylist is frozen with no recovery path.

This breaches section `4.2 Role separation is procedural, not enforced` from `GlobalDenylist-AuditScope.md` which says:

> - `changeAdmin` guards self-transfer (`CannotTransferAdminToSelf`) and performs grant and revoke as independent, non-short-circuited statements. Verify no remaining sequence leaves the contract with zero admins, or silently retains the deployer as admin.

**Recommended Mitigation:** Route every `DEFAULT_ADMIN_ROLE` transition through `changeAdmin` by rejecting that role in both inherited entry points:

```solidity
function revokeRole(bytes32 role, address account) public virtual override onlyRole(DEFAULT_ADMIN_ROLE) {
    if (role == DEFAULT_ADMIN_ROLE) revert CannotRevokeAdminRole();
    super.revokeRole(role, account);
}

function renounceRole(bytes32 role, address callerConfirmation) public virtual override {
    if (role == DEFAULT_ADMIN_ROLE) revert CannotRenounceAdminRole();
    super.renounceRole(role, callerConfirmation);
}
```

Also consider whether more than one admin should exist; currently `grantRole` accepts an arbitrary role so `grantRole(DEFAULT_ADMIN_ROLE, account)` can already create a second admin.

If more than one admin is intended the above recommended mitigation should instead block removal of the last remaining admin, which `AccessControlEnumerableUpgradeable` supports through `getRoleMemberCount`.

**Securitize:** Acknowledged; this scenario requires the admin to take a deliberate, avoidable action against their own interest. `changeAdmin` (the intended, guarded path) carries an equivalent self-inflicted risk that no code change eliminates: transferring admin to the wrong address also permanently locks the caller out, with the same blast radius (no admin, no path to `_authorizeUpgrade`). Restricting `revokeRole/renounceRole` narrows one specific way to make that mistake without addressing the underlying class of risk.

There's also a real cost on the other side: this contract can technically hold more than one `DEFAULT_ADMIN_ROLE` account (nothing prevents `grantRole(DEFAULT_ADMIN_ROLE, account`) from creating a second admin). If that ever happens, blocking `revokeRole/renounceRole` removes the only way to remove a specific admin without their cooperation; `changeAdmin` only ever transfers the caller's own role, it cannot target-remove another admin. So the mitigation trades a self-inflicted single-admin mistake (already possible via `changeAdmin`) for a real operational dead-end in the multi-admin case.

Given both paths carry comparable operator-error risk, and the fix actively removes a needed capability in the multi-admin case, we're leaving `revokeRole/renounceRole` as inherited from `AccessControlUpgradeable`, unguarded for `DEFAULT_ADMIN_ROLE`.
