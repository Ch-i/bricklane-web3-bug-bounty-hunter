---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-28-orbital-finance-3-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-05-28T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-28-Orbital%20Finance.md
tags:
- firm:trust-security
- report:2023-05-28-orbital-finance
title: Redundant reentrancy protection
vuln_class: []
---

# Redundant reentrancy protection

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-05-28-Orbital Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-28-Orbital%20Finance.md)_

---

Several functions in the vault factory contract are protected with a reentrancy guard. It is not 
clear why this guard is required, so it would be best to re-consider uses of the reentrancy 
guard in several of the contracts. Specifically, consider when an attacker could gain code 
execution and what is the current state that could be abused.

**Team response:**
"Removed several reentrancy protections, including all from the VaultV2 contract (anything 
that might be a problem is called only by the VaultManager, which has the protection in 
place)."

**Mitigation review:**
Fix is sound
