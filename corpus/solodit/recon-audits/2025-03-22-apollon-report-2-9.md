---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-2-9
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[M-10] `SwapOperations` `swapFee` is non deterministic and can cause people
  to lose funds'
vuln_class: []
---

# [M-10] `SwapOperations` `swapFee` is non deterministic and can cause people to lose funds

_Section severity (from Solodit section header): Medium_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

SwapOperations charges a fee that is computed by `SwapPair` as follows:

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/SwapPair.sol#L187-L209

```solidity
  function getSwapFee(uint postReserve0, uint postReserve1) public view override returns (uint feePercentage) {
    address nonStableCoin = token1; // find stable coin
    if (tokenManager.isDebtToken(nonStableCoin) && totalSupply > 0) {
      // query prices
      (uint oraclePrice, ) = priceFeed.getPrice(nonStableCoin); /// @audit not validated for staleness
      uint preDexPrice = _getDexPrice(reserve0, reserve1); /// @audit this is spot and can be altered in some way
      uint postDexPrice = _getDexPrice(postReserve0, postReserve1);

      // only apply the dynamic fee if the swap trades against the oracle peg
      if ( /// @audit ??? | No deviation threshold | Spot vs Oracle (Donate to reserves?)
        (postDexPrice > oraclePrice && postDexPrice > preDexPrice) ||
        (postDexPrice < oraclePrice && preDexPrice > postDexPrice)
      ) {
        uint avgDexPrice = (preDexPrice + postDexPrice) / 2;
        uint priceRatio = (oraclePrice * DECIMAL_PRECISION) / avgDexPrice; // 1e18
        return
          _calcFee(priceRatio > DECIMAL_PRECISION ? priceRatio - DECIMAL_PRECISION : DECIMAL_PRECISION - priceRatio) +
          swapOperations.getSwapBaseFee();
      }
    }

    return swapOperations.getSwapBaseFee();
  }
```

The fee uses the previous "spot ratio" and compares it against the new pre-fee "spot ratio"

This means that any transaction that alters the reserves between when a user signs their transaction and when it get's included in a block may alter the fee that a user pays

This creates scenario where, if a minority of users owns the majority of the LP tokens, they can perform donations to front-run swaps, which will cause benign users to pay an additional fee that they didn't intend to pay

**Mitigation**

Add an explicit check for the fees that will be paid on a swap as to ensure that's intended or within an acceptable range
