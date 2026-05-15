---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-12-trzn-finance-3-1
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
title: Missing checks for parameters for setParams Function in `ERC20PriceOracle_V2`
vuln_class: []
---

# Missing checks for parameters for setParams Function in `ERC20PriceOracle_V2`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-01-12-TRZN Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

The setParams function allows the owner to set parameters, including unitRatio, gap, and precisionLimit. 

**Recommendations**: 

Ensure that these parameters are set within reasonable and safe ranges to avoid potential vulnerabilities.
