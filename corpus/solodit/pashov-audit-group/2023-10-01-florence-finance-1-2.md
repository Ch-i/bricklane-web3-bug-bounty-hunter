---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-10-01-florence-finance-1-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-10-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-10-01-Florence%20Finance.md
tags:
- firm:pashov-audit-group
- report:2023-10-01-florence-finance
title: '[L-03] Enforce initializer methods to be callable just once'
vuln_class: []
---

# [L-03] Enforce initializer methods to be callable just once

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-10-01-Florence Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-10-01-Florence%20Finance.md)_

---

The `setLoansOutstanding` method in `LoanVault` says in its NatSpec that "This is used for the initial deployment on Arbitrum." - the method should be callable only once. The same note is valid for the `initializeArbitrumBridging` method in token contracts in the codebase.
