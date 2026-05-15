---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-parcel-payroll-1-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-02-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-Parcel%20Payroll.md
tags:
- firm:pashov-audit-group
- report:2023-02-01-parcel-payroll
title: '[M-01] Using the `transfer` function of `address payable` is discouraged'
vuln_class: []
---

# [M-01] Using the `transfer` function of `address payable` is discouraged

_Section severity (from Solodit section header): Medium_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-Parcel Payroll.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-Parcel%20Payroll.md)_

---

**Impact:**
Medium, as payroll will revert and Merkle Trees & approvals would have to be done again

**Likelihood:**
Medium, as it happens any time the recipient is a smart contract or a multisig wallet that has a receive function taking up more than 2300 gas

**Description**

The `executePayroll` function uses the `transfer` method of `address payable` to transfer native asset funds to a recipient address. This address is set by the caller but is also encoded in the leaf of a Merkle Tree that is created off-chain. It is possible that this recipient is a smart contract that has a `receive` or `fallback` function that takes up more than the 2300 gas which is the limit of `transfer`. Examples are some smart contract wallets or multi-sig wallets, so usage of `transfer` is discouraged.

**Recommendations**

Use a `call` with value instead of `transfer`. The function already has a `nonReentrant` modifier so reentrancy is not a problem here.
