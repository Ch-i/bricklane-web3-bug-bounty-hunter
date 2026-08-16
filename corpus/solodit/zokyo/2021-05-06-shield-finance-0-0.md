---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-05-06-shield-finance-0-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2021-05-06T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-05-06-Shield%20Finance.md
tags:
- firm:zokyo
- report:2021-05-06-shield-finance
title: TODO in pre-production code
vuln_class: []
---

# TODO in pre-production code

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2021-05-06-Shield Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-05-06-Shield%20Finance.md)_

---

**Description**

Line 84
TODO statements in pre-production code for allocations calculations. This statement needs
clarification, especially from the point of view of the non-audited code potentially added.

**Recommendation**:

Clarify the statement and finish the logic.
