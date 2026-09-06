---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-lizardstarking-2-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-02-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md
tags:
- firm:pashov-audit-group
- report:2023-02-01-lizardstarking
title: '[M-01] Looping over unbounded array can result in a state of DoS'
vuln_class: []
---

# [M-01] Looping over unbounded array can result in a state of DoS

_Section severity (from Solodit section header): Medium_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-LizardStarking.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md)_

---

**Impact:**
High, as the contract will be in a state of DoS, without a way for anyone to withdraw NFTs or claim rewards

**Likelihood:**
Low, as it requires a lot of pools added or a malicious owner

**Description**

The `claimCalculation` and `getCurrentShareRaw` methods both loop over the `pool` array to do proper calculations. The problems is that there is no way to pop elements out of the array, but there is no upper bound on the length of the array. Each time the `currentRewards` are more than or equal to the `minResetValue`, the `createPool` method will be called, adding a new element to the `pool` array. If at some point there are now a large number of pools, iterating over them will become very costly and can result in a gas cost that is over the block gas limit. This will mean that a transaction cannot be executed anymore, leaving the contract's main functionalities (withdrawing the staked NFTs and claiming rewards) in a state of DoS.

**Recommendations**

Limit the number of pools that can be created, for example a maximum of 25 pools created.
