---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-06-14-paid-ignition-2-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2021-06-14T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-14-Paid%20Ignition.md
tags:
- firm:zokyo
- report:2021-06-14-paid-ignition
title: Unused functions in the library
vuln_class: []
---

# Unused functions in the library

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2021-06-14-Paid Ignition.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-14-Paid%20Ignition.md)_

---

**Description**

Library BitOpMapPool.sol contains functions setPkgDtTknPool() and setPkgDtWhiteList() which
are not used within the project. In case if it is native and not external library, consider
removing the unused functions.

**Recommendation**:

Remove unused functions.
