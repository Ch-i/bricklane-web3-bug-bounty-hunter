---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-14-cyfrin-goldilocks-v1-1-1-4
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-04-14T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md
tags:
- firm:cyfrin
- report:2024-04-14-cyfrin-goldilocks-v1-1
title: '`Goldilend.liquidate()` might revert due to underflow'
vuln_class: []
---

# `Goldilend.liquidate()` might revert due to underflow

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-14-cyfrin-goldilocks-v1.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md)_

---

**Severity:** Medium

**Description:** In `repay()`, there would be a rounding during the `interest` calculation.

```solidity
  function repay(uint256 repayAmount, uint256 _userLoanId) external {
      Loan memory userLoan = loans[msg.sender][_userLoanId];
      if(userLoan.borrowedAmount < repayAmount) revert ExcessiveRepay();
      if(block.timestamp > userLoan.endDate) revert LoanExpired();
      uint256 interestLoanRatio = FixedPointMathLib.divWad(userLoan.interest, userLoan.borrowedAmount);
L425  uint256 interest = FixedPointMathLib.mulWadUp(repayAmount, interestLoanRatio); //@audit rounding issue
      outstandingDebt -= repayAmount - interest > outstandingDebt ? outstandingDebt : repayAmount - interest;
      ...
  }
...
  function liquidate(address user, uint256 _userLoanId) external {
      Loan memory userLoan = loans[msg.sender][_userLoanId];
      if(block.timestamp < userLoan.endDate || userLoan.liquidated || userLoan.borrowedAmount == 0) revert Unliquidatable();
      loans[user][_userLoanId].liquidated = true;
      loans[user][_userLoanId].borrowedAmount = 0;
L448  outstandingDebt -= userLoan.borrowedAmount - userLoan.interest;
      ...
  }
```

Here is a possible scenario.
- There are 2 borrowers of `borrowedAmount = 100, interest = 10`. And `outstandingDebt = 2 * (100 - 10) = 180`.
- The first borrower calls `repay()` with `repayAmount = 100`.
- Due to the rounding issue at L425, `interest` is 9 instead of 10. And `outstandingDebt = 180 - (100 - 9) = 89`.
- In `liquidate()` for the second borrower, it will revert at L448 because `outstandingDebt = 89 < borrowedAmount - interest = 90`.

**Impact:** `liquidate()` might revert due to underflow.

**Recommended Mitigation:** In `liquidate()`, `outstandingDebt` should be updated like the below.

```diff
  /// @inheritdoc IGoldilend
  function liquidate(address user, uint256 _userLoanId) external {
    Loan memory userLoan = loans[msg.sender][_userLoanId];
    if(block.timestamp < userLoan.endDate || userLoan.liquidated || userLoan.borrowedAmount == 0) revert Unliquidatable();
    loans[user][_userLoanId].liquidated = true;
    loans[user][_userLoanId].borrowedAmount = 0;
+  uint256 debtToRepay = userLoan.borrowedAmount - userLoan.interest;
+  outstandingDebt -= debtToRepay > outstandingDebt ? outstandingDebt : debtToRepay;
   ...
  }
```

**Client:** Fixed in [PR #10](https://github.com/0xgeeb/goldilocks-core/pull/10)

**Cyfrin:** Verified.
