---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-parallel3-1-v2-0-4-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-03-04T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-04-cyfrin-parallel3-1-v2-0
title: Implement fail-fast mechanism in `_quoteBurnExact` functions for collateral
  availability check
vuln_class: []
---

# Implement fail-fast mechanism in `_quoteBurnExact` functions for collateral availability check

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-parallel3.1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md)_

---

**Description:** In the `Swapper` contract, the `_quoteBurnExactInput` and `_quoteBurnExactOutput` functions compute the expected output or input amounts for burning `USDP` (the stablecoin tokenP) in exchange for collateral without first verifying if the computed collateral amount is actually available for withdrawal.

This can lead to unnecessary gas consumption when the swap would ultimately revert due to insufficient available collateral (e.g., in managed collaterals where LibManager.maxAvailable is less than the required amount).

By moving the `_checkAmounts` call into the quote functions as a fail-fast mechanism, we can revert early if the collateral is unavailable, saving gas on invalid transactions. This is particularly beneficial for managed collaterals, where availability might be limited by external strategies.

**Recommended Mitigation:**
1. In `Swapper::_quoteBurnExactOutput`
```diff
function _quoteBurnExactOutput(address tokenOut, Collateral storage collatInfo, uint256 amountOut) internal view returns (uint256 amountIn) {
    // Add fail-fast check at the start
+   _checkAmounts(tokenOut, collatInfo, amountOut);
    ...
}
```

2. In `Swapper::_quoteBurnExactInput`
```diff
function _quoteBurnExactInput(address tokenOut, Collateral storage collatInfo, uint256 amountIn) internal view returns (uint256 amountOut) {
    ...
    // Add fail-fast check at the end
+   _checkAmounts(tokenOut, collatInfo, amountOut);
}
```

3. Functions like `quoteIn` and `quoteOut` can remove the call to `_checkAmounts`, given that such a call would have already been performed inside the `_quoteBurnExact` functions.

**Parallel:** Acknowledged

\clearpage
