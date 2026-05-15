---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-2-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-06-17T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md
tags:
- firm:cyfrin
- report:2024-06-17-cyfrin-templedao-v2-1
title: In rewards distribution, dust amount is left and stuck in the contract
vuln_class: []
---

# In rewards distribution, dust amount is left and stuck in the contract

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-06-17-cyfrin-templedao-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md)_

---

**Description:** When rewards distribution happens, it's distributed over 7 days(604800 seconds), the reward rate is calculated per second, thus every time, the remainder which is less than 604800 wei of tokens are left in the contract.

**Recommended Mitigation:** The left amount of rewards should be added to next round of distribution.

**Temple DAO:**
Fixed in [PR 1046](https://github.com/TempleDAO/temple/pull/1046)

**Cyfrin:** Verified
