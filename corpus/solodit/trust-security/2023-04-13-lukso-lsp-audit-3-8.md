---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-04-13-lukso-lsp-audit-3-8
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-04-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md
tags:
- firm:trust-security
- report:2023-04-13-lukso-lsp-audit
title: Whitelisting functionality for universal receiver delegate
vuln_class: []
---

# Whitelisting functionality for universal receiver delegate

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-04-13-LUKSO LSP audit.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md)_

---

The default receiver delegate can be easily spammed by faking the receiving of assets on the 
account. This would make enumerating on the received assets unfeasible. It may be beneficial 
to have a global whitelist of credible assets, and accounts can opt-in to only track assets in the 
whitelist.

**Team response:**
Considered to be implemented in future LSP Standards.
