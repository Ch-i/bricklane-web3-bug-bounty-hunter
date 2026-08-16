---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-05-21-daoventures-1-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2021-05-21T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-05-21-DAOventures.md
tags:
- firm:zokyo
- report:2021-05-21-daoventures
title: Potential gas overflow due to unlimited array length
vuln_class: []
---

# Potential gas overflow due to unlimited array length

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2021-05-21-DAOventures.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-05-21-DAOventures.md)_

---

**Description**

In function massUpdatePools() there is a loop that depends on pool.length. In the case
significant amount of pools, this function potentially could not be completed due to gas limits.

**Recommendation**:

Add a comment that confirms that no significant pool amount expected. Otherwise, add offset
and limit parameters, to update pools portionally.
