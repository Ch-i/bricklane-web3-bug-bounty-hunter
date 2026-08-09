---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-14-cyfrin-goldilocks-v1-1-0-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-04-14T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md
tags:
- firm:cyfrin
- report:2024-04-14-cyfrin-goldilocks-v1-1
title: Wrong `PoolSize` increment in `Goldilend.repay()`
vuln_class: []
---

# Wrong `PoolSize` increment in `Goldilend.repay()`

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-14-cyfrin-goldilocks-v1.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md)_

---

**Severity:** High

**Description:** When a user repays his loan using `repay()`, it increases `poolSize` with the repaid interest. During the increment, it uses the wrong amount.

```solidity
  function repay(uint256 repayAmount, uint256 _userLoanId) external {
    Loan memory userLoan = loans[msg.sender][_userLoanId];
    if(userLoan.borrowedAmount < repayAmount) revert ExcessiveRepay();
    if(block.timestamp > userLoan.endDate) revert LoanExpired();
    uint256 interestLoanRatio = FixedPointMathLib.divWad(userLoan.interest, userLoan.borrowedAmount);
    uint256 interest = FixedPointMathLib.mulWadUp(repayAmount, interestLoanRatio);
    outstandingDebt -= repayAmount - interest > outstandingDebt ? outstandingDebt : repayAmount - interest;
    loans[msg.sender][_userLoanId].borrowedAmount -= repayAmount;
    loans[msg.sender][_userLoanId].interest -= interest;
    poolSize += userLoan.interest * (1000 - (multisigShare + apdaoShare)) / 1000; //@audit should use interest instead of userLoan.interest
...
  }
```

It should use `interest` instead of `userLoan.interest` because the user repaid `interest` only.

**Impact:** `poolSize` would be tracked wrongly after calling `repay()` and several functions wouldn't work as expected.

**Recommended Mitigation:** `poolSize` should be updated using `interest`.

**Client:** Fixed in [PR #2](https://github.com/0xgeeb/goldilocks-core/pull/2)

**Cyfrin:** Verified.
