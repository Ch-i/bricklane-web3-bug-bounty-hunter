---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-20-hats-protocol-1-7
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-02-20T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md
tags:
- firm:trust-security
- report:2023-02-20-hats-protocol
title: TRST-M-8 Safety checks compare safe's threshold with a stale value
vuln_class: []
---

# TRST-M-8 Safety checks compare safe's threshold with a stale value

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-02-20-Hats Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md)_

---

**Description:**
In HatsSignerGateBase, `_correctThreshold()` calculates what the safe's threshold should be. 
However, it uses **signerCount** without updating it by calling `reconcileSignerCount()`. 
Therefore, in `checkAfterExecution()`, the safe's current threshold will be compared to potentially the wrong value. This may trip valid transactions or allow malicious ones to go 
through, where the threshold should end up being higher.

**Recommended mitigation:**
Call `reconcileSignerCount()` before making use of the signerCount value.

**Team response:**
Accepted; added `_countValidSigners()` rather than `reconcileSignerCount()`.

**Mitigation review:**
Fixed.
