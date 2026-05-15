---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-11-01-yhairvesting-1-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-11-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-11-01-yHairVesting.md
tags:
- firm:pashov-audit-group
- report:2023-11-01-yhairvesting
title: '[L-03] Possible DoS in `getVestingSchedulesIds`'
vuln_class: []
---

# [L-03] Possible DoS in `getVestingSchedulesIds`

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-11-01-yHairVesting.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-11-01-yHairVesting.md)_

---

The `getVestingSchedulesIds` method copies the whole `vestingSchedulesIds` array to memory, which due to memory expansion costs can cost a huge amount of gas. Pushing to the array is unbounded, so if it gets too big then the gas needed for the method call can be more than the block gas limit or just too expensive to execute. Make sure to limit the size of the array so that such error can't happen.
