---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-28-orbital-finance-3-3
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
title: Mark variables as immutable
vuln_class: []
---

# Mark variables as immutable

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-05-28-Orbital Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-28-Orbital%20Finance.md)_

---

Some variables, like **vaultInfoAddress** and **AI**, are fixed at deployment-time. It would be best 
to mark them as immutable, for code clarity as well as gas savings.

**Team response**
"Changed several variables to constant or immutable."

**Mitigation review:**
Change applied correctly.
