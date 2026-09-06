---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-lizardstarking-4-13
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-02-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md
tags:
- firm:pashov-audit-group
- report:2023-02-01-lizardstarking
title: '[I-14] Naming problem in `onlyApprovedContracts`'
vuln_class: []
---

# [I-14] Naming problem in `onlyApprovedContracts`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-LizardStarking.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md)_

---

The `onlyApprovedContracts` modifier uses three different words for the same thing - `approved`, `allowed` and `whitelisted`. Stay consistent and use only one word for one meaning in the context of the protocol, for example `whitelisted`.
