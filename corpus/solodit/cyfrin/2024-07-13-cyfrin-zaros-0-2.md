---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-0-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: '`TradingAccount::withdrawMarginUsd` transfers an incorrectly larger amount
  of margin collateral for tokens with less than 18 decimals'
vuln_class: []
---

# `TradingAccount::withdrawMarginUsd` transfers an incorrectly larger amount of margin collateral for tokens with less than 18 decimals

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** The `UD60x18` values are [scaled up to 18 decimal places](https://github.com/zaros-labs/zaros-core-audit/blob/de09d030c780942b70f1bebcb2d245214144acd2/src/perpetuals/leaves/MarginCollateralConfiguration.sol#L46-L50) for collateral tokens with less than 18 decimals places. But when `TradingAccount::withdrawMarginUsd` transfers tokens to the recipient it doesn't scale the transferred amount back down to the collateral token's native decimal value:

```solidity
function withdrawMarginUsd(
    Data storage self,
    address collateralType,
    UD60x18 marginCollateralPriceUsdX18,
    UD60x18 amountUsdX18,
    address recipient
)
    internal
    returns (UD60x18 withdrawnMarginUsdX18, bool isMissingMargin)
{
    UD60x18 marginCollateralBalanceX18 = getMarginCollateralBalance(self, collateralType);
    UD60x18 requiredMarginInCollateralX18 = amountUsdX18.div(marginCollateralPriceUsdX18);
    if (marginCollateralBalanceX18.gte(requiredMarginInCollateralX18)) {
        withdraw(self, collateralType, requiredMarginInCollateralX18);

        withdrawnMarginUsdX18 = withdrawnMarginUsdX18.add(amountUsdX18);

        // @audit wrong amount for collateral tokens with less than 18 decimals
        // needs to be scaled down to collateral token's native precision
        IERC20(collateralType).safeTransfer(recipient, requiredMarginInCollateralX18.intoUint256());

        isMissingMargin = false;
        return (withdrawnMarginUsdX18, isMissingMargin);
    } else {
        UD60x18 marginToWithdrawUsdX18 = marginCollateralPriceUsdX18.mul(marginCollateralBalanceX18);
        withdraw(self, collateralType, marginCollateralBalanceX18);
        withdrawnMarginUsdX18 = withdrawnMarginUsdX18.add(marginToWithdrawUsdX18);

        // @audit wrong amount for collateral tokens with less than 18 decimals
        // needs to be scaled down to collateral token's native precision
        IERC20(collateralType).safeTransfer(recipient, marginCollateralBalanceX18.intoUint256());

        isMissingMargin = true;
        return (withdrawnMarginUsdX18, isMissingMargin);
    }
}
```

Here is a possible scenario.
- A user deposits 10K USDC(has 6 decimals) to his trading account. Then his margin collateral balance will be `10000 * 10^(18 - 6) = 10^16`.
- During a liquidation/settlement, `withdrawMarginUsd` is called with `requiredMarginInCollateralX18 = 1e4` which means `10^-8 USDC`.
- But due to the incorrect decimal conversion logic, the function transfers the whole collateral(10K USDC) but still has `10^16 - 10^4` collateral balance.

**Impact:** Margin collateral balances become corrupt allowing users to withdraw more collateral than they should leading to loss of funds for other users since they won't be able to withdraw.

**Recommended Mitigation:** `withdrawMarginUsd` should scale the amount down to the collateral token's native precision before calling `safeTransfer`.

**Zaros:** Fixed in commit [1ac2acc](https://github.com/zaros-labs/zaros-core/commit/1ac2acc179830c08069b3e5856b9439867a06d50#diff-f09472a5f9e6d5545d840c0760cb5606febbfe8a60fa8b7fc6e7cda8735ce357R378-R396).

**Cyfrin:** Verified.
