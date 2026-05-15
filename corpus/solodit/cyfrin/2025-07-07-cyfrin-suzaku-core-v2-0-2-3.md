---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-2-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-07-07T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-07-cyfrin-suzaku-core-v2-0
title: Incorrect vault status determination in `MiddlewareVaultManager`
vuln_class: []
---

# Incorrect vault status determination in `MiddlewareVaultManager`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-07-cyfrin-suzaku-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md)_

---

**Description:** The `MiddlewareVaultManager::_wasActiveAt()`  determines whether a vault was active at a specific timestamp. This function is used by the `getVaults()` method to filter active vaults for a given epoch.

The current implementation of `_wasActiveAt()` incorrectly considers a vault to be active at the exact timestamp when it was disabled. The function returns true when:

- The vault has been enabled (enabledTime != 0)
- The vault was enabled at or before the timestamp (enabledTime <= timestamp)
- AND EITHER:
       - The vault was never disabled (disabledTime == 0) OR
       - The vault's disabled timestamp is greater than or equal to the query timestamp (disabledTime >= timestamp)


```solidity
// Current implementation
function _wasActiveAt(uint48 enabledTime, uint48 disabledTime, uint48 timestamp) private pure returns (bool) {
    return enabledTime != 0 && enabledTime <= timestamp && (disabledTime == 0 || disabledTime >= timestamp);
}
```

The issue is with the third condition (`disabledTime >= timestamp`). This logic means that a vault disabled exactly at the timestamp being queried (e.g., at the start of an epoch) would still be considered active for that epoch, which is counterintuitive. Typically, when an entity is disabled at a specific timestamp, it should be considered inactive from that timestamp forward.


**Impact:** Vaults disabled exactly at an epoch boundary to be incorrectly included as active in that epoch.

**Recommended Mitigation:** Consider modifying the `_wasActiveAt()` function to use a strict inequality for the disablement check.

**Suzaku:**
Fixed in commit [9bbbcfc](https://github.com/suzaku-network/suzaku-core/pull/155/commits/9bbbcfce7bedd1dd4e60fdf55bb5f13ba8ab4847).

**Cyfrin:** Verified.
