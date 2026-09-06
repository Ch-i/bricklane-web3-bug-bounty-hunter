---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-23-mozaic-archimedes-3-7
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-05-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md
tags:
- firm:trust-security
- report:2023-05-23-mozaic-archimedes
title: Better sanitization in _getPoolIndexInFarming() of StargatePlugin
vuln_class: []
---

# Better sanitization in _getPoolIndexInFarming() of StargatePlugin

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-05-23-Mozaic Archimedes.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md)_

---

If the call to _getPool() returns an address of zero, the plugin could confuse it as a valid found 
pool. It is best to revert in that scenario.
