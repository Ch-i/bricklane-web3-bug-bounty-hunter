---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-08-ninja-yield-farming-v3-3-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-01-08T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-08-Ninja%20Yield%20Farming%20v3.md
tags:
- firm:trust-security
- report:2023-01-08-ninja-yield-farming-v3
title: Make greater use of immutable variables
vuln_class: []
---

# Make greater use of immutable variables

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-01-08-Ninja Yield Farming v3.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-08-Ninja%20Yield%20Farming%20v3.md)_

---

Immutable variables are guaranteed to be read only during a contract's lifetime. In V3 vault, 
several variables are not immutable but should never change: **profitToken**, 
**constructionTime**, **underlying**. 

**Team response**
Accepted & done.
