---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-04-13-lukso-lsp-audit-1-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-04-13T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md
tags:
- firm:trust-security
- report:2023-04-13-lukso-lsp-audit
title: TRST-M-5 renounceOwnership will accidentally be one-step in a certain time
  period
vuln_class: []
---

# TRST-M-5 renounceOwnership will accidentally be one-step in a certain time period

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-04-13-LUKSO LSP audit.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md)_

---

**Description:** 
In `_renounceOwnership()`, if renouncing did not start yet, **confirmationPeriodStart** and 
**confirmationPeriodEnd** will be 100 and 200 respectively. This means that if the current block 
is between those values, logic will funnel to the second stage handling. This is dangerous as 
we know Lukso will start from a new genesis block and other blockchains may use the same 
LSP code when they boot.

**Recommended Mitigation:**
If **_renounceOwnershipStartedAt** is zero, perform the first step regardless.

**Team response:**
Fixed (applied recommendation).

**Mitigation review:**
Fixed.
