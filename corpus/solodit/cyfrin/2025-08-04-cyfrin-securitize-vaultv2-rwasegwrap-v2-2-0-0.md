---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2-0-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-08-04T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md
tags:
- firm:cyfrin
- report:2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2
title: Shared configuration parameters across different asset types in vault deployers
  leads to incorrect pricing and fee calculations
vuln_class: []
---

# Shared configuration parameters across different asset types in vault deployers leads to incorrect pricing and fee calculations

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md)_

---

**Description:** The `VaultDeployer` and `SecuritizeVaultDeployer` contracts maintain shared configuration parameters (`navProvider`, `feeManager`, `redemptionAddress`) that are applied to all deployed vaults regardless of their underlying asset type. When `SegregatedVaultDeployer::deploy()` or `SecuritizeVaultDeployer::deploy()` is called with different `assetToken` and `liquidationToken` parameters to support various vault types, the same `navProvider` is used across all deployments. This creates a critical architectural flaw because different RWA assets require asset-specific NAV providers for accurate valuation.

In `SecuritizeVaultV2`, the `navProvider.rate()` is extensively used in critical functions like `_convertToShares()`, `_convertToAssets()`, and `getShareValue()` to determine share-to-asset conversion ratios. When vaults for different assets (e.g., real estate tokens vs commodity tokens) share the same NAV provider, the pricing calculations become incorrect for at least one of the asset types.

Similar issues exist with:
- `SecuritizeVaultDeployer.feeManager` - applies the same fee logic to all asset types
- `SecuritizeVaultDeployer.redemptionAddress` - uses the same redemption contract for different assets that may require different redemption mechanisms

Note that `SegregatedVault` does not use `navProvider` in its calculations, so it is not directly affected by this issue, but the architecture problem persists in the deployment pattern.

**Impact:** Users depositing assets into vaults with incorrect NAV providers will receive wrong share amounts, leading to economic losses and potential exploitation opportunities where attackers can deposit low-value assets but receive shares calculated using high-value asset NAV rates.

```solidity
// In SecuritizeVaultDeployer::deploy()
BeaconProxy proxy = new BeaconProxy(
    upgradeableBeacon,
    abi.encodeWithSelector(
        SecuritizeVaultV2(payable(address(0))).initializeV2.selector,
        name,
        symbol,
        assetToken,      // Different per deployment
        redemptionAddress, // Same for all deployments - ISSUE
        liquidationToken,
        navProvider,     // Same for all deployments - ISSUE
        feeManager       // Same for all deployments - ISSUE
    )
);
```

**Recommended Mitigation:** We understand that these parameters are meant to be managed by only the admin, and that is why it's managed by the contract instead of allowing users to specify in the deploy function. We recommend the team consider either of below two solutions.

1. Modify the vault deployer architecture to support asset-specific configurations. Below is an example implementation.

```diff
+ mapping(address => address) public assetNavProviders;
+ mapping(address => address) public assetFeeManagers;
+ mapping(address => address) public assetRedemptionAddresses;

+ function setAssetConfiguration(
+     address assetToken,
+     address navProvider,
+     address feeManager,
+     address redemptionAddress
+ ) external onlyRole(DEFAULT_ADMIN_ROLE) {
+     assetNavProviders[assetToken] = navProvider;
+     assetFeeManagers[assetToken] = feeManager;
+     assetRedemptionAddresses[assetToken] = redemptionAddress;
+ }
```
2. If the intention is to have one deployer for every pair of asset token ad liquid token, store the asset token address and liquid token address in the deployer with the nav provider together and remove the `assetToken` adn `liquidToken` parameters from the deploy function.

**Securitize:** Fixed in commit [05044b](https://github.com/securitize-io/bc-rwa-seg-wrap-sc/commit/05044b3f10d66d82ad134fc73f712c62ba5796e2).

**Cyfrin:** Verified.

\clearpage
