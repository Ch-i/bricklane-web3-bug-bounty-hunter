---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-04-13-lukso-lsp-audit-3-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-04-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md
tags:
- firm:trust-security
- report:2023-04-13-lukso-lsp-audit
title: Avoid reverts which break specs
vuln_class: []
---

# Avoid reverts which break specs

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-04-13-LUKSO LSP audit.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md)_

---

In LSP0ERC725AccountCore's `isValidSignature()`, when owner is an EOA, ECDSA.recover() is 
used to fetch the signer. However, that function will revert if the signature is invalid. This 
function should only return **MAGICVALUE** or **FAILVALUE**, so it would be best to refactor and 
return **FAILVALUE** when the signature is invalid.

**Team response:**
Fixed
