---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-2-4
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: Single step redemption and two step redemption not equivalent logic
vuln_class: []
---

# Single step redemption and two step redemption not equivalent logic

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** The `RedemptionManager::executeSingleStepRedemption` has multiple issues when used with `CollateralLiquidityProvider`

1. Fee calculated on requested amount, not actual amount:

```solidity
        // Apply fee if it exists, transfer it to the fee collector
        fee = TokenCalculator.calculateFee(_params.feeManager, _params.liquidityTokenAmount);
```
The fee is calculated based on `_params.liquidityTokenAmount ` (the requested amount), but `CollateralLiquidityProvider::supplyTo` returns a different (smaller) amount due to external redemption fees:

```solidity
function supplyTo(
        address _redeemer,
        uint256 _liquidityAmount
    ) public whenNotPaused onlySecuritizeRedemption returns (uint256 amountToSupply) {
        ...
        // Discount the fee charged by the external collateral redemption
        amountToSupply = externalCollateralRedemption.calculateLiquidityTokenAmount(collateralAmount);

        // Supply redeemer
        liquidityToken.transfer(_redeemer, amountToSupply);
    }
```

2. The return value of fee `supplyTo` is ignored:

```solidity
 if (fee > 0) {
            _params.liquidityProvider.supplyTo(IFeeManager(_params.feeManager).feeCollector(), fee);
        }//@audit why not supplied here?
```
The return value is not captured. The fee collector receives less than fee due to external redemption fees, but the function returns the original calculated fee, causing incorrect accounting.

3. Double external redemption fees:

```solidity
 // Supply liquidity tokens to the fee collector
        if (fee > 0) {
            _params.liquidityProvider.supplyTo(IFeeManager(_params.feeManager).feeCollector(), fee);
        }//@audit why not supplied here?

        // Supply liquidity tokens to the redeemer
        userSuppliedAmount = _params.liquidityProvider.supplyTo(_params.redeemer, _params.liquidityTokenAmount - fee);
```
Each `CollateralLiquidityProvider ::supplyTo` call triggers a full external redemption flow compare to `executeTwoStepRedemption` which correctly uses a single `supplyTo` call and calculates fees on the actual supplied amount


**Recommended Mitigation:** Consider make single step redemption and two step redemption equivalent.

**Securitize:** Acknowledged.
