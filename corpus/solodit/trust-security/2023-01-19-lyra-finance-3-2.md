---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-19-lyra-finance-3-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-01-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md
tags:
- firm:trust-security
- report:2023-01-19-lyra-finance
title: Misleading variable names
vuln_class: []
---

# Misleading variable names

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-01-19-Lyra Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md)_

---

There are some instances where possibly code has been duplicated without proper renaming. 
For example, in GMXAdapter, _getMaxPrice() is implemented as:
```solidity
    function _getMaxPrice(address asset) internal view returns (uint) {
        uint minPrice = vault.getMaxPrice(asset);
       return ConvertDecimals.normaliseTo18(minPrice, GMX_PRICE_PRECISION);
         }
```
Another example is the function`_getPendingIncreaseCollateralDelta()` which actually returns 
the **amountIn** variable.
Such patterns are prone to the introduction of bugs.
