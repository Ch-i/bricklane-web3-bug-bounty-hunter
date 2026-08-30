---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-12-cyfrin-bebop-router-v2-0-2-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-06-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-12-cyfrin-bebop-router-v2-0
title: '`BebopRouter::_executeSwapCore` uses absolute balances, causing unrelated
  residual funds to be consumed or paid to another order'
vuln_class: []
---

# `BebopRouter::_executeSwapCore` uses absolute balances, causing unrelated residual funds to be consumed or paid to another order

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-12-cyfrin-bebop-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md)_

---

**Description:** `_executeSwapCore` uses the router's absolute token balances at both the PMM input and receiver output boundaries. Consequently, tokens already held by the router can be treated as belonging to a later swap.

When a pre-hook converts `order.fromToken` into a different `order.pmmFromToken`, the router forwards its complete `pmmFromToken` balance to the PMM:

```solidity
// contracts/BebopRouter.sol:275-283
} else if (order.pmmFromToken != order.fromToken) {
    pmmFromAmount = IERC20(order.pmmFromToken).balanceOf(address(this));
}

_executePmmSwap(
    bebopPmmCalldata,
    ctx.pmm.selector,
    order.pmmFromToken,
    pmmFromAmount
);
```

Any `pmmFromToken` already present from an under-consumed fill, hook overproduction, or direct transfer is folded into the current PMM fill instead of being isolated from it.

The same problem occurs at the receiver boundary. For native output, the router unwraps its complete WETH balance and transfers its complete ETH balance:

```solidity
// contracts/BebopRouter.sol:296-303
uint256 wethBalance =
    IERC20(address(wrappedNativeToken)).balanceOf(address(this));

if (wethBalance > 0) {
    wrappedNativeToken.withdraw(wethBalance);
}

receiverAmount = address(this).balance;
_transferNative(order.receiver, receiverAmount);
```

For ERC20 output, the router transfers its complete `toToken` balance:

```solidity
// contracts/BebopRouter.sol:305-308
receiverAmount = IERC20(order.toToken).balanceOf(address(this));

require(
    !ctx.calc.isExactOut ||
        receiverAmount >= ctx.calc.toAmountAfterFeeSlippage,
    LimitAmountViolation()
);
require(
    order.limitAmount <= 0 ||
        receiverAmount >= uint256(order.limitAmount),
    LimitAmountViolation()
);

IERC20(order.toToken).safeTransfer(order.receiver, receiverAmount);
```

No balance is recorded before the current swap or its hooks. Therefore, unrelated `toToken`, WETH, or ETH already held by the router is included in the current receiver's payout.

These are two manifestations of the same accounting defect: the router treats its global balances as the current swap's balance changes.

This issue is distinct from incidental `pmmToToken` being classified as fee or positive slippage inside `_distributeFees`. It concerns:

- Residual `pmmFromToken` consumed as input by a subsequent hook-transformed swap.
- Residual `toToken`, WETH, or ETH surviving until the final receiver payout.

**Files:**

- `contracts/BebopRouter.sol` - `BebopRouter::_executeSwapCore` (lines 275-283, 296-308)

**Impact:** Residual funds can be attributed to an unrelated later order:

- Existing `pmmFromToken` may be consumed by the PMM, with the resulting output distributed according to the later order.
- Existing `toToken`, WETH, or ETH may be paid to the later order's receiver.
- Exact-out receivers can receive more than the intended target because the router checks only that the absolute balance is at least the required amount and then transfers all of it.

The magnitude is bounded by the router's residual balance and, for PMM input, the PMM quote's taker-amount capacity.

Exploitation is constrained because the later route and receiver are authorized by the `routerSigner`. This is therefore a value-isolation and accounting issue rather than permissionless theft.

**Recommended Mitigation:** Account for each swap using balance deltas rather than absolute balances.

Before pre-hooks, snapshot the `pmmFromToken` balance:

```solidity
uint256 pmmFromBalanceBefore =
    IERC20(order.pmmFromToken).balanceOf(address(this));

HookLib.executeHooks(/* ... */);

uint256 pmmFromBalanceAfter =
    IERC20(order.pmmFromToken).balanceOf(address(this));

uint256 pmmFromAmount =
    pmmFromBalanceAfter - pmmFromBalanceBefore;
```

Use that delta as the PMM input. Also require the PMM to consume exactly that amount or refund any remainder to the appropriate payer.

Similarly, snapshot the receiver asset before the swap can produce it and transfer only the current operation's balance increase:

```solidity
uint256 receiverAmount = balanceAfter - balanceBefore;
```

Native ETH and WETH should be accounted for separately so unrelated ETH and WETH balances are neither unwrapped nor transferred.

For exact-out orders, transfer exactly `toAmountAfterFeeSlippage` after verifying that the current swap produced at least that amount. Route genuine surplus through explicit positive-slippage or recovery logic.

**Bebop:** Acknowledged.
