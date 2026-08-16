---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-24-satin-exchange-2-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-02-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md
tags:
- firm:trust-security
- report:2023-02-24-satin-exchange
title: TRST-L-1 There is no functionality to remove a whitelisted token
vuln_class: []
---

# TRST-L-1 There is no functionality to remove a whitelisted token

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-02-24-Satin.Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md)_

---

**Description:**
SatinVoter.sol allows to whitelist tokens that can be used as rewards when creating new 
gauges, but there is no functionality that allows removing tokens from the whitelist. This can 
be problematic if some incompatibility and/or exploit is discovered in a whitelisted token.

**Recommended Mitigation:**
Add a function callable only by the owner that allows to remove tokens from the whitelist.

**Team Response:**
Fixed.

**Mitigation Review:**
The issue has been resolved as suggested, there’s now a function `removeWhitelist()` that 
allows removing tokens from the whitelist.
