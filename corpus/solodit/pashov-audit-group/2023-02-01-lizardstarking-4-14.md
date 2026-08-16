---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-lizardstarking-4-14
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
title: '[I-15] The `IERC721` interface is not needed'
vuln_class: []
---

# [I-15] The `IERC721` interface is not needed

_Section severity (from Solodit section header): Informational_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-LizardStarking.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md)_

---

The `IEthlizards` interface imports and inherits from the `IERC721` interface - this is not needed as none of its methods are used. Remove the `IERC721` inteface and its import.
