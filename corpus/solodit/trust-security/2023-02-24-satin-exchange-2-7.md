---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-24-satin-exchange-2-7
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-02-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md
tags:
- firm:trust-security
- report:2023-02-24-satin-exchange
title: TRST-L-8 The owner can acquire an arbitrary amount of voting power
vuln_class: []
---

# TRST-L-8 The owner can acquire an arbitrary amount of voting power

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-02-24-Satin.Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md)_

---

**Description:** 
The function `createLockForOwner()` in Ve.sol allows the owner of the protocol to mint a 
veSatin without requiring Satin/$CASH LP to be deposited. This allows the owner to get an 
arbitrary amount of voting power in the system.
