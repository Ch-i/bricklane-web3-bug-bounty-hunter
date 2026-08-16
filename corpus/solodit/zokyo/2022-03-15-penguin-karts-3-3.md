---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-15-penguin-karts-3-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2022-03-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-15-Penguin%20Karts.md
tags:
- firm:zokyo
- report:2022-03-15-penguin-karts
title: No message in “require” statements.
vuln_class: []
---

# No message in “require” statements.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-03-15-Penguin Karts.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-15-Penguin%20Karts.md)_

---

**Description**

StakingB_1.sol Line 546
StakingB.sol Lines 80, 95, 97, 99, 102, 103, 115, 117
To hold the exception error messages must be added.

**Recommendation**:

Add an error message to each exception.
