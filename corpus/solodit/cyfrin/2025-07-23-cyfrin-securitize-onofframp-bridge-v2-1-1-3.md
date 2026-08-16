---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1-1-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-07-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1
title: Calculation of available liquidity in `CollateralLiquidityProvider::availableLiquidity`
  assumes 1:1 ratio between collateral asset and liquidity tokens
vuln_class: []
---

# Calculation of available liquidity in `CollateralLiquidityProvider::availableLiquidity` assumes 1:1 ratio between collateral asset and liquidity tokens

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md)_

---

**Description:** The `CollateralLiquidityProvider::availableLiquidity` function incorrectly returns the balance of the collateral asset held by the collateral provider, assuming a 1:1 ratio between the collateral asset and the liquidity tokens that will actually be provided to redeemers. This assumption is flawed because the actual liquidity supplied to redeemers goes through the `externalCollateralRedemption.redeem()` function, which may apply fees, exchange rates, or other conversion mechanisms that break the 1:1 assumption.

```solidity
function availableLiquidity() external view returns (uint256) {
    return IERC20(externalCollateralRedemption.asset()).balanceOf(collateralProvider);
}

function _availableLiquidity() private view returns (uint256) {
    return IERC20(externalCollateralRedemption.asset()).balanceOf(collateralProvider);
}

function supplyTo(
    address redeemer,
    uint256 amount,
    uint256 minOutputAmount
) public whenNotPaused onlySecuritizeRedemption {
    if (amount > _availableLiquidity()) {
        revert InsufficientLiquidity(amount, _availableLiquidity());
    }

    // ... collateral transfer and redemption logic ...

    // The actual liquidity provided is calculated here, not the raw collateral amount
    uint256 assetsAfterExternalCollateralRedemptionFee = externalCollateralRedemption.calculateLiquidityTokenAmount(
        amount
    );

    liquidityToken.transfer(redeemer, assetsAfterExternalCollateralRedemptionFee);
}
```

When `CollateralLiquidityProvider::supplyTo` is called, the flow involves: transferring collateral assets from the collateral provider, calling `externalCollateralRedemption.redeem()` to convert collateral to liquidity tokens, calculating the actual liquidity amount using `externalCollateralRedemption.calculateLiquidityTokenAmount()`, and finally transferring the calculated liquidity tokens to the redeemer.
The `availableLiquidity()` function should query the external redemption contract to determine the actual liquidity that can be provided, rather than using the raw collateral asset balance. (e.g. `externalCollateralRedemption.calculateLiquidityTokenAmount(IERC20(externalCollateralRedemption.asset()).balanceOf(collateralProvider));`

Additionally, the external `availableLiquidity()` function duplicates the logic of the internal `_availableLiquidity()` function instead of calling it, which goes against the intended design pattern and creates unnecessary code duplication.

**Impact:** Users and integrating systems may receive incorrect information about available liquidity, potentially leading to failed transactions when the actual convertible liquidity is less than the reported collateral asset balance.

**Recommended Mitigation:** Update the `availableLiquidity()` function to calculate the actual liquidity that can be provided by querying the external redemption contract, and fix the function to call the internal `_availableLiquidity()` function as intended:

```diff
function availableLiquidity() external view returns (uint256) {
-    return IERC20(externalCollateralRedemption.asset()).balanceOf(collateralProvider);
+    return _availableLiquidity();
}

function _availableLiquidity() private view returns (uint256) {
-    return IERC20(externalCollateralRedemption.asset()).balanceOf(collateralProvider);
+    uint256 collateralBalance = IERC20(externalCollateralRedemption.asset()).balanceOf(collateralProvider);
+    return externalCollateralRedemption.calculateLiquidityTokenAmount(collateralBalance);
}
```

**Securitize:** Fixed in commit [1da35c](https://github.com/securitize-io/bc-on-off-ramp-sc/commit/bf970d6cc4152c1b22e386b6acc6095aece8f12a) and [4a426e](https://github.com/securitize-io/bc-on-off-ramp-sc/commit/4a426e689586a37cdcb463dba2f670fd58190ef9).

**Cyfrin:** Verified.

\clearpage
