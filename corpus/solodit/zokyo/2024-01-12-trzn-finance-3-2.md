---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-12-trzn-finance-3-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md
tags:
- firm:zokyo
- report:2024-01-12-trzn-finance
title: Missing check for array length greater than 0 `getERC20Price_High` and `getERC20Price_Low`
  Functions
vuln_class: []
---

# Missing check for array length greater than 0 `getERC20Price_High` and `getERC20Price_Low` Functions

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-01-12-TRZN Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

In both functions, there is a loop over the AMMInfos array to calculate the average price. 

**Recommendations**: 

Consider adding a check to ensure that the AMMInfos array is not empty before entering the loop to prevent division by zero.
