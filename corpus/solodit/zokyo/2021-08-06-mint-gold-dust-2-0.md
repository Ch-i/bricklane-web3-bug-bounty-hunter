---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-08-06-mint-gold-dust-2-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2021-08-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-08-06-Mint%20Gold%20Dust.md
tags:
- firm:zokyo
- report:2021-08-06-mint-gold-dust
title: Event invocations have to be prefixed by emit
vuln_class: []
---

# Event invocations have to be prefixed by emit

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2021-08-06-Mint Gold Dust.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-08-06-Mint%20Gold%20Dust.md)_

---

**Description**

contracts/OrderBook.sol#257
It is recommended to explicitly use emit keyword for the event to distinguish the functions
calls and events emitting per recommendation from the Solidity checklist.

**Recommendation**:

Event invocations have to be prefixed by emit . Add prefixed by emit .
