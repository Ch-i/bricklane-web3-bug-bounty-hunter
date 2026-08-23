---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-19-cedro-finance-0-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-03-19T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md
tags:
- firm:zokyo
- report:2024-03-19-cedro-finance
title: Liquidation bonus is 0% when `currentLTV > 1e18`
vuln_class: []
---

# Liquidation bonus is 0% when `currentLTV > 1e18`

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2024-03-19-Cedro Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md)_

---

**Severity**: High

**Status**: Acknowledged

**Description**

In Contract LiquidationManager.sol, the method `liquidate(..)` has the following check:
```solidity
       uint256 discount; 
       uint256 liqPercent = 1e18;
       if (currentLTV < 1e18) {
           discount = 1e36 / currentLTV - 999000000000000000;
           console.log("discount", discount);
           if (discount > config.liqMaxDiscount) {
               discount = config.liqMaxDiscount;
           }
…}}
```
Here discount is 0 if `currentLTV` is more than 1e18. This means there is no liquidation bonus for liquidators and will lead to a pile of bad debts as there is no incentive for users to liquidate.

**Recommendation**: 

Update the liquidation logic to assign a discount amount for liquidation to provide the incentive for the same.

**Client commented**: 

We have implemented the liquidation logic in a way to mitigate the toxic liquidation spiral. So for that reason the liquidation bonus is 0% when currentLTV>1e18. Please refer to https://arxiv.org/pdf/2212.07306.pdf
