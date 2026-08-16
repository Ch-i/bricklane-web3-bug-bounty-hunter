---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-06-14-paid-ignition-2-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2021-06-14T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-14-Paid%20Ignition.md
tags:
- firm:zokyo
- report:2021-06-14-paid-ignition
title: Library is not used in the project
vuln_class: []
---

# Library is not used in the project

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2021-06-14-Paid Ignition.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-14-Paid%20Ignition.md)_

---

**Description**

Library DateTimePool.sol is not used in the project. Review the logic or remove the library.

**Recommendation**:

Remove unused library.
