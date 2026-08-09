---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-24-satin-exchange-2-8
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-02-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md
tags:
- firm:trust-security
- report:2023-02-24-satin-exchange
title: TRST-L-9 The owner can mint an arbitrary amount of Satin
vuln_class: []
---

# TRST-L-9 The owner can mint an arbitrary amount of Satin

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-02-24-Satin.Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md)_

---

**Description:** 
The function `ownerMint()` allows the owner to mint an arbitrary amount of Satin. If the 
owner is compromised this can make the protocol collapse instantly. Consider limiting the 
power of the owner account.

**Team Response:**
"Both capabilities will be walled behind a 5/9 ecosystem multisig, with 36 hour timelock."
