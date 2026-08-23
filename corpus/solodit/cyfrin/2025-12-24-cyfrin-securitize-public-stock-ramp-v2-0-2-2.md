---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-2-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: Missing `liquidityToken` validation in `CollateralLiquidityProvider::initialize`
vuln_class: []
---

# Missing `liquidityToken` validation in `CollateralLiquidityProvider::initialize`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** The `CollateralLiquidityProvider::setExternalCollateralRedemption` function includes a validation check to ensure the liquidity token of the new external collateral redemption contract matches the existing `liquidityToken`:

```solidity
function setExternalCollateralRedemption(address _externalCollateralRedemption) external onlyRole(DEFAULT_ADMIN_ROLE) {
        if (_externalCollateralRedemption == address(0)) {
            revert NonZeroAddressError();
        }

        if (
            address(
                ILiquidityProvider(address(ISecuritizeOffRamp(_externalCollateralRedemption).liquidityProvider()))
                    .liquidityToken()
            ) != address(liquidityToken)//@audit-ok (low) why this i not checked in intializatuion
        ) {
            revert LiquidityTokenMismatch();
        }
        address oldExternalCollateral = address(externalCollateralRedemption);
        externalCollateralRedemption = ISecuritizeOffRamp(_externalCollateralRedemption);
        emit ExternalCollateralRedemptionUpdated(oldExternalCollateral, address(externalCollateralRedemption));
    }
```

However, `CollateralLiquidityProvider::initialize` sets the same `externalCollateralRedemption` without performing this validation:

```solidity
function initialize(
    address _liquidityToken,
    address _recipient,
    address _securitizeOffRamp,
    address _externalCollateralRedemption,
    address _collateralProvider
) public onlyProxy initializer {
    // ... zero address checks only ...

    liquidityToken = IERC20Metadata(_liquidityToken);
    externalCollateralRedemption = ISecuritizeOffRamp(_externalCollateralRedemption);
    ...
    //@audit missing validation that _externalCollateralRedemption's liquidity token matches _liquidityToken
}
```

**Impact:** During contract deployment, an admin could mistakenly initialize the contract with an `_externalCollateralRedemption` that uses a different liquidity token than the configured `_liquidityToken`.

**Recommended Mitigation:** Add the liquidity token validation to the  `CollateralLiquidityProvider::initialize`.

**Securitize:** Fixed in commit [d8fd4fb](https://github.com/securitize-io/bc-on-off-ramp-sc/commit/d8fd4fb9c38ed4d006df7ace366d30de239d6d4a).

**Cyfrin:** Verified.
