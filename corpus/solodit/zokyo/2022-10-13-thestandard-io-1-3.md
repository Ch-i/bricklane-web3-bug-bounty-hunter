---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-10-13-thestandard-io-1-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2022-10-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-10-13-TheStandard.io.md
tags:
- firm:zokyo
- report:2022-10-13-thestandard-io
title: Missing non-zero amount check for swap functions in SEuroOffering.
vuln_class: []
---

# Missing non-zero amount check for swap functions in SEuroOffering.

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2022-10-13-TheStandard.io.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-10-13-TheStandard.io.md)_

---

**Description**

SEuroOffering.sol body of swap(...) & swapETH(): input amount and msg.value are not required here to be non-zero leading to unnecessary computation.

**Recommendation**

Add checks to ensure input amount and msg.value are non-zero in `swap()` and `swapETH()` functions to prevent unnecessary computation.

**Re-audit comment**

Resolved
