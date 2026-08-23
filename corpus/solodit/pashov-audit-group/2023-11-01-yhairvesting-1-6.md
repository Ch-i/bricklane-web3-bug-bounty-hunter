---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-11-01-yhairvesting-1-6
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-11-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-11-01-yHairVesting.md
tags:
- firm:pashov-audit-group
- report:2023-11-01-yhairvesting
title: '[L-07] Missing `INVALID` value in enum'
vuln_class: []
---

# [L-07] Missing `INVALID` value in enum

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-11-01-yHairVesting.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-11-01-yHairVesting.md)_

---

The current default value of the `Status` enum is `INITIALIZED`. This is error-prone as even for a vesting schedule that doesn't exist, when the schedule is a value in a mapping it has default values and its `Status` will be `INITIALIZED`. Make sure to add `INVALID` as a Status value with index 0 (the default one) to protect from subtle errors with default values.
