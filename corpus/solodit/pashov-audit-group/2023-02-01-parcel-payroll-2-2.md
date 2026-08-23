---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-parcel-payroll-2-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-02-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-Parcel%20Payroll.md
tags:
- firm:pashov-audit-group
- report:2023-02-01-parcel-payroll
title: '[L-03] Missing array arguments length check'
vuln_class: []
---

# [L-03] Missing array arguments length check

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-Parcel Payroll.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-Parcel%20Payroll.md)_

---

In `PayrollManager::executePayroll` there is a check that most arrays have the same length, but a check that `paymentTokens.length == payoutAmounts.length` is missing and should be added.
