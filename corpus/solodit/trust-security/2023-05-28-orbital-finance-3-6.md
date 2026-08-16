---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-28-orbital-finance-3-6
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
title: Validation checks
vuln_class: []
---

# Validation checks

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-05-28-Orbital Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-28-Orbital%20Finance.md)_

---

There is no check that all tokens in a newly created vault are unique. This could cause a wide 
variety of problems.

**Team response:**
"Added unique token validation to the VaultV2 constructor"

**Mitigation review:**
The new check is sound.
