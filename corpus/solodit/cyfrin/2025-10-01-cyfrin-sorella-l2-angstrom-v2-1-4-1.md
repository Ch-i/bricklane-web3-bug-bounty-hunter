---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-01-cyfrin-sorella-l2-angstrom-v2-1-4-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-10-01T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-01-cyfrin-sorella-l2-angstrom-v2-1
title: Remove unnecessary local variables
vuln_class: []
---

# Remove unnecessary local variables

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md)_

---

**Description:** The following functions in `AngstromL2` assign an unnecessary local variable `priorityFee` that can be removed:

```diff
function _getSwapTaxAmount() internal view returns (uint256) {
-   uint256 priorityFee = tx.gasprice - block.basefee;
-   return getSwapTaxAmount(priorityFee);
+   return getSwapTaxAmount(tx.gasprice - block.basefee);
}

function _getJitTaxAmount() internal view returns (uint256) {
    if (_getBlock() == _blockOfLastTopOfBlock) {
        return 0;
    }
-   uint256 priorityFee = tx.gasprice - block.basefee;
-   return getJitTaxAmount(priorityFee);
+   return getJitTaxAmount(tx.gasprice - block.basefee);
}
```

The `simplePstarX96` variable within `CompensationPriceFinder::getOneForZero` can also be inlined and removed:

```diff
if (sumAmount0Deltas > taxInEther) {
-   uint256 simplePstarX96 = sumAmount1Deltas.divX96(sumAmount0Deltas - taxInEther);
-   if (simplePstarX96 <= uint256(priceUpperSqrtX96).mulX96(priceUpperSqrtX96)) {
+   if (
+       sumAmount1Deltas.divX96(sumAmount0Deltas - taxInEther)
+           <= uint256(priceUpperSqrtX96).mulX96(priceUpperSqrtX96)
+   ) {
        pstarSqrtX96 = _oneForZeroGetFinalCompensationPrice(
            liquidity,
            priceLowerSqrtX96,
            taxInEther,
            sumAmount0Deltas - delta0,
            sumAmount1Deltas - delta1
        );

        return (lastTick, pstarSqrtX96);
    }
}
```

**Sorella Labs:** Acknowledged. Will leave the variables as is because it improves readability and the gas improvement is likely negligible.

**Cyfrin:** Acknowledged.
