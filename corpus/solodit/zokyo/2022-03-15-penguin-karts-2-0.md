---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-15-penguin-karts-2-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2022-03-15T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-15-Penguin%20Karts.md
tags:
- firm:zokyo
- report:2022-03-15-penguin-karts
title: Excess functionality.
vuln_class: []
---

# Excess functionality.

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2022-03-15-Penguin Karts.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-15-Penguin%20Karts.md)_

---

**Description**

StakingB_1.sol Line 632
Calling pool.token will cause the same result as the tokenAddress() function.

**Recommendation**:

Delete tokenAddress() function.
