---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-3-23
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[L-24] `SwapOperations.addLiquidity` is not validating desired and min amounts'
vuln_class: []
---

# [L-24] `SwapOperations.addLiquidity` is not validating desired and min amounts

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

`addLiquidity` bases it's logic on the implicit invariant that `amountDesired` are greater than `minAmounts`

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/SwapOperations.sol#L242-L258

```solidity
    {
      (vars.reserveA, vars.reserveB) = getReserves(tokenA, tokenB);
      if (vars.reserveA == 0 && vars.reserveB == 0) {
        (amountA, amountB) = (amountADesired, amountBDesired); /// @audit First LP Can attack by massively imbalancing by performing a single sided swap or similar
      } else {
        uint amountBOptimal = quote(amountADesired, vars.reserveA, vars.reserveB);
        if (amountBOptimal <= amountBDesired) {
          if (amountBOptimal < amountBMin) revert InsufficientBAmount();
          (amountA, amountB) = (amountADesired, amountBOptimal);
        } else {
          uint amountAOptimal = quote(amountBDesired, vars.reserveB, vars.reserveA);
          assert(amountAOptimal <= amountADesired); /// @audit Looks wrong
          if (amountAOptimal < amountAMin) revert InsufficientAAmount();
          (amountA, amountB) = (amountAOptimal, amountBDesired);
        }
      }
    }
```

However this check is missing from `addLiquidity`

**Mitigation**

Add the following checks

```solidity
        if (amountADesired < amountAMin) revert InsufficientAmountADesired();
        if (amountBDesired < amountBMin) revert InsufficientAmountBDesired();
```

Also see: [Velodrome Router](https://github.com/velodrome-finance/contracts/blob/9e5a5748c3e2bcef7016cc4194ce9758f880153f/contracts/Router.sol#L172-L182)
