---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-04-01-florence-finance-3-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-04-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-Florence%20Finance.md
tags:
- firm:pashov-audit-group
- report:2023-04-01-florence-finance
title: '[L-03] Allowance check gives a false sense of security'
vuln_class: []
---

# [L-03] Allowance check gives a false sense of security

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-04-01-Florence Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-Florence%20Finance.md)_

---

The `LoanVault::createFundingAttempt` method contains the following allowance check:

```solidity
if (fundingToken.allowance(_msgSender(), address(this)) < fillableFundingTokenAmount) {
    revert Errors.InsufficientAllowance();
}
```

But it does not do a `transferFrom` for the `fundingToken` by itself. This means that the call to the method can be back-ran with an allowance revoke transaction. This will invalidate the check and later revert when the funding attempt is executed, so you are better off removing the check.
