---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-01-cyfrin-sorella-l2-angstrom-v2-1-2-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-10-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-01-cyfrin-sorella-l2-angstrom-v2-1
title: '`CompensationPriceFinder` amount delta rounding directions are not consistent
  with Uniswap'
vuln_class: []
---

# `CompensationPriceFinder` amount delta rounding directions are not consistent with Uniswap

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md)_

---

**Description:** `CompensationPriceFinder::getZeroForOne` and `CompensationPriceFinder::getOneForZero` both round down in every instance when invoking `SqrtPriceMath::getAmount0Delta` and `SqrtPriceMath::getAmount1Delta`:

```solidity
uint256 delta0 =
    SqrtPriceMath.getAmount0Delta(priceLowerSqrtX96, priceUpperSqrtX96, liquidity, false);
uint256 delta1 =
    SqrtPriceMath.getAmount1Delta(priceLowerSqrtX96, priceUpperSqrtX96, liquidity, false);
```

To be consistent with how Uniswap charges swaps in `SwapMath::computeSwapStep`, the input token delta should round depending on whether the swap is an exact input or an exact output swap:

```solidity
if (exactIn) {
    uint256 amountRemainingLessFee =
        FullMath.mulDiv(uint256(-amountRemaining), MAX_SWAP_FEE - _feePips, MAX_SWAP_FEE);
    amountIn = zeroForOne
@>      ? SqrtPriceMath.getAmount0Delta(sqrtPriceTargetX96, sqrtPriceCurrentX96, liquidity, true)
@>      : SqrtPriceMath.getAmount1Delta(sqrtPriceCurrentX96, sqrtPriceTargetX96, liquidity, true);
    if (amountRemainingLessFee >= amountIn) {
        // `amountIn` is capped by the target price
        ...
    } else {
        // exhaust the remaining amount
        ...
    }
    amountOut = zeroForOne
@>      ? SqrtPriceMath.getAmount1Delta(sqrtPriceNextX96, sqrtPriceCurrentX96, liquidity, false)
@>      : SqrtPriceMath.getAmount0Delta(sqrtPriceCurrentX96, sqrtPriceNextX96, liquidity, false);
} else {
```

**Impact:** While this could result in incorrect computation of the effective price, the impact is thought to be limited.


**Recommended Mitigation:** Consider the swap context when determining the rounding direction.

**Sorella Labs:** Acknowledged. This is different than Uniswap's logic. There you want to round in the pool's favor to prevent abuse on small amounts. Here you'd be slightly favoring ticks that are closer/further from the current price which seems subjective.

**Cyfrin:** Acknowledged.
