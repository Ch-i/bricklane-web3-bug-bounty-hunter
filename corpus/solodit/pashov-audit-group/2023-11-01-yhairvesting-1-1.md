---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-11-01-yhairvesting-1-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-11-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-11-01-yHairVesting.md
tags:
- firm:pashov-audit-group
- report:2023-11-01-yhairvesting
title: '[L-02] Pausing not implemented correctly'
vuln_class: []
---

# [L-02] Pausing not implemented correctly

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-11-01-yHairVesting.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-11-01-yHairVesting.md)_

---

Currently the `setPaused` method of `TokenVestingV2` says the following in its NatSpec - "Pauses or unpauses the release of tokens and claiming of schedules". The problem is that no method in the contract has the `whenNotPaused` or `whenPaused` modifiers, so the comment is wrong. Remove the `setPaused` method altogether.

#**Discussion**

**Pashov Audit Group:** the client put a `whenNotPaused` modifier on `createVestingSchedule` and `purchaseVSchedule` methods instead as a fix, which brings some centralization to schedule purchasing - the owner can block users from doing so.
