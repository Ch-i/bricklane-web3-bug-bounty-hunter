---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-04-13-lukso-lsp-audit-3-1
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
title: Improve code documentation
vuln_class: []
---

# Improve code documentation

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-04-13-LUKSO LSP audit.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md)_

---

1. In LSP0ERC725AccountInitAbstract, the `_initialize()` call doesn't initialize the parents 
as they don't have non-zero initial state. It is worth explicitly noting this as usually 
derived Proxy classes have to initialize parent contracts.
2. Copy-paste error in documentation of 
`_getPermissionToSetAllowedERC725YDataKeys()`
```solidity
      @dev retrieve the permission required to set some AllowedCalls  for a controller.
```
**Team response:**
Fixed Natspec.
