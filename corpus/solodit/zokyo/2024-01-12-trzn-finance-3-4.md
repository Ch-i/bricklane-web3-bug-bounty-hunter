---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-12-trzn-finance-3-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md
tags:
- firm:zokyo
- report:2024-01-12-trzn-finance
title: Missing checks in `CheckRiskManagerStatus` function
vuln_class: []
---

# Missing checks in `CheckRiskManagerStatus` function

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-01-12-TRZN Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md)_

---

**Severity**: Informational

**Status**: Acknowledged

**Description**

 This assumes that the inputs (escrow, riskManager, inputAmt, tokenPrice, tokenPriceDecimal) are valid and within reasonable ranges. 

**Recommendations**: 

Consider including input validation checks to ensure that these values are as expected.
