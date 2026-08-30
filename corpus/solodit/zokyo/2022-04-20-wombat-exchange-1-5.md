---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-04-20-wombat-exchange-1-5
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2022-04-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-04-20-Wombat%20Exchange.md
tags:
- firm:zokyo
- report:2022-04-20-wombat-exchange
title: In contract Pool.sol at lines 197-200 there’s no event emitted after changing
  the dev address, similar to the Ownable approach which emits a OwnershipTransferred
  event.
vuln_class: []
---

# In contract Pool.sol at lines 197-200 there’s no event emitted after changing the dev address, similar to the Ownable approach which emits a OwnershipTransferred event.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-04-20-Wombat Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-04-20-Wombat%20Exchange.md)_

---

**Recommendation**: Add an event for the setDev function.
