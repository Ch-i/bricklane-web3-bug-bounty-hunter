---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-parcel-payroll-3-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-02-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-Parcel%20Payroll.md
tags:
- firm:pashov-audit-group
- report:2023-02-01-parcel-payroll
title: '[I-05] Incorrect NatSpec'
vuln_class: []
---

# [I-05] Incorrect NatSpec

_Section severity (from Solodit section header): Informational_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-Parcel Payroll.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-Parcel%20Payroll.md)_

---

The NatSpec of the `ORG` struct in `Storage` is incorrect as it says there are `claimbles` and `autoClaim` parameters or struct fields but there are no such fields, so they should be removed from the NatSpec doc. Also the order of `approvers` and `approvalsRequired` should be switched.
