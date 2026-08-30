---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-11-cyfrin-strata-v2-1-2-7
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-06-11T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-11-cyfrin-strata-v2-1
title: '`pUSDeVault::startYieldPhase` should not remove supported vaults from being
  supported or should prevent new supported vaults once in the yield phase'
vuln_class: []
---

# `pUSDeVault::startYieldPhase` should not remove supported vaults from being supported or should prevent new supported vaults once in the yield phase

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-11-cyfrin-strata-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md)_

---

**Description:** The intention of `pUSDeVault::startYieldPhase` is to convert assets from existing supported vaults into `USDe` in order to then stake the vault's total `USDe` into the `sUSDe` vault.

However because this ends up calling `MetaVault::removeVaultAndRedeemInner`, all the supported vaults are also removed after their assets are converted.

But new vaults can continue to be added during the yield phase, so it makes no sense to remove all supported vaults at this time.

**Impact:** The contract owner will need to re-add all the previously enabled supported vaults causing all user deposits to revert until this is done.

**Proof Of Concept:**
```solidity
function test_supportedVaultsRemovedWhenYieldPhaseEnabled() external {
    // supported vault prior to yield phase
    assertTrue(pUSDe.isAssetSupported(address(eUSDe)));

    // user1 deposits $1000 USDe into the main vault
    uint256 user1AmountInMainVault = 1000e18;
    USDe.mint(user1, user1AmountInMainVault);

    vm.startPrank(user1);
    USDe.approve(address(pUSDe), user1AmountInMainVault);
    uint256 user1MainVaultShares = pUSDe.deposit(user1AmountInMainVault, user1);
    vm.stopPrank();

    // admin triggers yield phase on main vault
    pUSDe.startYieldPhase();

    // supported vault was removed when initiating yield phase
    assertFalse(pUSDe.isAssetSupported(address(eUSDe)));

    // but can be added back in?
    pUSDe.addVault(address(eUSDe));
    assertTrue(pUSDe.isAssetSupported(address(eUSDe)));

    // what was the point of removing it if it can be re-added
    // and used again during the yield phase?
}
```

**Recommended Mitigation:** Don't remove all supported vaults when calling `pUSDeVault::startYieldPhase`; just convert their assets to `USDe` but continue to allow the vaults themselves to be supported and accept future deposits.

Alternatively don't allow supported vaults to be added during the yield phase (apart from sUSDe which is added when the yield phase is enabled). In this case removing them when enabled the yield phase is fine, but add code to disallow adding them once the yield phase is enabled.

**Strata:** Fixed in commit [076d23e](https://github.com/Strata-Money/contracts/commit/076d23e2446ad6780b2c014d66a46e54425a8769#diff-34cf784187ffa876f573d51b705940947bc06ec85f8c303c1b16a4759f59524eR190) by no longer allowing adding new supporting vaults during the yield phase.

**Cyfrin:** Verified.
