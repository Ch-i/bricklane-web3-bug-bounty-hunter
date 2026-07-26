---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-04-13-lukso-lsp-audit-1-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-04-13T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md
tags:
- firm:trust-security
- report:2023-04-13-lukso-lsp-audit
title: TRST-M-3 LSP0 allows delegate calls when LSP20 post-execution check is required
vuln_class: []
---

# TRST-M-3 LSP0 allows delegate calls when LSP20 post-execution check is required

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-04-13-LUKSO LSP audit.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md)_

---

**Description:**
LSP20 call verification protects actions on an LSP0 account. The pre-execution check may mark 
the action as requiring a post-execution check. However, in the case of **delegate call** execution, the post-execution check can never be guaranteed to execute. The called contract 
may call the SELFDESTRUCT opcode and destroy the calling contract. Call flow returns 
immediately from the call to `execute()`, without executing the necessary check.


**Recommended Mitigation:**
When the first call verification marks a secondary call as necessary, disallow **delegate call**
execution. The fix should be applied to both `execute()` variants.

**Team Response:**
The use of **delegatecall** with **selfdestruct** will result in the destruction of the contract, in this 
case, the post-execution check will not run. However, **delegatecall** could be used in other 
scenarios requiring a post-execution check. We decided not to remove the post-execution 
check because of only one edge case.
