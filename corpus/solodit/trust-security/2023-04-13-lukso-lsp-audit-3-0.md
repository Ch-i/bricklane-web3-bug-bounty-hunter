---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-04-13-lukso-lsp-audit-3-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-04-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md
tags:
- firm:trust-security
- report:2023-04-13-lukso-lsp-audit
title: The uncheckedIncrement() code is not efficient
vuln_class: []
---

# The uncheckedIncrement() code is not efficient

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-04-13-LUKSO LSP audit.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md)_

---

**Description:**
In various places a loop construct is used as below:
```solidity
         for (uint256 i; i < data.length; i = GasLib.uncheckedIncrement(i)) {
```
The resulting bytecode is actually unoptimized compared to an inline unchecked block. This 
creates a jump and several additional opcodes as overhead.

**Team response:**
Fixed
