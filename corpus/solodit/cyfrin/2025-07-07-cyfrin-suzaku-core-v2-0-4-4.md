---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-4-4
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-07-07T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-07-cyfrin-suzaku-core-v2-0
title: Optimize `_getStakerVaults` to Avoid Redundant External Calls to `activeBalanceOfAt`
vuln_class: []
---

# Optimize `_getStakerVaults` to Avoid Redundant External Calls to `activeBalanceOfAt`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-07-cyfrin-suzaku-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md)_

---

**Description:** The `Rewards::_getStakerVaults` function performs two passes over the vault array to filter vaults with non-zero balances, which doubles the number of external calls to `IVaultTokenized.activeBalanceOfAt`.

```solidity
function _getStakerVaults(address staker, uint48 epoch) internal view returns (address[] memory) {
        address[] memory vaults = middlewareVaultManager.getVaults(epoch);
        uint48 epochStart = l1Middleware.getEpochStartTs(epoch);

        uint256 count = 0;

        // First pass: Count non-zero balance vaults
        for (uint256 i = 0; i < vaults.length; i++) {
            uint256 balance = IVaultTokenized(vaults[i]).activeBalanceOfAt(staker, epochStart, new bytes(0));
            if (balance > 0) {
                count++;
            }
        }

        // Create a new array with the exact number of valid vaults
        address[] memory validVaults = new address[](count);
        uint256 index = 0;

        // Second pass: Populate the new array
        for (uint256 i = 0; i < vaults.length; i++) {
            uint256 balance = IVaultTokenized(vaults[i]).activeBalanceOfAt(staker, epochStart, new bytes(0));
            if (balance > 0) {
                validVaults[index] = vaults[i];
                index++;
            }
        }

        return validVaults;
    }
```

**Recommended Mitigation:** Make the following change to the `_getStakerVaults`:

```diff
function _getStakerVaults(address staker, uint48 epoch) internal view returns (address[] memory) {
    address[] memory vaults = middlewareVaultManager.getVaults(epoch);
    uint48 epochStart = l1Middleware.getEpochStartTs(epoch);
+   address[] memory tempVaults = new address[](vaults.length); // Temporary oversized array
    uint256 count = 0;

-   // First pass: Count non-zero balance vaults
-   for (uint256 i = 0; i < vaults.length; i++) {
-       uint256 balance = IVaultTokenized(vaults[i]).activeBalanceOfAt(staker, epochStart, new bytes(0));
-       if (balance > 0) {
-           count++;
-       }
-   }
-
-   // Create a new array with the exact number of valid vaults
+   // Single pass: Collect valid vaults
+   for (uint256 i = 0; i < vaults.length;) {
+       if (IVaultTokenized(vaults[i]).activeBalanceOfAt(staker, epochStart, new bytes(0)) > 0) {
+           tempVaults[count] = vaults[i];
+           count++;
+       }
+       unchecked { i++; }
+   }
+
+   // Copy to correctly sized array
    address[] memory validVaults = new address[](count);
-   uint256 index = 0;
-
-   // Second pass: Populate the new array
-   for (uint256 i = 0; i < vaults.length; i++) {
-       uint256 balance = IVaultTokenized(vaults[i]).activeBalanceOfAt(staker, epochStart, new bytes(0));
-       if (balance > 0) {
-           validVaults[index] = vaults[i];
-           index++;
-       }
+   for (uint256 i = 0; i < count;) {
+       validVaults[i] = tempVaults[i];
+       unchecked { i++; }
    }

    return validVaults;
}
```

**Suzaku:**
Fixed in commit [2fb0daf](https://github.com/suzaku-network/suzaku-core/commit/2fb0dafd684eeaf11b177602c5047d1e6ce2d715).

**Cyfrin:** Verified.
