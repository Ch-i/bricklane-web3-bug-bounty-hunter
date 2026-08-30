---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-lizardstarking-4-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-02-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md
tags:
- firm:pashov-audit-group
- report:2023-02-01-lizardstarking
title: '[I-01] No need to use `safeTransfer` since contracts are not allowed'
vuln_class: []
---

# [I-01] No need to use `safeTransfer` since contracts are not allowed

_Section severity (from Solodit section header): Informational_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-LizardStarking.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md)_

---

The `depositStake` method disallows contract calling it (even though code is commented out, it says it will be uncommented out) so you never need to do use the ERC721 `_safeTransfer` functionality since it is always done to the initial depositor. Use the normal `_transfer` functionality instead.
