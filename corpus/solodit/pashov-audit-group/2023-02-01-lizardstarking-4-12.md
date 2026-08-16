---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-lizardstarking-4-12
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
title: '[I-13] Make `isLizardWithdrawable` directly return the result of the check'
vuln_class: []
---

# [I-13] Make `isLizardWithdrawable` directly return the result of the check

_Section severity (from Solodit section header): Informational_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-LizardStarking.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md)_

---

There is no need to have an if-else statement in the method, instead just directly do:

```solidity
return block.timestamp - timeLizardLocked[_tokenId] >= 90 days;
```

in `isLizardWithdrawable`.
