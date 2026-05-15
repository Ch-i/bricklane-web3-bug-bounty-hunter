---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-04-13-lukso-lsp-audit-3-6
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-04-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md
tags:
- firm:trust-security
- report:2023-04-13-lukso-lsp-audit
title: Set up account owner migration from EOA to LSP6
vuln_class: []
---

# Set up account owner migration from EOA to LSP6

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-04-13-LUKSO LSP audit.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md)_

---

Once LSP6 becomes an account owner, all validations go through it. It seems easy to 
misconfigure the permissions and make an account uncallable when moving from an EOA 
owner to LSP6 owner. It is recommended to set up a validation at the smart contract level that 
the EOA can still access some key functionality.

**Team response:**
The way it is set is a design decision. We do not want to implement the recommendation as 
otherwise it would make it too custom. The LSP11 standard can be used to solve this problem, 
if the account owner lose access to its permissions to recover access.
