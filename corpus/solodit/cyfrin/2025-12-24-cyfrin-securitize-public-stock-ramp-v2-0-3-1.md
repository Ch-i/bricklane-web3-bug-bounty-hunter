---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-3-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: Emit events first to refactor away local variables storing previous values
vuln_class: []
---

# Emit events first to refactor away local variables storing previous values

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** When values are being changed, emit events first to refactor away local variables storing previous values. For example in `SecuritizeAmmNavProvider::setPriceScaleFactor`:
```diff
    function setPriceScaleFactor(uint256 newScaleFactor) external onlyRole(DEFAULT_ADMIN_ROLE) {
        require(newScaleFactor > 0, "scaleFactor = 0");

-       uint256 oldScaleFactor = priceScaleFactor;
+       emit PriceScaleFactorUpdated(priceScaleFactor, newScaleFactor);
        priceScaleFactor = newScaleFactor;

-       emit PriceScaleFactorUpdated(oldScaleFactor, newScaleFactor);
    }
```

Similar optimizations can be made in:
* `SecuritizeInternalNavProvider::setRate`
* `MbpsFeeManager::setFeePercentageMBPS, setFeeCollector`
* `AllowanceLiquidityProvider::setAllowanceProviderWallet`
* `CollateralLiquidityProvider::setExternalCollateralRedemption, setCollateralProvider`
* `BaseOffRamp::updateLiquidityProvider`
* `PublicStockOffRamp::updateNavProvider`
* `SecuritizeOffRamp::updateNavProvider`
* `AllowanceAssetProvider::setAllowanceProviderWallet`
* `SecuritizeOnRamp::updateNavProvider`
* `BaseOnRamp::updateAssetProvider, updateMinSubscriptionAmount`
* `PublicStockOnRamp::updateNavProvider`

**Securitize:** Fixed in commits [41538fa](https://bitbucket.org/securitize_dev/bc-nav-provider-sc/commits/41538faf0df8e31fd4a51f2a478fc6a48a7d6f3a), [7f500c1](https://github.com/securitize-io/bc-on-off-ramp-sc/commit/7f500c1d40da961f709fdeeb9551ef1b6f258363).

**Cyfrin:** Verified.
