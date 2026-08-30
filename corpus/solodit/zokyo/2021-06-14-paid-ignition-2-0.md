---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-06-14-paid-ignition-2-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2021-06-14T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-14-Paid%20Ignition.md
tags:
- firm:zokyo
- report:2021-06-14-paid-ignition
title: Optimization in calculation
vuln_class: []
---

# Optimization in calculation

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2021-06-14-Paid Ignition.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-14-Paid%20Ignition.md)_

---

**Description**

IgnitionIDO.sol, line 53
poolTokens[_poolAddr][_pool].tokenTotalAmount is set to the result of subtraction, though,
due to the logic of previous calculations, it can be set directly to
poolTokens[_poolAddr][_pool].soldAmount.
IgnitionIDO.sol, line 238. poolTokens[_poolAddr][_pool].tokenTotalAmount can be set to
soldAmount instead of re-calculation

**Recommendation**:

Optimize the calculation.
