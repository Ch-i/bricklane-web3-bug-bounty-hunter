---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-3-14
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: Event is never used.
vuln_class: []
---

# Event is never used.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

MiddleFee Distribution.sol: MintersUpdated() 
Mint method was removed from the contract but the corresponding event remains present. 

**Recommendation**:

Remove unused event. 

**Post-audit**: 
Radiant team has removed unused event.
