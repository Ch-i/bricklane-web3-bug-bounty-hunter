---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-parcel-payroll-0-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-02-01T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-Parcel%20Payroll.md
tags:
- firm:pashov-audit-group
- report:2023-02-01-parcel-payroll
title: '[C-01] Contract is missing a `payable` function which makes it impossible
  to operate with native assets'
vuln_class: []
---

# [C-01] Contract is missing a `payable` function which makes it impossible to operate with native assets

_Section severity (from Solodit section header): High_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-Parcel Payroll.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-Parcel%20Payroll.md)_

---

**Impact:**
High, as all transactions that use native assets will revert

**Likelihood:**
High, as it is well expected that native assets will be used as a `paymentToken` often

**Description**

The `PayrollManager` does not have a `receive` function that is marked as `payable` neither any `payable` function at all. This will make it impossible for the contract to work with native assets because all transfers from the Gnosis Safe multisig to him will revert.

**Recommendations**

Add a `payable` `fallback` or `receive` function in `PayrollManager` to allow for native assets transfers.
