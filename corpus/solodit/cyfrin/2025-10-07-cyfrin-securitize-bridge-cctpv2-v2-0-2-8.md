---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0-2-8
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-10-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0
title: Misleading event emission in `USDCBridgeV2::addBridgeCaller, removeBridgeCaller`
  when role was not granted or revoked
vuln_class: []
---

# Misleading event emission in `USDCBridgeV2::addBridgeCaller, removeBridgeCaller` when role was not granted or revoked

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md)_

---

**Description:** `AccessControlUpgradeable::_grantRole,_revokeRole` [return](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/master/contracts/access/AccessControlUpgradeable.sol#L204-L230) `bool` to indicate whether the role has been granted or revoked.

But `USDCBridgeV2::removeBridgeCaller, addBridgeCaller` ignore the returned `bool` since they call the `public` functions and always emits an event even if no role was granted or revoked.

**Recommended Mitigation:**
```diff
    function addBridgeCaller(address _account) external override addressNotZero(_account) onlyRole(DEFAULT_ADMIN_ROLE) {
-       grantRole(BRIDGE_CALLER, _account);
-       emit BridgeCallerAdded(_account);
+       if(_grantRole(BRIDGE_CALLER, _account)) emit BridgeCallerAdded(_account);
    }

    function removeBridgeCaller(address _account) external override addressNotZero(_account) onlyRole(DEFAULT_ADMIN_ROLE) {
-       revokeRole(BRIDGE_CALLER, _account);
-       emit BridgeCallerRemoved(_account);
+       if(_revokeRole(BRIDGE_CALLER, _account)) emit BridgeCallerRemoved(_account);
    }
```

**Securitize:** Acknowledged.
