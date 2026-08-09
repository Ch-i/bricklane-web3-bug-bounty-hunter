---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-07-21-itrustfinance-2-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2021-07-21T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-07-21-ITrustFinance.md
tags:
- firm:zokyo
- report:2021-07-21-itrustfinance
title: Usage of “magic” numbers
vuln_class: []
---

# Usage of “magic” numbers

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2021-07-21-ITrustFinance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-07-21-ITrustFinance.md)_

---

**Description**

buyCover(), line 205, line 237
Avoid usage of “magic” numbers for the accuracy of calculations. Consider usage of the
constant.

**Recommendation**:

Consider usage of the constant.
