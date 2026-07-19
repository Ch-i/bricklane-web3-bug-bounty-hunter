---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-05-21-daoventures-1-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2021-05-21T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-05-21-DAOventures.md
tags:
- firm:zokyo
- report:2021-05-21-daoventures
title: Math could fail due to negative number in DVGToken.sol
vuln_class: []
---

# Math could fail due to negative number in DVGToken.sol

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2021-05-21-DAOventures.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-05-21-DAOventures.md)_

---

**Description**

At function _moveDelegates, line 220 srcRepOld can be 0 or less than amount:
![image](https://github.com/user-attachments/assets/31b3c020-78e3-4794-a2bb-2d7dcd1b2831)


While line 221 expects srcRepOld to be >= amount:
![image](https://github.com/user-attachments/assets/015f1caf-eb93-420e-bbcb-bd27d8cb2dd1)

**Recommendation**:
Depending on requirements, add ‘revert’ or ‘if’ to correctly handle possible negative value.
