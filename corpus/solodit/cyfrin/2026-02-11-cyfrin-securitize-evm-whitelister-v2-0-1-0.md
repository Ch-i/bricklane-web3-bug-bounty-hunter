---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-11-cyfrin-securitize-evm-whitelister-v2-0-1-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-02-11T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-11-cyfrin-securitize-evm-whitelister-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-11-cyfrin-securitize-evm-whitelister-v2-0
title: '`BaseWhitelister::addOperator, removeOperator` should use `_grantRole` and
  `_revokeRole` directly and only emit events when they return `true`'
vuln_class: []
---

# `BaseWhitelister::addOperator, removeOperator` should use `_grantRole` and `_revokeRole` directly and only emit events when they return `true`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-11-cyfrin-securitize-evm-whitelister-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-11-cyfrin-securitize-evm-whitelister-v2.0.md)_

---

**Description:** `BaseWhitelister::addOperator, removeOperator` use public functions `grantRole, revokeRole`; this is not ideal as these functions:
1) use [modifier](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/master/contracts/access/AccessControlUpgradeable.sol#L141) `onlyRole(getRoleAdmin(role))` but the access control has already been applied via modifier `onlyRole(DEFAULT_ADMIN_ROLE)`

2) call `_grantRole, _revokeRole` which [return](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/master/contracts/access/AccessControlUpgradeable.sol#L203) `bool` - if the returned `bool` is `false, the `ProtocolAuthorized, ProtocolRevoked` event would still be emitted even though no access was granted or revoked

**Recommended Mitigation:** `BaseWhitelister::addOperator, removeOperator` should directly call `_grantRole, _revokeRole` and only emit the events if the returned `bool` is `true`:
```solidity
    function addOperator(address operator) external onlyRole(DEFAULT_ADMIN_ROLE) notZeroAddress(operator) {
        if(_grantRole(OPERATOR_ROLE, operator)) emit ProtocolAuthorized(operator);
    }

    function removeOperator(address operator) external onlyRole(DEFAULT_ADMIN_ROLE) notZeroAddress(operator) {
        if(_revokeRole(OPERATOR_ROLE, operator)) emit ProtocolRevoked(operator);
    }
```

**Securitize:** Fixed in commit [c0bd66b](https://github.com/securitize-io/bc-vault-whitelister/commit/c0bd66b144d45a281b672d69eac0cc3c3c4c7dc8).

**Cyfrin:** Verified.
