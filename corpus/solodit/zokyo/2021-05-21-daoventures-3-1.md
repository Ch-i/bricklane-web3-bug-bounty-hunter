---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-05-21-daoventures-3-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2021-05-21T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-05-21-DAOventures.md
tags:
- firm:zokyo
- report:2021-05-21-daoventures
title: Same code doubled twice DAOstake.sol
vuln_class: []
---

# Same code doubled twice DAOstake.sol

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2021-05-21-DAOventures.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-05-21-DAOventures.md)_

---

**Description**

![image](https://github.com/user-attachments/assets/1ce0954b-15ec-468f-8115-ca365d655850)

At function updatePool(uint256 _pid), lines 265 and 271 contains the same code:

**Recommendation**:

Move this code before or below if condition.
