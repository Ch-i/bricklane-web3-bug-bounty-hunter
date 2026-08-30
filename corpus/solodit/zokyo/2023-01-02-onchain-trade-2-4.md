---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-01-02-onchain-trade-2-4
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-01-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-01-02-Onchain%20Trade.md
tags:
- firm:zokyo
- report:2023-01-02-onchain-trade
title: Use of reason strings instead of custom errors
vuln_class: []
---

# Use of reason strings instead of custom errors

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-01-02-Onchain Trade.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-01-02-Onchain%20Trade.md)_

---

**Severity**: Informational

**Status**: Unresolved

**Description**

Inside the contracts the reason strings are used inside require statements as revert messages. An alternative would be to use custom errors. This contributes to reducing contract size and reducing overall gas cost.

**Recommendation**: 

Change reason strings to custom errors.
