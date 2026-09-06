---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-12-cyfrin-bebop-router-v2-0-2-14
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-06-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-12-cyfrin-bebop-router-v2-0
title: '`BebopRouter::_distributeFees` subtracts cross-denomination operands when
  a post-hook makes pmmToToken differ from toToken'
vuln_class: []
---

# `BebopRouter::_distributeFees` subtracts cross-denomination operands when a post-hook makes pmmToToken differ from toToken

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-12-cyfrin-bebop-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md)_

---

**Description:** `_distributeFees` runs before post-hooks and computes the fee pool from the router's `pmmToToken` balance:

```solidity
// contracts/BebopRouter.sol:450-455
uint256 pmmToBalance = IERC20(order.pmmToToken).balanceOf(address(this));

uint256 feePool = pmmToBalance > calc.toAmountAfterFeeSlippage
    ? pmmToBalance - calc.toAmountAfterFeeSlippage
    : 0;
```

`pmmToBalance` is denominated in `order.pmmToToken`, the token delivered by the PMM. However, `calc.toAmountAfterFeeSlippage` is derived from `order.toAmount`, which represents the final receiver token:

```solidity
// contracts/BebopRouter.sol:403-408
calc.newFromAmount = uint256(exactAmount);
calc.newToAmount = (order.toAmount * calc.newFromAmount) / order.fromAmount;
calc.feeAmount = (calc.newToAmount * fee) / UNIT_BASE;
calc.slippageAmount = (calc.newToAmount * slippage) / UNIT_BASE;
calc.toAmountAfterFeeSlippage = calc.newToAmount - calc.feeAmount - calc.slippageAmount;
```

When `order.pmmToToken == order.toToken`, both operands share the same units. When a post-hook converts `pmmToToken` into a different `toToken`, the operands can represent different tokens, decimals, or conversion rates. In that case, `_distributeFees` may understate or overstate `feePool` before the post-hook has converted the remaining `pmmToToken` into the receiver asset.

**Files:**

- `contracts/BebopRouter.sol` - `BebopRouter::_calculateAmounts`, `BebopRouter::_distributeFees`, `BebopRouter::_executeSwapCore`

**Impact:** When a post-hook conversion changes the denomination between `pmmToToken` and `toToken`, fee/slippage distribution can be computed from incompatible units:

- If `calc.toAmountAfterFeeSlippage` is inflated relative to the `pmmToToken` balance, `feePool` collapses to zero and no fee/slippage refund is distributed.
- If `calc.toAmountAfterFeeSlippage` is understated relative to the `pmmToToken` balance, `feePool` is inflated and value can be misclassified as fee, slippage refund, or positive slippage.

The affected path requires a post-hook that changes the output token denomination.

**Recommended Mitigation:** Ensure the receiver floor used by `_distributeFees` is denominated in `pmmToToken`, not final `toToken`, whenever fee/slippage is distributed before a post-hook conversion.

**Bebop:** Fixed in commit [9db95bc](https://github.com/bebop-dex/bebop-rfqa/commit/9db95bc2b423d9317c149e90a70ae51565e26367).

**Cyfrin:**
Verified.
