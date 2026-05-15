---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-23-mozaic-archimedes-3-8
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-05-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md
tags:
- firm:trust-security
- report:2023-05-23-mozaic-archimedes
title: Use of "0x" for address strings
vuln_class: []
---

# Use of "0x" for address strings

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-05-23-Mozaic Archimedes.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md)_

---

In several instances in StargatePlugin and MozBridge, "0x" is used for an empty address. It is 
recommended to use address(0) instead, to save gas costs and reduce confusion. In some 
cases, "0x" could be interpreted as a valid address.
