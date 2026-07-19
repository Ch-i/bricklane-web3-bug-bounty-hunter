---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-12-cyfrin-bebop-router-v2-0-2-10
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-06-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-12-cyfrin-bebop-router-v2-0
title: BebopRouter::_distributeFees leaves below-threshold positive slippage in the
  router, causing it to be paid to the receiver
vuln_class: []
---

# BebopRouter::_distributeFees leaves below-threshold positive slippage in the router, causing it to be paid to the receiver

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-12-cyfrin-bebop-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md)_

---

**Description:** When positive slippage is above zero but below `getMinPositiveSlippageToTreasury` and both protocol shares are zero, the router zeroes the `positiveSlippage` variable to avoid a dust treasury transfer:

```solidity
// contracts/BebopRouter.sol:479-486
if (positiveSlippage > 0 && positiveSlippage < order.getMinPositiveSlippageToTreasury()
    && protocolFeeShare == 0 && protocolSlippageShare == 0) {
    positiveSlippage = 0;
}

uint256 toTreasury = protocolFeeShare + protocolSlippageShare + positiveSlippage;
uint256 totalMakerRefund = (feeAmount + slippageAmount) - protocolFeeShare - protocolSlippageShare;
```

The zeroed amount is not added to `totalMakerRefund`, so it remains in the router's `pmmToToken` balance after `_distributeFees`. For the common path where `order.pmmToToken == order.toToken`, `_executeSwapCore` then transfers the router's full remaining `toToken` balance to the receiver:

```solidity
// contracts/BebopRouter.sol:304-308
receiverAmount = IERC20(order.toToken).balanceOf(address(this));
require(!ctx.calc.isExactOut || receiverAmount >= ctx.calc.toAmountAfterFeeSlippage, LimitAmountViolation());
require(order.limitAmount <= 0 || receiverAmount >= uint256(order.limitAmount), LimitAmountViolation());
IERC20(order.toToken).safeTransfer(order.receiver, receiverAmount);
```

As a result, below-threshold positive slippage is paid to the receiver instead of being sent to treasury or included in the maker refund.

**Files:**

- `contracts/BebopRouter.sol` - `BebopRouter::_distributeFees`, `BebopRouter::_executeSwapCore`

**Impact:** On swaps where positive slippage falls below the dust threshold and both protocol shares are zero, the below-threshold surplus is paid to the receiver. The deviation is bounded by `minPositiveSlippageToTreasury` per swap.

**Recommended Mitigation:** When zeroing dust `positiveSlippage`, add it to `totalMakerRefund` before distribution:

```solidity
if (positiveSlippage > 0 && positiveSlippage < order.getMinPositiveSlippageToTreasury()
    && protocolFeeShare == 0 && protocolSlippageShare == 0) {
    // Route dust back to makers instead of zeroing it
    totalMakerRefund += positiveSlippage;
    positiveSlippage = 0;
}
```

This ensures the below-threshold amount is distributed pro-rata to makers via `_distributeMakerRefundAndEmit` instead of remaining for the final receiver payout.

**Bebop:** Acknowledged.
