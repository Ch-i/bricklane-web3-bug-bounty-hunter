---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-04-01-florence-finance-3-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-04-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-Florence%20Finance.md
tags:
- firm:pashov-audit-group
- report:2023-04-01-florence-finance
title: '[L-02] Number of registered loan vaults should be capped'
vuln_class: []
---

# [L-02] Number of registered loan vaults should be capped

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-04-01-Florence Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-Florence%20Finance.md)_

---

The owner of the `LoanVaultRegistry` might call `registerLoanVault` too many times, which will make the `loanVaultIds` array very big. Calling `getLoanVaultIds` on-chain might result in a revert if the gas required for the call is too much (more than the block gas limit for example). It is recommended that you limit the number of loan vaults that can be registered, for example a maximum of 200.
