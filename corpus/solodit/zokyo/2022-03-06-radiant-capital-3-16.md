---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-3-16
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: Unnecessary variable.
vuln_class: []
---

# Unnecessary variable.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

RadiantOFT:_mint() 
Since contract can use_mint once per lifespan maxMintAmount is replacing maxSupply. 

**Recommendation**: 

maxMintAmount should be removed and replaced with maxSupply instead, also requires in this function cannot be reverted in the current contract version.
