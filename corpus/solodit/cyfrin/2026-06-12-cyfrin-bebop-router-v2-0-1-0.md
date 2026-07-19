---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-12-cyfrin-bebop-router-v2-0-1-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-06-12T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-12-cyfrin-bebop-router-v2-0
title: '`BebopRouter::_distributeMakerRefundAndEmit` scales legs by fromToken-denominated
  `newFromAmount` instead of the actual PMM fill, causing incorrect maker accounting
  and conditional swap reverts'
vuln_class: []
---

# `BebopRouter::_distributeMakerRefundAndEmit` scales legs by fromToken-denominated `newFromAmount` instead of the actual PMM fill, causing incorrect maker accounting and conditional swap reverts

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-12-cyfrin-bebop-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md)_

---

**Description:** When a swap uses a pre-hook to convert `order.fromToken` into a different `order.pmmFromToken`, `_executeSwapCore` takes the converted token balance as the PMM fill amount:

```solidity
// contracts/BebopRouter.sol:275-277
} else if (order.pmmFromToken != order.fromToken) {
    pmmFromAmount = IERC20(order.pmmFromToken).balanceOf(address(this));
}
```

That `pmmFromAmount` is then injected into the PMM calldata as `filledTakerAmount` and is the value `BebopSettlement` uses to scale the maker/taker legs actually executed by the PMM.

Inside `_distributeMakerRefundAndEmit` at `contracts/BebopRouter.sol:531-532`, the per-leg scaling uses a different value:

```solidity
uint256 scaledTakerAmt = (legs[j].takerAmount * calc.newFromAmount) / pmm.pmmTakerAmount;
uint256 scaledMakerAmt = (legs[j].makerAmount * calc.newFromAmount) / pmm.pmmTakerAmount;
```

Here `calc.newFromAmount` is denominated in the router order's `fromToken`, while `pmm.pmmTakerAmount` is denominated in `pmmFromToken`. For 1:1 same-decimal wrappers this may accidentally match, but non-1:1 wrappers or decimal-changing conversions make the ratio wrong. The event therefore reports maker/taker leg amounts using `fromToken` units even though the PMM filled using `pmmFromToken` units.

For example, the existing rate-wrapper scenario converts `600 rvUSDC` into `750 USDC` before the PMM call. The PMM fills against `750 USDC`, so a `1000 USDC -> 0.4 WETH` PMM quote delivers `0.3 WETH`. However, `_distributeMakerRefundAndEmit` scales the leg by `600 / 1000` instead of `750 / 1000`, so after a `0.003 WETH` maker refund the event reports `0.237 WETH` maker delivery even though the maker's real WETH balance change is `0.297 WETH`.

The same mismatch can also revert the whole swap. If `calc.newFromAmount` is sufficiently smaller than the actual PMM fill amount, `scaledMakerAmt` can be computed below the fee/slippage-derived `legRefund`. The checked subtraction at `contracts/BebopRouter.sol:545` then underflows:

```solidity
scaledMakerAmt - legRefund
```

This does not affect every pre-hook conversion. Near-1:1 conversions or low-refund cases can succeed but emit incorrect PMM swap accounting. The revert occurs once the conversion ratio and fee/refund parameters make the incorrectly-scaled `scaledMakerAmt` smaller than `legRefund`.

**Files:**

`contracts/BebopRouter.sol::_distributeMakerRefundAndEmit, _executeSwapCore`

**Impact:** Pre-hook conversion swaps with non-1:1 or cross-decimal conversions can produce incorrect `BebopPmmSwap` maker/taker amounts, causing off-chain accounting and monitoring systems to observe balances that do not match the actual PMM transfer amounts.

For sufficiently lopsided conversions, the same mismatch can make `_distributeMakerRefundAndEmit` revert during `scaledMakerAmt - legRefund`, making otherwise valid swaps unfillable. The revert unwinds the full transaction, so pre-hooks and the PMM fill do not remain partially executed, but the affected order path is unavailable until the conversion ratio, fee/refund parameters, or implementation are changed.

**Recommended Mitigation:** Scale per-leg amounts using the actual PMM fill amount, not `calc.newFromAmount`. If the router also enforces that the PMM consumes exactly the amount supplied, this can be the `pmmFromAmount` injected into the PMM calldata:

```solidity
uint256 scaledTakerAmt = (legs[j].takerAmount * pmmFromAmount) / pmm.pmmTakerAmount;
uint256 scaledMakerAmt = (legs[j].makerAmount * pmmFromAmount) / pmm.pmmTakerAmount;
```

If `pmmFromAmount` may exceed `pmm.pmmTakerAmount` and `BebopSettlement` caps the consumed amount, use the actual consumed PMM amount instead, e.g. `min(pmmFromAmount, pmm.pmmTakerAmount)`, or enforce `pmmFromAmount <= pmm.pmmTakerAmount` before calling the PMM.

To make the value available at event emission, pass it through `_distributeFees` into `_distributeMakerRefundAndEmit` or store it in the swap context. The same actual-fill value should also be used anywhere hook-facing scaled swaps are meant to describe the PMM legs that actually executed.

**Bebop:** Fixed in commit [9db95bc](https://github.com/bebop-dex/bebop-rfqa/commit/9db95bc2b423d9317c149e90a70ae51565e26367).

**Cyfrin:**
Verified.
