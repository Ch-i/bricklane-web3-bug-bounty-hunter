---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-4-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-07-07T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-07-cyfrin-suzaku-core-v2-0
title: Gas optimization for `getVaults` function
vuln_class: []
---

# Gas optimization for `getVaults` function

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-07-cyfrin-suzaku-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md)_

---

**Description:** The `MiddlewareVaultManager::getVaults` uses an inefficient pattern that iterates through the entire list of vaults twice. The first iteration counts the number of active vaults, while the second iteration builds the array of active vaults.

This implementation:

- Makes the same `vaults.atWithTimes(i)` calls twice
- Performs the same `_wasActiveAt()` calculation twice for each vault
- Results in unnecessary gas consumption, especially as the number of vaults grows

**Recommended Mitigation:** Consider refactoring the function to use a single-pass approach that eliminates the redundant iteration by caching the active vaults in the first loop.

```diff solidity
function getVaults(
    uint48 epoch
) external view returns (address[] memory) {
    uint256 vaultCount = vaults.length();
    uint48 epochStart = middleware.getEpochStartTs(epoch);

    // Early return for empty vaults
    if (vaultCount == 0) {
        return new address[](0);
    }

++    address[] memory tempVaults = new address[](vaultCount);
    uint256 activeCount = 0;

    // Single pass through the vaults
    for (uint256 i = 0; i < vaultCount; i++) {
        (address vault, uint48 enabledTime, uint48 disabledTime) = vaults.atWithTimes(i);
        if (_wasActiveAt(enabledTime, disabledTime, epochStart)) {
++          tempVaults[activeCount] = vault;
            activeCount++;
        }
    }

    // Create the final result array with correct size
    address[] memory activeVaults = new address[](activeCount);
-- uint256 activeIndex = 0;
-- for (uint256 i = 0; i < vaultCount; i++) {
--      (address vault, uint48 enabledTime, uint48 disabledTime) = vaults.atWithTimes(i);
--      if (_wasActiveAt(enabledTime, disabledTime, epochStart)) {
--          activeVaults[activeIndex] = vault;
--          activeIndex++;
--       }
--    }
++    for (uint256 i = 0; i < activeCount; i++) {
++       activeVaults[i] = tempVaults[i];
++    }

    return activeVaults;
}
```

**Suzaku:**
Fixed in commit [59a0109](https://github.com/suzaku-network/suzaku-core/commit/59a01095a1940aae4e75a87580695ca3e4d99712).

**Cyfrin:** Verified.
