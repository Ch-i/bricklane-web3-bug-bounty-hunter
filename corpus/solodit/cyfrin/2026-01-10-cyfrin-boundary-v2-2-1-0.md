---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-10-cyfrin-boundary-v2-2-1-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-01-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-10-cyfrin-boundary-v2.2.md
tags:
- firm:cyfrin
- report:2026-01-10-cyfrin-boundary-v2-2
title: Add minimum deposit to mitigate vault manipulation edge cases
vuln_class: []
---

# Add minimum deposit to mitigate vault manipulation edge cases

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-10-cyfrin-boundary-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-10-cyfrin-boundary-v2.2.md)_

---

**Description:** Consider adding basic input/rounding validations to reduce exposure to common ERC4626 vault-manipulation edge cases. In particular: enforce a small minimum deposit (e.g., `>= 1e18` USBD). This check help prevent dust/rounding-based griefing  outcomes that can be leveraged in manipulation attempts or to create confusing user-facing behavior.


**Boundary:**
Acknowledged. The vault already burns `1e12` shares to itself at deployment, which permanently protects against inflation/donation attacks and ensures dust deposits cannot round to zero shares. Combined with existing `ZeroAssets` and `ZeroShares` checks in `_deposit` and `_withdraw`, minimum deposit enforcement is redundant.
