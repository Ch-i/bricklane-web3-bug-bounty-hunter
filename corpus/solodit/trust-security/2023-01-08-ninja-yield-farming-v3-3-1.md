---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-08-ninja-yield-farming-v3-3-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-01-08T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-08-Ninja%20Yield%20Farming%20v3.md
tags:
- firm:trust-security
- report:2023-01-08-ninja-yield-farming-v3
title: Emission of events during state changes
vuln_class: []
---

# Emission of events during state changes

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-01-08-Ninja Yield Farming v3.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-08-Ninja%20Yield%20Farming%20v3.md)_

---

To satisfy the objective of transparency, it is recommended to emit events when any change 
of importance takes place. In V3 Strategies, `updateSecurityFee()`, `updateTreasury()` and the 
important upgrade related functions `clearUpgradeCooldown()` and 
`initiateUpgradeCooldown()` do not emit events.

**Team response**
Accepted & done.
