---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-04-01-moleculevesting-1-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-04-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-MoleculeVesting.md
tags:
- firm:pashov-audit-group
- report:2023-04-01-moleculevesting
title: '[L-01] Limit the max size of the `vestingSchedulesIds` array and `holdersVestingScheduleCount`'
vuln_class: []
---

# [L-01] Limit the max size of the `vestingSchedulesIds` array and `holdersVestingScheduleCount`

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-04-01-MoleculeVesting.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-MoleculeVesting.md)_

---

If too many vesting schedules are added for a user it is possible that the `getVestingSchedulesIds` method will take too much gas and won't be executable (if it gets over the block gas limit, for example). Also in `releaseAvailableTokensForHolder` there is a `for` loop that loops `vestingScheduleCount` number of times, which can also be problematic, as it can lead to a DoS state with the function. Limit the max size of both, for example up to 500 vesting schedules created from the contract.
