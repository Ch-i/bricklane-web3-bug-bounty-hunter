---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-24-narwhal-finance-3-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-01-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-24-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2024-01-24-narwhal-finance
title: Method `setNativeForKeeper` sets `nativeForCallback` as well with no events
vuln_class: []
---

# Method `setNativeForKeeper` sets `nativeForCallback` as well with no events

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-01-24-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-24-Narwhal%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**


In Contract Trading.sol, the method setNativeForKeeper also sets nativeForCallback with emitting any event even though there is a method to set nativeForCallback. 

**Recommendation**: 

Remove the setting of `nativeForCallback` from the method `setNativeForKeeper`.
