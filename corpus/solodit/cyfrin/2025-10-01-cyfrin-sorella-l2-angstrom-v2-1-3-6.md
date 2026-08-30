---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-01-cyfrin-sorella-l2-angstrom-v2-1-3-6
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-10-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-01-cyfrin-sorella-l2-angstrom-v2-1
title: Large priority fee relative to one-for-zero swap amounts will cause `CompensationPriceFinder::getOneForZero`
  to underflow
vuln_class: []
---

# Large priority fee relative to one-for-zero swap amounts will cause `CompensationPriceFinder::getOneForZero` to underflow

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md)_

---

**Description:** Swaps over zero liquidity can push the square root price to any arbitrary tick and are allowed by Uniswap; however, such top-of-block one-for-zero swaps are in certain circumstances not possible in Angstrom due to arithmetic panic revert.

For a sufficiently large priority fee relative to the swap amount such that `taxInEther > sumAmount0Deltas`, `CompensationFinder::getOneForZero` will panic revert due to underflow:

```solidity
uint256 simplePstarX96 = sumAmount1Deltas.divX96(sumAmount0Deltas - taxInEther);
```

Alternatively, this logic will throw `FullMulDivFailed()` when `sumAmount0Deltas` and `taxInEther` are exactly equal.

While it is understood that this is intended and would not make financial sense for an arbitrageur to swap insufficient ETH out of one-for-zero swaps such that the tax is not covered, LPs will not receive any share of the priority fee.

**Proof of Concept:** The following test should be added to `AngstromL2.t.sol`

```solidity
// If priority fee is high enough, one-for-zero swap underflows
function test_cyfrin_EnormousPriorityFeeCausesUnderflowInCompensationPriceFinderGetOneForZero() public {
    PoolKey memory key = initializePool(address(token), 10, 3);

    setupSimpleZeroForOnePositions(key);

    uint256 PRIORITY_FEE = 1750 gwei;
    setPriorityFee(PRIORITY_FEE);

    vm.expectRevert();
    router.swap(key, false, 1e18, int24(35).getSqrtPriceAtTick());
}

// If there is no liquidity, one-for-zero swap reverts
function test_cyfrin_zeroLiquiditySwap() public {
    setPriorityFee(10 gwei);
    PoolKey memory key = initializePool(address(token), 10, 3);

    uint160 sqrtPriceLimit = int24(15).getSqrtPriceAtTick();

    router.swap(key, false, 100e18, sqrtPriceLimit);
}
```

**Recommended Mitigation:** Consider throwing an informative error:

```solidity
error OutputLessThanMevTax();

if (!(sumAmount0Deltas >= taxInEther)) {
     revert OutputLessThanMevTax()
}
```

**Sorella Labs:** Acknowledged. Not worth the complexity, will leave as is.

**Cyfrin:** Acknowledged.
