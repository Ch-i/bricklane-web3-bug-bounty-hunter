---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-2-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: Wrong hunter address is used.
vuln_class: []
---

# Wrong hunter address is used.

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

Disqualifier.sol: processUserWithBounty(). 
Parameter_hunter' is never used. Based on the logic of the function and a similar function processUsersWithBounty(), where parameter '_hunter' is passed to the internal function, the same should happen in process UserWithBounty(). 

**Recommendation**: 

Pass parameter _hunter to the internal function instead of msg.sender OR remove 
parameter_hunter'. 

**Post-audit**: 

Contract was removed.
