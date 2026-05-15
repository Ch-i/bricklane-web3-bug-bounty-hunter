---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-lizardstarking-3-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-02-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md
tags:
- firm:pashov-audit-group
- report:2023-02-01-lizardstarking
title: '[L-04] Division before multiplication in the `calculateShareFromTime` method'
vuln_class: []
---

# [L-04] Division before multiplication in the `calculateShareFromTime` method

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-LizardStarking.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md)_

---

The `requiredRebases` variable is calculated by using division by `1 days`. It can unexpectedly round down to zero but this won't lead to any problems, as then the result is passed to the `calculateRebasePercentage` method, where it is used as a "power of" value, so then the `calculateRebasePercentage` will return 1 even if it received 0 as an argument. This should be well documented and understood by developers and auditors. Add proper comments in the code.
