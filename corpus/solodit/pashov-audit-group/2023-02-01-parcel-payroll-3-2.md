---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-parcel-payroll-3-2
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
title: '[I-03] Prefer Solidity Custom Errors over `require` statements with strings'
vuln_class: []
---

# [I-03] Prefer Solidity Custom Errors over `require` statements with strings

_Section severity (from Solodit section header): Informational_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-Parcel Payroll.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-Parcel%20Payroll.md)_

---

Using Solidity Custom Errors has the benefits of less gas spent in reverted transactions, better interoperability of the protocol as clients of it can catch the errors easily on-chain, as well as you can give descriptive names of the errors without having a bigger bytecode or transaction gas spending, which will result in a better UX as well. Remove all `require` statements and use Custom Errors instead.
