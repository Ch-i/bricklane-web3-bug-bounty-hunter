---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-01-cyfrin-sorella-l2-angstrom-v2-1-2-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-10-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-01-cyfrin-sorella-l2-angstrom-v2-1
title: '`CompensationPriceFinder::getZeroForOne` may compute smaller effective prices
  than expected'
vuln_class: []
---

# `CompensationPriceFinder::getZeroForOne` may compute smaller effective prices than expected

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md)_

---

**Description:** `CompensationPriceFinder::getOneForZero` contains a conditional branch that exists to skip execution that would result in reverts either due to underflow or division by zero:

```solidity
@>  if (sumAmount0Deltas > taxInEther) {
@>      uint256 simplePstarX96 = sumAmount1Deltas.divX96(sumAmount0Deltas - taxInEther);
        if (simplePstarX96 <= uint256(priceUpperSqrtX96).mulX96(priceUpperSqrtX96)) {
            pstarSqrtX96 = _oneForZeroGetFinalCompensationPrice(...);

            return (lastTick, pstarSqrtX96);
        }
    }
```

This logic is also present in `CompensationPriceFinder::getZeroForOne`; however, in this case, neither underflow nor division by zero is possible:

```solidity
@>  if (sumAmount0Deltas > taxInEther) {
        if (
@>          sumAmount1Deltas.divX96(sumAmount0Deltas + taxInEther)
                >= uint256(priceLowerSqrtX96).mulX96(priceLowerSqrtX96)
        ) {
            pstarSqrtX96 = _zeroForOneGetFinalCompensationPrice(...);

            return (lastTick, pstarSqrtX96);
        }
    }
```

This could result in the effective price calculation being skipped even when it would have been validated to lie within the current tick range, since the threshold ratio could be satisfied even when `sumAmount0Deltas <= taxInEther`.

Furthermore, after all the ticks have been iterated, there is a subsequent asymmetry when checking the effective price condition:

```solidity
if (simplePstarX96 > uint256(priceLowerSqrtX96).mulX96(priceLowerSqrtX96)) {
```

Here, if the effective price is exactly equal to the end tick then execution will fall through to returning a 512-bit square root price based on `simplePstarX96` instead of executing `_oneForZeroGetFinalCompensationPrice()`.

**Impact:** This may result in computation of a smaller effective price than expected, compensating liquidity providers who otherwise shouldn't be compensated.

**Recommended Mitigation:**
```diff
    function getZeroForOne(
        TickIteratorDown memory ticks,
        uint128 liquidity,
        uint256 taxInEther,
        uint160 priceUpperSqrtX96,
        Slot0 slot0AfterSwap
    ) internal view returns (int24 lastTick, uint160 pstarSqrtX96) {
        uint256 sumAmount0Deltas = 0; // X
        uint256 sumAmount1Deltas = 0; // Y

        uint160 priceLowerSqrtX96;
        while (ticks.hasNext()) {
            lastTick = ticks.getNext();
            priceLowerSqrtX96 = TickMath.getSqrtPriceAtTick(lastTick);

            {
                uint256 delta0 = SqrtPriceMath.getAmount0Delta(
                    priceLowerSqrtX96, priceUpperSqrtX96, liquidity, false
                );
                uint256 delta1 = SqrtPriceMath.getAmount1Delta(
                    priceLowerSqrtX96, priceUpperSqrtX96, liquidity, false
                );
                sumAmount0Deltas += delta0;
                sumAmount1Deltas += delta1;

--              if (sumAmount0Deltas > taxInEther) {
                    if (
                        sumAmount1Deltas.divX96(sumAmount0Deltas + taxInEther)
                            >= uint256(priceLowerSqrtX96).mulX96(priceLowerSqrtX96)
                    ) {
                        pstarSqrtX96 = _zeroForOneGetFinalCompensationPrice(
                            priceUpperSqrtX96,
                            taxInEther,
                            liquidity,
                            sumAmount0Deltas - delta0,
                            sumAmount1Deltas - delta1
                        );
                        return (lastTick, pstarSqrtX96);
                    }
--              }
            }

            (, int128 liquidityNet) = ticks.manager.getTickLiquidity(ticks.poolId, lastTick);
            require(int128(liquidity) >= liquidityNet, "getZeroForOne: liquidity < liquidityNet");
            liquidity = liquidity.sub(liquidityNet);

            priceUpperSqrtX96 = priceLowerSqrtX96;
        }

        priceLowerSqrtX96 = slot0AfterSwap.sqrtPriceX96();

        uint256 delta0 =
            SqrtPriceMath.getAmount0Delta(priceLowerSqrtX96, priceUpperSqrtX96, liquidity, false);
        uint256 delta1 =
            SqrtPriceMath.getAmount1Delta(priceLowerSqrtX96, priceUpperSqrtX96, liquidity, false);
        sumAmount0Deltas += delta0;
        sumAmount1Deltas += delta1;

        uint256 simplePstarX96 = sumAmount1Deltas.divX96(sumAmount0Deltas + taxInEther);
--      if (simplePstarX96 > uint256(priceLowerSqrtX96).mulX96(priceLowerSqrtX96)) {
++      if (simplePstarX96 >= uint256(priceLowerSqrtX96).mulX96(priceLowerSqrtX96)) {
            pstarSqrtX96 = _zeroForOneGetFinalCompensationPrice(
                priceUpperSqrtX96,
                taxInEther,
                liquidity,
                sumAmount0Deltas - delta0,
                sumAmount1Deltas - delta1
            );

            return (type(int24).min, pstarSqrtX96);
        }
        (uint256 p1, uint256 p0) = Math512Lib.checkedMul2Pow96(0, simplePstarX96);

        return (type(int24).min, Math512Lib.sqrt512(p1, p0).toUint160());
    }
```

**Sorella Labs:** Fixed in commit [f09acd4](https://github.com/SorellaLabs/l2-angstrom/commit/f09acd43ceb05bfc06ba5e8d674d333554adb982). The `if (sumAmount0Deltas > taxInEther) {` in the zero-for-one case can actually lead to computing wrong compensation prices, it's only triggered for very large tick spacings though (>6,900 I think) so arguably still low.

**Cyfrin:** Verified. The outer conditional branch has been removed.
