---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-06-08-yield-farming-2-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2022-06-08T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-06-08-Yield%20Farming.md
tags:
- firm:zokyo
- report:2022-06-08-yield-farming
title: In contract UnifarmCohort, functions setPortionAmount and disableBooster does
  not contains sanity checks, even if they are only settable by the owner they still
  need to contains sanity checks to be in standard with best practices.
vuln_class: []
---

# In contract UnifarmCohort, functions setPortionAmount and disableBooster does not contains sanity checks, even if they are only settable by the owner they still need to contains sanity checks to be in standard with best practices.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-06-08-Yield Farming.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-06-08-Yield%20Farming.md)_

---

**Recommendation**:
Add sanity checks to the setPortionAmount and disableBooster functions. (this was
informational so skipping it)
