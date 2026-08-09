---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-3-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Function do not emit proper events
vuln_class: []
---

# Function do not emit proper events

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

The following state changing function do not emit proper event:
NarwhalPool.setRewardsDuration
NarwhalPool.notifyRewardAmount
VesterNLP.setGov
BaseToken.setGov
Vester.setGov
TradingVaultV2.setRewardToken
TradingVaultV2.setVester
XXX

**Recommendation**: 

Consider adding events to functions that change important state variables.
