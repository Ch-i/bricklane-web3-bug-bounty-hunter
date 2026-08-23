---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-11-01-yhairvesting-0-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-11-01T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-11-01-yHairVesting.md
tags:
- firm:pashov-audit-group
- report:2023-11-01-yhairvesting
title: '[H-01] `createVestingSchedule` can be front-ran by another holder of `ROLE_CREATE_SCHEDULE`
  role'
vuln_class: []
---

# [H-01] `createVestingSchedule` can be front-ran by another holder of `ROLE_CREATE_SCHEDULE` role

_Section severity (from Solodit section header): High_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-11-01-yHairVesting.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-11-01-yHairVesting.md)_

---

**Severity**

**Impact:**
High, as vesting token balance can be stolen

**Likelihood:**
Medium, as it requires front-running

**Description**

The `createVestingSchedule` method of `TokenVestingV2` expects to have a pre-transferred balance before initializing a vesting schedule. The problem with the current contract version is that multiple accounts can hold the `ROLE_CREATE_SCHEDULE` role. Since two transactions are expected to create a vesting schedule (transferring funds to the `TokenVestingV2` contract and then calling `createVestingSchedule`) this means that between them another holder of the role can come in and create a vesting schedule of his own (with himself as beneficiary for example, non-revokable with just 7 days of duration) and in this way steal the funds of the other role holder.

**Recommendations**

Either change `createVestingSchedule` to itself transfer the vesting schedule tokens from the caller to the contract or make it callable by just 1 address
