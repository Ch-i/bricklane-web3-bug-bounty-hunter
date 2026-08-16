---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-2-10
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[M-11] `SwapOperations` is performing some swaps without updating the price,
  resulting in incorrect fees being charged'
vuln_class: []
---

# [M-11] `SwapOperations` is performing some swaps without updating the price, resulting in incorrect fees being charged

_Section severity (from Solodit section header): Medium_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**
Operations such as: `swapExactTokensForTokens`, `swapTokensForExactTokens` receive `_priceUpdateData` but update the price only at the `_swap` operation

`_swap` uses `getAmountsOut` and `getAmountsIn` to determine the price at which to charge fees at

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/SwapOperations.sol#L469-L484

```solidity

  function swapExactTokensForTokens(
    uint amountIn,
    uint amountOutMin,
    address[] calldata path,
    address to,
    uint deadline,
    bytes[] memory _priceUpdateData
  ) public payable virtual override ensure(deadline) returns (SwapAmount[] memory amounts) {
    amounts = getAmountsOut(amountIn, path); /// @audit Used old prices
    if (amounts[amounts.length - 1].amount < amountOutMin) revert InsufficientOutputAmount();

    safeTransferFrom(path[0], msg.sender, getPair[path[0]][path[1]], amounts[0].amount);
    _swap(amounts, path, to, _priceUpdateData, false); /// @audit Updates prices after having used old prices
  }
```

This means that fees on swaps are computed on the stale price rather then the latest

Because oracle prices can be updated via other operations, this also allows swappers to pick the most optimal price at which to pay the lowest fee  


**Mitigation**

You can ensure the price is updated by:
- Forcing the update in all external functions
- Performing the staleness check in `getSwapFee`
