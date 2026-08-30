---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-04-13-lukso-lsp-audit-3-2
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
title: Specification improvements
vuln_class: []
---

# Specification improvements

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-04-13-LUKSO LSP audit.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md)_

---

1. LSP20 specification should specify explicitly that the **callResult** passed to 
`lsp20VerifyCallResult()` would be an empty **bytes**, if the called function does not return 
values.
2. LSP0 specification states about the universal receiver:
"If an address is stored under the data key attached below and and this address is a 
contract that supports the LSP1UniversalReceiver interface id, forwards the call to 
the `universalReceiver(bytes32,bytes)` function on the address retreived. If there is no 
address stored under this data key, execution continues normally."
It would be good to clarify that execution continues normally also in the case that 
the address does not support LSP1UniversalReceiver interface id (rather than revert, 
for example).

**Team response:**
Documented in specs.
