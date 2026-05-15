---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-04-01-moleculevesting-0-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-04-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-MoleculeVesting.md
tags:
- firm:pashov-audit-group
- report:2023-04-01-moleculevesting
title: '[M-02] Insufficient input validation in function `createVestingSchedule`'
vuln_class: []
---

# [M-02] Insufficient input validation in function `createVestingSchedule`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-04-01-MoleculeVesting.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-MoleculeVesting.md)_

---

**Impact:**
High, as it can lead to users never vesting their tokens

**Likelihood:**
Low, as it requires a malicious/compromised admin or an error on his side

**Description**

The input arguments of the `createVestingSchedule` function are not sufficiently validated. Here are some problematic scenarios:

1. `_start` can be a timestamp that has already passed or is too far away in the future
2. `_cliff` can be too big, users won't be able to claim
3. 1 is a valid value for `duration`, the `!= 0` check is insufficient
4. If `_slicePeriodSeconds` is too big then the math in `_computeReleasableAmount` will have rounding errors

**Recommendations**

Add sensible lower and upper bounds for all arguments of the `createVestingSchedule` method.
