---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-12-cyfrin-bebop-router-v2-0-2-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-06-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-12-cyfrin-bebop-router-v2-0
title: '`BebopRouter::swap` native-input/native-output orders with excess msg.value
  revert because the excess is paid to the receiver before refund'
vuln_class: []
---

# `BebopRouter::swap` native-input/native-output orders with excess msg.value revert because the excess is paid to the receiver before refund

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-12-cyfrin-bebop-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md)_

---

**Description:**

In `swap`, native-token input requires only `msg.value >= ctx.calc.newFromAmount`, so callers are allowed to send more ETH than the swap needs:

```solidity
// contracts/BebopRouter.sol:155-156
if (order.fromToken == NATIVE_TOKEN) {
    require(msg.value >= ctx.calc.newFromAmount, UnexpectedMsgValue());
}
```

The excess ETH (`msg.value - ctx.calc.newFromAmount`) is supposed to be refunded only after `_executeSwapCore` returns:

```solidity
// contracts/BebopRouter.sol:167-169
if (msg.value > ctx.calc.newFromAmount && order.fromToken == NATIVE_TOKEN) {
    _transferNative(msg.sender, msg.value - ctx.calc.newFromAmount);
}
```

However, `_executeSwapCore` wraps only `ctx.calc.newFromAmount` into WETH for the PMM, leaving the excess as raw ETH in the router. If the same order also has `order.toToken == NATIVE_TOKEN`, the native-output branch computes the receiver payout from the router's full ETH balance:

```solidity
// contracts/BebopRouter.sol:271-274
pmmFromAmount = ctx.calc.newFromAmount;
wrappedNativeToken.deposit{value: pmmFromAmount}();

// contracts/BebopRouter.sol:296-303
uint256 wethBalance = IERC20(address(wrappedNativeToken)).balanceOf(address(this));
if (wethBalance > 0) {
    wrappedNativeToken.withdraw(wethBalance);
}
receiverAmount = address(this).balance;
...
_transferNative(order.receiver, receiverAmount);
```

At that point `address(this).balance` includes both the PMM output unwrapped from WETH and the not-yet-refunded excess `msg.value`. The native-output payout transfers the full balance to `order.receiver`. Control then returns to `swap`, which attempts to refund the same excess to `msg.sender`; under normal execution the router has no ETH left, so the refund reverts with `NativeTransferFailed` and the whole swap unwinds.

**Files:**

- `contracts/BebopRouter.sol` - `BebopRouter::swap` (lines 156, 167-169)
- `contracts/BebopRouter.sol` - `BebopRouter::_executeSwapCore` (lines 271-274, 296-303)

**Impact:** Native-input/native-output swaps revert whenever the caller sends `msg.value > ctx.calc.newFromAmount`. The failure is recoverable by resubmitting with exact `msg.value`, and the revert unwinds the attempted receiver payout, so no funds are permanently lost in the normal case. It is still an availability/accounting bug in the native-to-native path: the contract first treats refundable ETH as receiver output, then tries to refund ETH it has already transferred away.

This does not affect native-input swaps whose output is ERC20, because the raw ETH excess remains in the router until the post-core refund. It also does not affect ERC20-input native-output swaps, because those calls require `msg.value == 0`.

**Recommended Mitigation:** Refund excess `msg.value` before calling `_executeSwapCore`, so refundable ETH is not part of `address(this).balance` during the native-output payout. Alternatively, make the native-output branch pay only the ETH produced by the current swap, e.g. by tracking the WETH/ETH delta attributable to the PMM output instead of transferring the router's full ETH balance.

**Bebop:** Fixed in commit [9db95bc](https://github.com/bebop-dex/bebop-rfqa/commit/9db95bc2b423d9317c149e90a70ae51565e26367).

**Cyfrin:**
Verified.
