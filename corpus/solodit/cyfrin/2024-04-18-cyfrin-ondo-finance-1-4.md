---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-18-cyfrin-ondo-finance-1-4
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-04-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md
tags:
- firm:cyfrin
- report:2024-04-18-cyfrin-ondo-finance
title: Misleading events are emitted when transferring a dust amount of rOUSG shares
vuln_class: []
---

# Misleading events are emitted when transferring a dust amount of rOUSG shares

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-18-cyfrin-ondo-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md)_

---

**Description:** Calling `ROUSG.transferShares` emits two events:

`TransferShares`: How much rOUSG shares were transferred
`Transfer`: How much rOUSG tokens were transferred

Calling this function with a dust amount will emit an event that a non-zero amount of shares was transferred, together with an event that zero tokens were transferred as the `getROUSGByShares` will round to 0.

**Ondo:**
Acknowledged.
