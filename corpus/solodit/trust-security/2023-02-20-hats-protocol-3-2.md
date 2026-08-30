---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-20-hats-protocol-3-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-02-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md
tags:
- firm:trust-security
- report:2023-02-20-hats-protocol
title: Emit events without state change
vuln_class: []
---

# Emit events without state change

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-02-20-Hats Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md)_

---

In `changeHatMaxSupply()`, if the new **maxSupply** equals the previous **maxSupply**, the 
function doesn't actually change anything yet emits a supply changed event. It is 
recommended to validate the next supply is greater than the current one.
