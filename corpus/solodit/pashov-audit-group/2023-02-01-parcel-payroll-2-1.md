---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-parcel-payroll-2-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-02-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-Parcel%20Payroll.md
tags:
- firm:pashov-audit-group
- report:2023-02-01-parcel-payroll
title: '[L-02] The `PayrollManager` contract has less than 5% code coverage'
vuln_class: []
---

# [L-02] The `PayrollManager` contract has less than 5% code coverage

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-Parcel Payroll.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-Parcel%20Payroll.md)_

---

Some security vulnerabilities are more easily caught in a normal unit testing scenario than in a full line-by-line manual audit. It is strongly recommended to strive for close to 100% code coverage on all of the code that you are about to deploy so no low-hanging fruit bugs are left in the contracts.
