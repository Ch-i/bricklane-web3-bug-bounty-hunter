---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-3-18
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: PausableInterface variables never used
vuln_class: []
---

# PausableInterface variables never used

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

In TradingStorage contract, `trading` and `callbacks` variables uses PausableInterface but never uses the only method defined in it, i.e. isPaused().

**Recommendation**: 

Remove the unused variables or Update the interface.

**Fixed**: Issue fixed in commit a72e06b
