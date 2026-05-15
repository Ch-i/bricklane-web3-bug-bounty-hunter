---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-06-08-yield-farming-2-6
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
title: In library ConvertHexToString, function toString, for a better gas optimization,
  you can save the value of data.length in memory and iterate over the variable that
  is safe in memory, it will be cheaper to read from memory every time then to
vuln_class: []
---

# In library ConvertHexToString, function toString, for a better gas optimization, you can save the value of data.length in memory and iterate over the variable that is safe in memory, it will be cheaper to read from memory every time then to read from storage.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-06-08-Yield Farming.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-06-08-Yield%20Farming.md)_

---

**Recommendation**:
Create a new variable that it will store the value of data.length and use it in the for loop.
(Done)
