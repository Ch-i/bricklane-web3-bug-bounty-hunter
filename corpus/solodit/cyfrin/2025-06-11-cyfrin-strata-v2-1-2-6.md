---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-11-cyfrin-strata-v2-1-2-6
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-06-11T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-11-cyfrin-strata-v2-1
title: '`MetaVault::addVault` should enforce identical underlying base asset'
vuln_class: []
---

# `MetaVault::addVault` should enforce identical underlying base asset

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-11-cyfrin-strata-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md)_

---

**Description:** When supporting additional vaults, `MetaVault::addVault` should enforce that the new vault being supported has an identical underlying base asset as itself. Otherwise:
* `redeemRequiredBaseAssets` won't work as expected since the newly supported vault doesn't have the same base asset
* `MetaVault::depositedBase` will become corrupt, especially if the underlying asset tokens use different decimal precision

**Proof of Concept:**
```solidity
function test_vaultSupportedWithDifferentUnderlyingAsset() external {
    // create ERC4626 vault with different underlying ERC20 asset
    MockUSDe differentERC20 = new MockUSDe();
    MockERC4626 newSupportedVault = new MockERC4626(differentERC20);

    // verify pUSDe doesn't have same underlying asset as new vault
    assertNotEq(pUSDe.asset(), newSupportedVault.asset());

    // but still allows it to be added
    pUSDe.addVault(address(newSupportedVault));

    // this breaks `MetaVault::redeemRequiredBaseAssets` since
    // the newly supported vault doesn't have the same base asset
}
```

**Recommended Mitigation:** Change `MetaVault::addVaultInner`:
```diff
    function addVaultInner (address vaultAddress) internal {
+       IERC4626 newVault = IERC4626(vaultAddress);
+       require(newVault.asset() == asset(), "Vault asset mismatch");
```

**Strata:** Fixed in commits [9e64f09](https://github.com/Strata-Money/contracts/commit/9e64f09af6eb927c9c736796aeb92333dbb72c18), [706c2df](https://github.com/Strata-Money/contracts/commit/706c2df3f2caf6651b1d8e858beb5097dbd7d066).

**Cyfrin:** Verified.
