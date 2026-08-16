---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-3-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: When emitting events don't read known values from storage
vuln_class: []
---

# When emitting events don't read known values from storage

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** When emitting events don't read known values from storage; for example in `SecuritizeAmmNavProvider::_resetBaseline`:
```diff
    function _resetBaseline(uint256 newBase, uint256 newQuote) internal {
        require(newBase > 0, "newBase=0");
        require(newQuote > 0, "newQuote=0");

        baseReserves = newBase;
        quoteReserves = newQuote;

        baseBaseline = newBase;
        quoteBaseline = newQuote;

        k = newBase * newQuote;

-       emit BaselineReset(baseBaseline, quoteBaseline);
+       emit BaselineReset(newBase, newQuote);
    }
```

Similar optimizations can be made in:
* `AllowanceLiquidityProvider::setAllowanceProviderWallet`
* `CollateralLiquidityProvider::setExternalCollateralRedemption, setCollateralProvider`
* `BaseOffRamp::updateLiquidityProvider` at this line `uint256 _liquidityDecimals = IERC20Metadata(address(liquidityProvider.liquidityToken())).decimals();` - use `_liquidityProvider` instead of `liquidityProvider`
* `BaseOffRamp::toggleTwoStepTransfer`
* `PublicStockOffRamp::updateNavProvider`
* `SecuritizeOffRamp::updateNavProvider`
* `AllowanceAssetProvider::setAllowanceProviderWallet`
* `BaseOnRamp::updateMinSubscriptionAmount, toggleInvestorSubscription, toggleTwoStepTransfer`

**Securitize:** Fixed in commits [fe9f910](https://bitbucket.org/securitize_dev/bc-nav-provider-sc/commits/fe9f910f1fe6b73aa63171a2e8f4cb55f0092123), [5d39cc1](https://github.com/securitize-io/bc-on-off-ramp-sc/commit/5d39cc1122fabdef280dd0da4ecc5d984f6355a1).

**Cyfrin:** Verified.
