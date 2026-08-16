---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-3-9
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
title: Require statements lacking error messages
vuln_class: []
---

# Require statements lacking error messages

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

In TradingStorage.sol - require statements in this contract are missing the inclusion of error messages. It is advised to provide a string containing a description about the error to be passed back to the caller.

**Recommendation** 

Include concise and short error messages.

**Fixed**: Issue fixed in commit a72e06b
