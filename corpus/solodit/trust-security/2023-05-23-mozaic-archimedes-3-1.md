---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-23-mozaic-archimedes-3-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-05-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md
tags:
- firm:trust-security
- report:2023-05-23-mozaic-archimedes
title: Theoretical reentrancy protection in MozToken
vuln_class: []
---

# Theoretical reentrancy protection in MozToken

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-05-23-Mozaic Archimedes.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md)_

---

MozToken guards against transferring of locked tokens using `_beforeTokenTransfer()` hook. It 
is recommended to instead use the `_afterTokenTransfer()` hook, because if the transfer 
operation somehow reenters MozToken `transfer()`, the check would be outdated.
