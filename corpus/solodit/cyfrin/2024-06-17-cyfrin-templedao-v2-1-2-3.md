---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-2-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-06-17T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md
tags:
- firm:cyfrin
- report:2024-06-17-cyfrin-templedao-v2-1
title: Current design of TempleGold prevents distribution of tokens
vuln_class: []
---

# Current design of TempleGold prevents distribution of tokens

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-06-17-cyfrin-templedao-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md)_

---

**Description:** With current TempleGold token design, tokens only can be transferred to/from whitelisted addresses. This prevents further distribution of TempleGold tokens where they could be listed on DEXes, put on lending protocols as collateral and so on, which would be impossible because the protocol can not whitelist all the addresses based on user demands.

**Recommended Mitigation:** There should be a whitelist flag, when it is set to true, only whitelisted from/to addresses are accepted and when it is set to false, it should be open.

**Temple DAO:**
Acknowledged, but TempleGold is not traded or used on lending platforms

**Cyfrin:** Acknowledged

\clearpage
