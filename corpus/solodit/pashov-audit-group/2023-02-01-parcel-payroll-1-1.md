---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-parcel-payroll-1-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-02-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-Parcel%20Payroll.md
tags:
- firm:pashov-audit-group
- report:2023-02-01-parcel-payroll
title: '[М-02] Usage of non-standard ERC20 tokens might lead to stuck funds'
vuln_class: []
---

# [М-02] Usage of non-standard ERC20 tokens might lead to stuck funds

_Section severity (from Solodit section header): Medium_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-Parcel Payroll.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-Parcel%20Payroll.md)_

---

**Impact:**
High, because tokens will be left stuck in `PayrollManager`

**Likelihood:**
Low, because there aren't many such ERC20 tokens

**Description**

The `executePayroll` method uses the `transfer` method of `ERC20`, but does not check if the returned `bool` value is `true`. This is problematic, because there are tokens on the blockchain which actually do not revert on failure but instead return `false` (example is `ZRX`). If such a token is used and a transfer fails, the tokens will be stuck in the `PayrollManager` smart contract forever.

**Recommendations**

Use the `SafeERC20` library from `OpenZeppelin` and change the `transfer` call to a `safeTransfer` call instead.
