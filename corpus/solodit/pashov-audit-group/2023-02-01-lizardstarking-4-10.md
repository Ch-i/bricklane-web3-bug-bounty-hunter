---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-lizardstarking-4-10
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-02-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md
tags:
- firm:pashov-audit-group
- report:2023-02-01-lizardstarking
title: '[I-11] Most state-changing methods do not emit events'
vuln_class: []
---

# [I-11] Most state-changing methods do not emit events

_Section severity (from Solodit section header): Informational_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-LizardStarking.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md)_

---

Examples for this are `setDepositsActive` or `setCouncilAddress` - state-changing methods should emit events so that off-chain monitoring can be implemented. Make sure to emit a proper event in each state-changing method to follow best practices.
