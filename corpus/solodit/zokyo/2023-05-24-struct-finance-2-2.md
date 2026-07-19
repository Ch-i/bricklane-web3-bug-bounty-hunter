---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-05-24-struct-finance-2-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-05-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md
tags:
- firm:zokyo
- report:2023-05-24-struct-finance
title: Critical function rescueTokens it's not emmiting event
vuln_class: []
---

# Critical function rescueTokens it's not emmiting event

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-05-24-Struct Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md)_

---

**Severity** : Informational 

**Status**: Resolved

**Description**

Critical function rescueTokens it's not emmiting event
It is a good practice that onlyOwner functions always emit event
https://github.com/zokyo-sec/audit-struct-finance-1/blob/audit/zokyo-feb-2023/contracts/protocol/products/traderjoe/FEYTraderJoeProduct.sol#L506

**Recommandation**: 

Add an event to record that owner/governance is rescuing tokens.
