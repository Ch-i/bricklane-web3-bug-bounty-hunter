---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-2-5
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
title: Protocol team can censor traders via centralized keepers
vuln_class: []
---

# Protocol team can censor traders via centralized keepers

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** The protocol team can censor traders since:
* only keepers can fulfill trader market orders
* the protocol team control which addresses can be keepers

**Impact:** The protocol team can censor traders by never filling their orders; eg they could prevent a trader from closing their opened leveraged position which severely disadvantages that trader because they remain subject to liquidation if the market moves against their position.

The protocol team could also favor some traders over others by choosing a specific order to fill pending trades which benefit some traders over others.

**Recommended Mitigation:** In terms of getting version 1 of the protocol to mainnet, it is easier and simpler to go with centralized keepers and gives the protocol team more control over the protocol. There is also likely little risk of the protocol team abusing this mechanic because it would destroy trust in the protocol. However long-term it would be ideal to move to decentralized keepers.

**Zaros:** Acknowledged.
