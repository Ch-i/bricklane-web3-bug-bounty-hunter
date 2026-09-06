---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-3-10
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Empty body if branching
vuln_class: []
---

# Empty body if branching

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

In LimitOrdersStorage.sol - Method setOpenLimitOrderType() the if-statement in this method is having no purpose as it only executes console.log code which is not meant for deployment.

**Recommendation** 

Remove the console.log lines and the if-statement if they are not meant to be used.

**Fixed**: Issue fixed in commit a72e06b
