---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-3-17
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
title: Unnecessary usage of variable
vuln_class: []
---

# Unnecessary usage of variable

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

VestingSchedule.sol - Variable bool started is unneeded since startTime (i.e. being set to block.timestamp) already serves the purpose to be a start flag since it is conveying the information that method start() has been invoked.

**Fixed**: Issue fixed in commit a72e06b
