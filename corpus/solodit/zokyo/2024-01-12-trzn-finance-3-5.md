---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-12-trzn-finance-3-5
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md
tags:
- firm:zokyo
- report:2024-01-12-trzn-finance
title: Unused params
vuln_class: []
---

# Unused params

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-01-12-TRZN Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

In Contract VaultETH_V2, the method mintableAmount() comments mention that it returns the mintable amount based on user and epoch value.
Although it doesn’t use `address user` anywhere in calculating the same. 

**Recommendation**: 

Either update the comment or the method as it suits the protocol.
