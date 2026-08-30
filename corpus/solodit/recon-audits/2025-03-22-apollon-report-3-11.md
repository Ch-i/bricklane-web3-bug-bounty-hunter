---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-3-11
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[L-12] `SwapOperation` First LP pays no fee and can set the price to an incorrect
  value, causing losses to traders, and higher fees'
vuln_class: []
---

# [L-12] `SwapOperation` First LP pays no fee and can set the price to an incorrect value, causing losses to traders, and higher fees

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

`addLiquidity` looks as follows

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/SwapOperations.sol#L228-L246

```solidity
  function addLiquidity(
    address tokenA,
    address tokenB,
    uint amountADesired,
    uint amountBDesired,
    uint amountAMin,
    uint amountBMin,
    PriceUpdateAndMintMeta memory _priceAndMintMeta,
    uint deadline
  ) public payable virtual override ensure(deadline) returns (uint amountA, uint amountB, uint liquidity) {
    ProvidingVars memory vars;
    vars.pair = getPair[tokenA][tokenB]; /// @audit QA not sorting tokens means this can revert | No fix is ok but it's a gotcha
    if (vars.pair == address(0)) revert PairDoesNotExist();
    /// @audit not checking that min < desired - S
    {
      (vars.reserveA, vars.reserveB) = getReserves(tokenA, tokenB);
      if (vars.reserveA == 0 && vars.reserveB == 0) {
        (amountA, amountB) = (amountADesired, amountBDesired); /// @audit First LP Can attack by massively imbalancing by performing a single sided swap or similar
      } else {
```

When no liquidity was previously added, the ratio for the LP will be taken at face value

This could be used by the first depositor to purposefully imbalance the pool, as a means to take on debts that either allow them to be closer to delta neutral, or as a means to grief other users

**Mitigation**

Consider using a ratio that is taken from the oracles
