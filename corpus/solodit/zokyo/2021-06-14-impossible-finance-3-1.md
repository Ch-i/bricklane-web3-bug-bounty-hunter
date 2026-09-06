---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-06-14-impossible-finance-3-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2021-06-14T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-14-Impossible%20Finance.md
tags:
- firm:zokyo
- report:2021-06-14-impossible-finance
title: Set the commission percentage to a variable
vuln_class: []
---

# Set the commission percentage to a variable

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2021-06-14-Impossible Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-14-Impossible%20Finance.md)_

---

**Description**

StableXPair.sol line 252, 253.
In order to increase the readability of the code and further development security it is
recommended to move the commision value (201) to the public variable or public constant.

**Recommendation**:

Move the value into a constant.
