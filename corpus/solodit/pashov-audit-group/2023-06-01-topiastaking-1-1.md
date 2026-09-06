---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-06-01-topiastaking-1-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-06-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-06-01-TopiaStaking.md
tags:
- firm:pashov-audit-group
- report:2023-06-01-topiastaking
title: '[M-02] Rewards can possibly be left stuck in contract'
vuln_class: []
---

# [M-02] Rewards can possibly be left stuck in contract

_Section severity (from Solodit section header): Medium_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-06-01-TopiaStaking.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-06-01-TopiaStaking.md)_

---

**Description**

Currently in `TopliaLpStaking::setRewards` we have this comment:

> // This must be called AFTER some LP are staked (or ensure at least 1 LP position is staked before the start timestamp)

While the issue is pointed out here, it is not enforced in a smart contract native manner and the code is still vulnerable. The problem is that if the `rewardsPeriod.start` timestamp has passed and no one has staked, the rewards accumulated until the first stake will be forever stuck in the contract, due to the `stake` method calling `updateRewardsPerWeight` before actually setting the staker's checkpoint.

**Recommendations**

Add a mechanism to ensure that at least 1 user has staked before `rewardsPeriod.start` - one possible solution is enforcing that there was at least one stake before calling `setRewards` and that `_start >= block.timestamp`.

**Discussion**

**pashov:** Fixed.
