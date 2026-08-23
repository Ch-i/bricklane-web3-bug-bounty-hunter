---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-20-hats-protocol-2-6
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-02-20T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md
tags:
- firm:trust-security
- report:2023-02-20-hats-protocol
title: TRST-L-7 Reentrancy guards can be easily bypassed
vuln_class: []
---

# TRST-L-7 Reentrancy guards can be easily bypassed

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-02-20-Hats Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md)_

---

**Description:**
In `checkTransaction()`, **guardEntries** is incremented while in `checkAfterExecution()`, it is 
decremented, implementing a basic reentrancy guard.
The issue is that both functions lack a msg.sender check. Therefore, if there was a way to 
exploit the contract using a reentrancy, this defense would be futile. Attacker could simply 
call `checkTransaction()` an unlimited amount of times, with valid arguments. Then, 
`checkAfterExecution()` would never overflow from the reentrancy abuse.

**Recommended mitigation:**
Check that the msg.sender is the safe for the two functions above.

**Team response:**
Accepted.

**Team response:**
Fixed
