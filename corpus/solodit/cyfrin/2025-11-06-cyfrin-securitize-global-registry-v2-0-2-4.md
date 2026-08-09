---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-06-cyfrin-securitize-global-registry-v2-0-2-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-11-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-06-cyfrin-securitize-global-registry-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-06-cyfrin-securitize-global-registry-v2-0
title: Inherited `AccessControlUpgradeable` functions bypass some validation checks
vuln_class: []
---

# Inherited `AccessControlUpgradeable` functions bypass some validation checks

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-06-cyfrin-securitize-global-registry-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-06-cyfrin-securitize-global-registry-v2.0.md)_

---

**Description:** The `GlobalRegistryService` contract implements custom wrapper functions (`addOperator()`, `revokeOperator()`, `changeAdmin()`) with additional safety checks and event emissions on top of OpenZeppelin's `AccessControlUpgradeable`. However, the contract fails to override the underlying public functions from `AccessControlUpgradeable`, allowing admins and operator to bypass some validation checks.

The contract creates wrapper functions with validation:
```solidity
function addOperator(address operator)
    external virtual override
    onlyRole(DEFAULT_ADMIN_ROLE)
    addressNotZero(operator)  // Safety check
{
    _grantRole(OPERATOR_ROLE, operator);
    emit OperatorAdded(operator);
}

function changeAdmin(address newAdmin)
    external virtual override
    onlyRole(DEFAULT_ADMIN_ROLE)
    addressNotZero(newAdmin)  // Safety check
{
    _grantRole(DEFAULT_ADMIN_ROLE, newAdmin);
    _revokeRole(DEFAULT_ADMIN_ROLE, _msgSender());
    emit AdminChanged(newAdmin);
}
```

But the underlying OpenZeppelin functions remain publicly accessible without overrides:
```solidity
function grantRole(bytes32 role, address account) public virtual onlyRole(getRoleAdmin(role)) {
    _grantRole(role, account);
}

function revokeRole(bytes32 role, address account) public virtual onlyRole(getRoleAdmin(role)) {
    _revokeRole(role, account);
}

function renounceRole(bytes32 role, address callerConfirmation) public virtual {
    if (callerConfirmation != _msgSender()) {
        revert AccessControlBadConfirmation();
    }
    _revokeRole(role, callerConfirmation);
}
```

**Impact:** Two unlikely problems could occur:

* Admin can renounce their role without assigning a successor, permanently bricking the contract (This can be done through `AccessControlUpgradeable::renounceRole`)
* Operator adding directly via `AccessControlUpgradeable::grantRole` won't emit the `OperatorAdded` event

**Recommended Mitigation:** Consider overriding default functions to revert which not going to be used in the inherited `AccessControlUpgradeable` contract.

**Securitize:** **Cyfrin:**
