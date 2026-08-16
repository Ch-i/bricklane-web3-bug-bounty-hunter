---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-10-13-thestandard-io-2-5
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2022-10-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-10-13-TheStandard.io.md
tags:
- firm:zokyo
- report:2022-10-13-thestandard-io
title: Direct contract referencing instead of interfaces in SEuroCalculator.
vuln_class: []
---

# Direct contract referencing instead of interfaces in SEuroCalculator.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-10-13-TheStandard.io.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-10-13-TheStandard.io.md)_

---

**Description**

SEuroCalculator.
SEuroCalculator.sol - Reference of BondingCurve, TokenManager
Generally referencing the contracts as is rather than implementing interfaces.

**Recommendation**

Use interfaces for interacting with external contracts (BondingCurve, TokenManager) instead of direct contract referencing for better upgradability and modularity.

**Re-audit comment**

Unresolved
