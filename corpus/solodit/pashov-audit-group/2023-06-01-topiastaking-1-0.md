---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-06-01-topiastaking-1-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-06-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-06-01-TopiaStaking.md
tags:
- firm:pashov-audit-group
- report:2023-06-01-topiastaking
title: '[M-01] Multiple centralization vulnerabilities can break the protocol'
vuln_class: []
---

# [M-01] Multiple centralization vulnerabilities can break the protocol

_Section severity (from Solodit section header): Medium_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-06-01-TopiaStaking.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-06-01-TopiaStaking.md)_

---

**Description**

Multiple methods in `TopiaLpStaking` are centralization vulnerabilities and some can be used to break the protocol for users:

- `setRewardsToken` can be used to update the `rewardsToken` address to a random one, making all reward claims revert, leading to stuck funds
- `setUniswapPair` can be used to update the `uniswapPair` address to a random one, making all stakes/unstakes revert, leading to stuck funds
- `addLockupInterval` can be used to add strange lockup intervals with huge multipliers

The `setRewards` method has multiple problems in itself:

- can be called multiple times, pushing the reward period away with every call
- the `_start` value can be too further away in the future
- the `_end` value can already have passed
- the duration between `_start` and `_end` might be too large (for example 70 years)
- the contract balance of reward tokens is not validated - this can mean users won't be guaranteed to be able to claim their rewards

**Recommendations**

Make the `rewardsToken`, `uniswapPair` and `lockupIntervals` immutable variables, there shouldn't be a need to change them. Also make sure `setRewards` is callable just once.

**Discussion**

**pashov:** Fixed.
