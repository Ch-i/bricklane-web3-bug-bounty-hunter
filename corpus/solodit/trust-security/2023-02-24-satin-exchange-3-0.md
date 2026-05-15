---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-24-satin-exchange-3-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-02-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md
tags:
- firm:trust-security
- report:2023-02-24-satin-exchange
title: Initialize ReentrancyGuardUpgradable
vuln_class: []
---

# Initialize ReentrancyGuardUpgradable

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-02-24-Satin.Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md)_

---

Both Ve.sol and SatinVoter.sol import ReentrancyGuardUpgradable.sol, but in both 
instances it’s not initialized in the `initialize()` function. It is not strictly necessary for the guard 
functionality, but still a good practice.
