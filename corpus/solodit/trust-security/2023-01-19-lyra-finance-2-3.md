---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-19-lyra-finance-2-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-01-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md
tags:
- firm:trust-security
- report:2023-01-19-lyra-finance
title: TRST-L-4 GMXAdapter minReturnPercent can be over 100%, requiring positive slippage
  for exchange to execute
vuln_class: []
---

# TRST-L-4 GMXAdapter minReturnPercent can be over 100%, requiring positive slippage for exchange to execute

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-01-19-Lyra Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md)_

---

**Description:**
In GMXAdapter `exchangeFromExactBase()`, minReturnPercent is used to set the minimum 
output tokens for the trade:
```solidity
    uint minOut = tokenInPrice.multiplyDecimal(marketPricingParams[_optionMarket].minReturnPercent)
      .multiplyDecimal(_amountBase)
       .divideDecimal(tokenOutPrice);
```
Since the rest of the calculation is done precisely the same as in positionRouter, except 
imposed fees, if minReturnPercent is above 100% transactions will never succeed. However, 
it’s allowed to be up to 120%. It appears the reason for that is to protect against any 
discrepancy that may occur in the future. It still does not seem to be correct to fix 
discrepancies with this parameter, as any change that causes the formula to not work needs 
to be examined closely rather than suppressed.

**Recommended mitigation:**
Allow **minReturnPercent** up to 100% (1e18).

**Team response:**
**minReturnPercent** has been removed and the functionality merged with the variable 
**staticSwapFeeEstimate**
