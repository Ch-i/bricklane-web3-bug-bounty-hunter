---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-04-13-lukso-lsp-audit-3-7
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
title: Limit transfer size per allowed call
vuln_class: []
---

# Limit transfer size per allowed call

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-04-13-LUKSO LSP audit.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md)_

---

LSP6 permissions either allow or disallow transfers for a specific function. From a practical 
perspective, it would seem necessary to limit spending to a certain amount, similar to how 
ERC20 allowances work. 

**Team response:**
This is a design decision. We want to keep it as it is for now.
