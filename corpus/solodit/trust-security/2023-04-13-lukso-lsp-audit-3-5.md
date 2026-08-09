---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-04-13-lukso-lsp-audit-3-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-04-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md
tags:
- firm:trust-security
- report:2023-04-13-lukso-lsp-audit
title: Improve logic in _verifyAllowedERC725YDataKeys()
vuln_class: []
---

# Improve logic in _verifyAllowedERC725YDataKeys()

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-04-13-LUKSO LSP audit.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md)_

---

When looping over the keys and validating them, if the number of keys found in the loop 
equals the input keys array length, it exits early. However, since some keys in the array are pre-validated in `_verifyCanSetData()`, this condition cannot be reached although all keys are 
already validated. The fix would be to supply an additional parameter which is the number of 
keys pre-validated, and add it to the number of keys found for the check. 

**Team response:**
Implemented for gas optimization.
