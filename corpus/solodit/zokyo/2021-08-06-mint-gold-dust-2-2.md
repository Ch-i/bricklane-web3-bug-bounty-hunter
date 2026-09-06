---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-08-06-mint-gold-dust-2-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2021-08-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-08-06-Mint%20Gold%20Dust.md
tags:
- firm:zokyo
- report:2021-08-06-mint-gold-dust
title: Use an interface instead of an abstract contract
vuln_class: []
---

# Use an interface instead of an abstract contract

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2021-08-06-Mint Gold Dust.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-08-06-Mint%20Gold%20Dust.md)_

---

**Description**

For now MGDcontract.sol has no functional value as an abstract contract. Consider usage of
the interface. Such a move will save gas and decrease the contract size.

**Recommendation**:

Use an interface instead of an abstract contract.
