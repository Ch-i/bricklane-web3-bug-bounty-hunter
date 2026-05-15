---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-11-01-yhairvesting-1-0
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
title: '[L-01] Flawed access control'
vuln_class: []
---

# [L-01] Flawed access control

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-11-01-yHairVesting.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-11-01-yHairVesting.md)_

---

The `setVTokenCost` and `setTokenCost` methods are callable only by `ROLE_CREATE_SCHEDULE` role holder. The methods decide the cost of purchasing vesting schedules. This should be a function of the `DEFAULT_ADMIN_ROLE` instead, since a role that creates schedules shouldn't decide their pricing.
