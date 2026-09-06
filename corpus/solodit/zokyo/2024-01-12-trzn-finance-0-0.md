---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-12-trzn-finance-0-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md
tags:
- firm:zokyo
- report:2024-01-12-trzn-finance
title: Missing access control in burn
vuln_class: []
---

# Missing access control in burn

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2024-01-12-TRZN Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md)_

---

**Severity**: Critical

**Status**:  Resolved

**Description**

In the TokenStableV6 contract, there is a missing access control in `burn()`. This function can be used by an attacker to burn tokens from any address. 

**Recommendation**: 

It is advised to either allow only the msg.sender to burn his own tokens, or add an appropriate access control modifier for the same.
