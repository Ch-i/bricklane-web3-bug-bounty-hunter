---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-3-11
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: Functions have the same implementation.
vuln_class: []
---

# Functions have the same implementation.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

Disqualifier.sol: getBaseBounty() and getCompound Bounty(). 
Implementation of functions getBaseBounty and getCompoundBounty is absolutely identical. Thus only one function can be left. 

**Recommendation**: 

Consider removing or modifying one of the functions. 

**Post-audit**: 
Contract was removed.
