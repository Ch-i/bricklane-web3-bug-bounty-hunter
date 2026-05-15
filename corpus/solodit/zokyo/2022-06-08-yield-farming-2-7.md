---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-06-08-yield-farming-2-7
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2022-06-08T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-06-08-Yield%20Farming.md
tags:
- firm:zokyo
- report:2022-06-08-yield-farming
title: Contract UnifarmCohort, variable factory is assigned only in the constructor
  and then the value is used all over the contract, from this behavior we understand
  that the scope of the factory variable is that it should be assigned only in con
vuln_class: []
---

# Contract UnifarmCohort, variable factory is assigned only in the constructor and then the value is used all over the contract, from this behavior we understand that the scope of the factory variable is that it should be assigned only in contract constructor, for that we would recommend making the variable as ‘immutable’, (immutable variables can only be assigned inside the constructor and only there), for extra security and to be in accordance with best practices.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-06-08-Yield Farming.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-06-08-Yield%20Farming.md)_

---

**Recommendation**:
Make variable factory from line 47 as immutable. (Done)
