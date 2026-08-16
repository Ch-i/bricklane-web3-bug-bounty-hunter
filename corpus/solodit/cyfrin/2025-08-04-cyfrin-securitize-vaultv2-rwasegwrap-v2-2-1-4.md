---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2-1-4
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-08-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md
tags:
- firm:cyfrin
- report:2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2
title: Inconsistency between function name and documentation in `getUnderlyingAsset`
vuln_class: []
---

# Inconsistency between function name and documentation in `getUnderlyingAsset`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md)_

---

**Description:** The `RWASegWrap::getUnderlyingAsset` function has inconsistent naming and documentation. The function name `getUnderlyingAsset` suggests it should return the underlying asset address (the RWA token), but the interface documentation states "Gets the vault address for a given asset ID", indicating it should return the vault contract address.

The current implementation returns `vaults[id]`, which is the vault contract address, aligning with the documentation but contradicting the function name. This creates confusion in the codebase where developers might expect the function to return the underlying asset address based on its name, when it actually returns the vault address.

```solidity
// Interface documentation says: "Gets the vault address for a given asset ID"
// But the function name suggests it returns the underlying asset
function getUnderlyingAsset(uint256 id) external view returns (address);

// Implementation returns vault address, matching documentation but not the name
function getUnderlyingAsset(uint256 id) public virtual view override returns (address) {
    return vaults[id]; // Returns vault contract address
}
```

In the ERC4626 vault architecture, there's a clear distinction between:
- Vault address: The contract address of the ERC4626 vault (share token contract)
- Underlying asset address: The address of the token that the vault accepts as deposits (obtainable via `vault.asset()`)

The same issue exists in `SecuritizeRWASegWrap` as it inherits from `RWASegWrap` and doesn't override this function.

**Impact:** The inconsistency between the function name and documentation creates confusion about the function's intended behavior, potentially leading to integration errors where developers expect the underlying asset address but receive the vault address.

**Recommended Mitigation:** Choose one of the following approaches to resolve the inconsistency:

Option 1 - Rename function to match documentation:
```diff
/**
 * @notice Gets the vault address for a given asset ID.
 * @dev Returns zero address if not found.
 */
- function getUnderlyingAsset(uint256 id) external view returns (address);
+ function getVaultAddress(uint256 id) external view returns (address);
```

Option 2 - Update documentation to match function name and fix implementation:
```diff
/**
- * @notice Gets the vault address for a given asset ID.
+ * @notice Gets the underlying asset address for a given asset ID.
 * @dev Returns zero address if not found.
 */
function getUnderlyingAsset(uint256 id) external view returns (address);

// And update implementation:
function getUnderlyingAsset(uint256 id) public virtual view override returns (address) {
-   return vaults[id];
+   return vaults[id] != address(0) ? IERC4626(vaults[id]).asset() : address(0);
}
```

**Securitize:** Fixed in [23f879](https://github.com/securitize-io/bc-rwa-seg-wrap-sc/commit/23f87990fb28f6c74344cae415ef1f7e9617da4c).

**Cyfrin:** Verified.
