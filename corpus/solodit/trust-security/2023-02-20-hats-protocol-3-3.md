---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-20-hats-protocol-3-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-02-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md
tags:
- firm:trust-security
- report:2023-02-20-hats-protocol
title: Improving display of information
vuln_class: []
---

# Improving display of information

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-02-20-Hats Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md)_

---

In _constructURI(), the printed JSON string is composed of some properties.
```solidity
        // split into two objects to avoid stack too deep error
                string memory idProperties = string.concat('"domain": "',
                     LibString.toString(getTophatDomain(_hatId)), '", "id": "',
                        LibString.toString(_hatId), '", "pretty id": "', "{id}", '",'
        );
```
It is recommended to change the {id} placeholder to a more informative value, such as 
`LibString.toHexString(_hatId, 32)`
