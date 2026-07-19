---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-23-mozaic-archimedes-3-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-05-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md
tags:
- firm:trust-security
- report:2023-05-23-mozaic-archimedes
title: Define immutables
vuln_class: []
---

# Define immutables

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-05-23-Mozaic Archimedes.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md)_

---

State variables that should never change during the lifetime of a contract should be defined 
as immutable. For example, the Vault's **chainId** is fixed. The use of immutables both improve 
readability and save loads from storage.
