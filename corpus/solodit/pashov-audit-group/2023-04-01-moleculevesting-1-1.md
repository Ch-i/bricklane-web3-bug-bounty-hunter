---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-04-01-moleculevesting-1-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-04-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-MoleculeVesting.md
tags:
- firm:pashov-audit-group
- report:2023-04-01-moleculevesting
title: '[L-02] The `onlyIfVestingScheduleNotRevoked` modifier will not revert even
  if the given `vestingScheduleId` is non-existent'
vuln_class: []
---

# [L-02] The `onlyIfVestingScheduleNotRevoked` modifier will not revert even if the given `vestingScheduleId` is non-existent

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-04-01-MoleculeVesting.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-MoleculeVesting.md)_

---

The modifier will pass successfully when the `vestingScheduleId` passed is of a non-existent vesting schedule, because the default `Status` of a vesting schedule is `INITIALIZED` anyway. Validate that the `vestingSchedules` exists, by checking that `vestingSchedules[vestingScheduleId].duration != 0`.
