---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-3-14
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Missing pure in function definition
vuln_class: []
---

# Missing pure in function definition

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

In NarwhalPriceAggregator - tenPow() is recommended to be defined as a pure function.

**Recommendation** 

Add pure to function definition.

Fixed: Issue fixed in commit a72e06b
