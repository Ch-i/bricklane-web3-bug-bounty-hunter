---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-lizardstarking-4-8
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-02-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md
tags:
- firm:pashov-audit-group
- report:2023-02-01-lizardstarking
title: '[I-09] Use the `delete` keyword instead of assigning the default value of
  variables'
vuln_class: []
---

# [I-09] Use the `delete` keyword instead of assigning the default value of variables

_Section severity (from Solodit section header): Informational_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-LizardStarking.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md)_

---

In `withdrawStake the `timeLizardLocked`and`originalLockedLizardOwners`for a staked NFT are reset by assigning them to 0 or`address(0)`. It is a best practice is to just use the `delete` keyword instead, there is no need to manually assign the type's default values.
