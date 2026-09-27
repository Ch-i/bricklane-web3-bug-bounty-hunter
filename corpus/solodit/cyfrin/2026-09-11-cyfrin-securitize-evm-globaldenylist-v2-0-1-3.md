---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-11-cyfrin-securitize-evm-globaldenylist-v2-0-1-3
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-09-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-11-cyfrin-securitize-evm-globaldenylist-v2-0
title: '`GlobalDenyListManager::revokeOperator` is bypassable via inherited `AccessControlUpgradeable::revokeRole,
  renounceRole`, which emit no `OperatorRevoked`'
vuln_class: []
---

# `GlobalDenyListManager::revokeOperator` is bypassable via inherited `AccessControlUpgradeable::revokeRole, renounceRole`, which emit no `OperatorRevoked`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md)_

---

**Description:** `GlobalDenyListManager::grantRole` is overridden so that granting `OPERATOR_ROLE` through the generic AccessControl path still emits the domain event `OperatorAdded`. The two matching removal paths received no such treatment: `revokeRole` and `renounceRole` are inherited from `AccessControlUpgradeable` unchanged and emit only the standard `RoleRevoked`.

An admin calling `revokeRole(OPERATOR_ROLE, operator)` therefore removes the role without emitting `OperatorRevoked`, and an operator calling `renounceRole(OPERATOR_ROLE, self)` does the same unilaterally. Both bypass `GlobalDenyListManager::revokeOperator`, the sanctioned removal path and the only one that emits the domain event.

**Impact:** No `OperatorRevoked` event is emitted; the asymmetry with the `grantRole` override is what marks this as an oversight rather than a design choice: the grant side was hardened specifically to keep the domain events authoritative, and the removal side was left inherited.

**Recommended Mitigation:** Reject `OPERATOR_ROLE` in both inherited entry points, so every operator removal goes through `revokeOperator`:

```solidity
function revokeRole(bytes32 role, address account) public virtual override onlyRole(DEFAULT_ADMIN_ROLE) {
    if (role == OPERATOR_ROLE) revert UseRevokeOperator();
    super.revokeRole(role, account);
}

function renounceRole(bytes32 role, address callerConfirmation) public virtual override {
    if (role == OPERATOR_ROLE) revert UseRevokeOperator();
    super.renounceRole(role, callerConfirmation);
}
```

**Securitize:** Fixed in commits [a09ebfa](https://github.com/securitize-io/bc-global-denylist-manager-sc/commit/a09ebfacb77296788d7dad399cded94f413a5a6a), [4f08c18](https://github.com/securitize-io/bc-global-denylist-manager-sc/commit/4f08c18d3f00db871926b69b7ea5bcc345b3db67).

**Cyfrin:** Verified.
