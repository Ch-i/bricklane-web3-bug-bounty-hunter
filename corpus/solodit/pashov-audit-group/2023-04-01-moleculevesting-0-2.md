---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-04-01-moleculevesting-0-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-04-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-MoleculeVesting.md
tags:
- firm:pashov-audit-group
- report:2023-04-01-moleculevesting
title: '[M-03] Contract can receive ETH but has no withdraw function for it'
vuln_class: []
---

# [M-03] Contract can receive ETH but has no withdraw function for it

_Section severity (from Solodit section header): Medium_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-04-01-MoleculeVesting.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-MoleculeVesting.md)_

---

**Impact:**
High, as value can be stuck forever

**Likelihood:**
Low, as it should be an error that someone sends ETH to the contract

**Description**

The `TokenVesting` contract has `receive` and `fallback` functions that are `payable`. If someone sends a transaction with `msg.value != 0` then the ETH will be stuck in the contract forever without a way for anyone to withdraw it.

**Recommendations**

Remove the `receive` and `fallback` functions since the ETH balance is not used in the contract anyway.
