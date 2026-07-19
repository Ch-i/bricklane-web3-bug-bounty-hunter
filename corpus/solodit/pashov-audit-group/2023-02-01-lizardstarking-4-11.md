---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-lizardstarking-4-11
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-02-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md
tags:
- firm:pashov-audit-group
- report:2023-02-01-lizardstarking
title: '[I-12] Interface is not needed'
vuln_class: []
---

# [I-12] Interface is not needed

_Section severity (from Solodit section header): Informational_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-LizardStarking.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md)_

---

The `IUSDc` interface is not needed in the codebase - import the OpenZeppelin `IERC20` interface and use it instead. Also remove the `ABDKMath64x64` from the codebase and just import it as an external dependency, as there is no need to keep it there.
