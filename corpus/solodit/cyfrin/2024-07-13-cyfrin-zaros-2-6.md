---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-2-6
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: Protocol team can preferentially refuse to liquidate traders via centralized
  liquidators
vuln_class: []
---

# Protocol team can preferentially refuse to liquidate traders via centralized liquidators

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** The protocol team can preferentially refuse to liquidate traders since:
* only liquidators can liquidate traders subject to liquidation
* the protocol team control which addresses can be liquidators

**Impact:** The protocol team can refuse to liquidate some traders (for example if some trading accounts are operated by the protocol and/or team members) allowing them to attempt to ride out unfavorable market movements without liquidation, giving them an advantage over other traders.

**Recommended Mitigation:** In terms of getting version 1 of the protocol to mainnet, it is easier and simpler to go with centralized liquidators and gives the protocol team more control over the protocol. There is also likely little risk of the protocol team abusing this mechanic because it would destroy trust in the protocol. However long-term it would be ideal to move to decentralized liquidators.

**Zaros:** Acknowledged.
