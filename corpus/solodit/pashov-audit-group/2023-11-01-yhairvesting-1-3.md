---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-11-01-yhairvesting-1-3
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
title: '[L-04] Missing input validation in token price setters'
vuln_class: []
---

# [L-04] Missing input validation in token price setters

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-11-01-yHairVesting.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-11-01-yHairVesting.md)_

---

The `setVTokenCost` and `setTokenCost` methods are missing lower and upper bounds, meaning the caller of them can set for example huge values so tokens are not actually purchasable. Make sure to put a sensible upper bound and possibly a lower bound on the values that you can set in those methods.
