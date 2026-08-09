---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-06-12-itrust-finance-3-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2021-06-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-12-iTrust%20Finance.md
tags:
- firm:zokyo
- report:2021-06-12-itrust-finance
title: Use standard ReentrancyGuard
vuln_class: []
---

# Use standard ReentrancyGuard

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2021-06-12-iTrust Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-12-iTrust%20Finance.md)_

---

**Description**

Throughout the project the variable _Locked together with _nonReentrant() function are used
for the reentrancy prevention, though, for the safety of further development it is
recommended to use standard ReentrancyGuard with modifier. It will increase the overall
code quality.

**Recommendation**:

Use standard ReentrancyGuard.
