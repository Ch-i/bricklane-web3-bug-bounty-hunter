---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-lizardstarking-4-2
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
title: '[I-03] Method and storage variables can be removed'
vuln_class: []
---

# [I-03] Method and storage variables can be removed

_Section severity (from Solodit section header): Informational_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-LizardStarking.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md)_

---

Rename `stakePoolClaims` to `rewardsClaimed`, remove `isRewardsClaimed` and then just use the automatically generated getter of it for simplicity. This will also result in a gas optimization. Also, the `resetCounter` and `rebaseCounter` storage variables are not read on-chain so you can just emit events on `reset` or `rebase` and do the counting off-chain.
