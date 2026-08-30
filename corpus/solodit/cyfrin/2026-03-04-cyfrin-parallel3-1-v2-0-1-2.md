---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-parallel3-1-v2-0-1-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-03-04T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-04-cyfrin-parallel3-1-v2-0
title: Insufficient validation of collateral consumption in external swap during Harvesting
  in `GenericHarvester`
vuln_class: []
---

# Insufficient validation of collateral consumption in external swap during Harvesting in `GenericHarvester`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-parallel3.1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md)_

---

**Description:** In the flashloan callback logic (`GenericHarvester::onFlashLoan`), the contract performs a three-step swap sequence to rebalance yield exposure:

1. Swaps flashloaned USDP → collateral asset (`tokenIn`) via Parallelizer (`swapExactInput`)
2. Swaps received `tokenIn` → `tokenOut` via external router / vault (`_swapToTokenOut`)
3. Swaps resulting `tokenOut` → USDP via Parallelizer to repay flashloan

There is **no validation** that **all** of the received `tokenIn` (from step 1) is actually consumed during the external swap in step 2.
```solidity
// Swaps flashloaned USDP → collateral (tokenIn)
uint256 amountOut =
  parallelizer.swapExactInput(amount, 0, address(tokenP), tokenIn, address(this), block.timestamp);

// Swaps received collateral → tokenOut (external swap / vault)
amountOut = _swapToTokenOut(typeAction, tokenIn, tokenOut, amountOut, swapType, callData);

@> // ← NO CHECK HERE whether all `tokenIn` was actually spent!

// Swaps tokenOut → USDP to repay flashloan
_adjustAllowance(tokenOut, address(parallelizer), amountOut);
uint256 amountStableOut =
  parallelizer.swapExactInput(amountOut, minAmountOut, tokenOut, address(tokenP), address(this), block.timestamp);

if (amount > amountStableOut) {
  budget[sender] -= amount - amountStableOut;   // Deducts shortfall from sender
}
```

This creates the following problems:
- In exact-output swaps on external routers, only a portion of `tokenIn` may be used → leftovers are not handled
- If the external swap consumes less than expected, the final USDP repayment may be insufficient → sender's budget is over-deducted unnecessarily
- Repeated operations can lead to gradual accumulation of unaccounted collateral assets


**Proof of Concept:**
1. Flashloan 1000 USDP
2. Step 1: 1000 USDP → 500 tokenIn (via Parallelizer)
3. Step 2: External swap tries to use 500 tokenIn, but due to:
  - exact-output mode
  - high slippage
  - aggregator behavior only consumes 400 tokenIn → 100 tokenIn left in contract
4. Step 3: Only output from 400 tokenIn is swapped back → repays e.g. 960 USDP
5. Contract deducts 40 USDP from sender's budget (even though 100 tokenIn is still held)

**Recommended Mitigation:** Add balance checks before and after the external swap to verify that `tokenIn` is fully consumed.

**Parallel:** Acknowledged. Harvester contracts will be refactored.
