---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-parcel-payroll-3-7
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-02-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-Parcel%20Payroll.md
tags:
- firm:pashov-audit-group
- report:2023-02-01-parcel-payroll
title: '[I-08] Inconsistent and unsafe pragma statements used'
vuln_class: []
---

# [I-08] Inconsistent and unsafe pragma statements used

_Section severity (from Solodit section header): Informational_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-Parcel Payroll.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-Parcel%20Payroll.md)_

---

It is a best practice to use a stable pragma statement so you can lock the compiler version and get the same bytecode in each compilation deterministically. Also it is recommended to use the same Solidity version throughout the codebase, but this is not the case currently. Change all pragma statements to use the same version and lock the pragma.
