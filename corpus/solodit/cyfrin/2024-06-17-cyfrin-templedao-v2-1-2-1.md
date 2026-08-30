---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-2-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-06-17T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md
tags:
- firm:cyfrin
- report:2024-06-17-cyfrin-templedao-v2-1
title: DAI-GOLD auction might not get started for last mint of gold tokens
vuln_class: []
---

# DAI-GOLD auction might not get started for last mint of gold tokens

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-06-17-cyfrin-templedao-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md)_

---

**Description:** Usually minting gold happens when the available amount is bigger than 1e4, which will configure the minimum distribution amount of DaiGoldAuction. However when it reaches the max supply, the minting amount can be smaller than minimum amount, thus DaiGoldAuction might not get started because the amount will be smaller than the minimum distribution amount.

**Recommended Mitigation:** When it reached max supply, it allows to start auction with remaining amount.

**Temple DAO:**
`config.auctionMinimumDistributedGold` is not necessarily equal to the minimum gold mint amount. Also, for the last mint (max supply), `config.auctionMinimumDistributedGold` will be updated.

**Cyfrin:** Acknowledged
