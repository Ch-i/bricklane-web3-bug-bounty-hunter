---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-19-cyfrin-bunni-fee-override-hooklet-v2-0-1-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-07-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-19-cyfrin-bunni-fee-override-hooklet-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-19-cyfrin-bunni-fee-override-hooklet-v2-0
title: Insufficient clamping in `HookletLib::hookletBeforeSwap` can result in unexpected
  reverts
vuln_class: []
---

# Insufficient clamping in `HookletLib::hookletBeforeSwap` can result in unexpected reverts

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-19-cyfrin-bunni-fee-override-hooklet-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-19-cyfrin-bunni-fee-override-hooklet-v2.0.md)_

---

**Description:** `HookletLib::hookletBeforeSwap` and `HookletLib::hookletBeforeSwapView` decode the fee and price override data returned from external hooklet calls, applying a clamping operation on these values to ensure that they lie within specified bounds:

```solidity
// clamp the override values to the valid range
fee = feeOverridden ? uint24(fee.clamp(0, SWAP_FEE_BASE)) : 0;
sqrtPriceX96 =
    priceOverridden ? uint160(sqrtPriceX96.clamp(TickMath.MIN_SQRT_PRICE, TickMath.MAX_SQRT_PRICE)) : 0;
```

However, the following edge cases have not been accounted for:
* Use of `SWAP_FEE_BASE` as the inclusive upper bound contradicts validation elsewhere throughout the codebase, for example in `BunniHookLogic::isValidParams` and `FeeOverrideHooklet::setFeeOverride` where a fee equal to `SWAP_FEE_BASE` is explicitly prevented. Allowing this value may cause a division-by-zero error in downstream logic such as `BunniHookLogic::beforeSwap` which relies on `SWAP_FEE_BASE - fee` to be non-zero.
* Bounding the overridden `sqrtPriceX96` to the range `[TickMath.MIN_SQRT_PRICE, TickMath.MAX_SQRT_PRICE]` fails to consider the sqrt price corresponding to the range of usable ricks $r_{\min} = \left\lfloor \frac{t_{\min}}{w} \right\rfloor\cdot w$ and $r_{\max} = \bigl(\lfloor \tfrac{t_{\max}}{w} \rfloor - 1\bigr) \cdot w$ as defined in the whitepaper. Allowing prices outside of this range may cause reverts due to the use of invalid ticks when `getSqrtPriceAtTick()` is called.

**Impact:** If the fee override value equals `SWAP_FEE_BASE`, this may result in a revert due to division-by-zero during further swap execution in `BunniHookLogic::beforeSwap`. If the sqrt price is such that the corresponding tick lies outside the range of usable ricks then execution will similarly revert within this invocation.

**Proof of Concept:** Apply the following patch:

```diff
---
 test/BunniHook.t.sol | 110 +++++++++++++++++--------------------------
 1 file changed, 41 insertions(+), 65 deletions(-)

diff --git a/test/BunniHook.t.sol b/test/BunniHook.t.sol
index 0a7978bd..25f3eb08 100644
--- a/test/BunniHook.t.sol
+++ b/test/BunniHook.t.sol
@@ -8,6 +8,9 @@ import {IAmAmm} from "biddog/interfaces/IAmAmm.sol";
 import "./BaseTest.sol";
 import {BunniStateLibrary} from "../src/lib/BunniStateLibrary.sol";

+import {SWAP_FEE_BASE} from "src/base/Constants.sol";
+import {CustomRevert} from "@uniswap/v4-core/src/libraries/CustomRevert.sol";
+
 contract BunniHookTest is BaseTest {
     using TickMath for *;
     using FullMathX96 for *;
@@ -1388,12 +1391,6 @@ contract BunniHookTest is BaseTest {
         ldf_.setMinTick(-30);

         // deploy pool with hooklet
-        // this should trigger:
-        // - before/afterInitialize
-        // - before/afterDeposit
-        uint24 feeMin = 0.3e6;
-        uint24 feeMax = 0.5e6;
-        uint24 feeQuadraticMultiplier = 1e6;
         (Currency currency0, Currency currency1) = (Currency.wrap(address(token0)), Currency.wrap(address(token1)));
         (IBunniToken bunniToken, PoolKey memory key) = _deployPoolAndInitLiquidity(
             currency0,
@@ -1401,11 +1398,12 @@ contract BunniHookTest is BaseTest {
             ERC4626(address(0)),
             ERC4626(address(0)),
             ldf_,
+            IHooklet(hooklet),
             ldfParams,
             abi.encodePacked(
-                feeMin,
-                feeMax,
-                feeQuadraticMultiplier,
+                uint24(0.3e6),
+                uint24(0.5e6),
+                uint24(1e6),
                 FEE_TWAP_SECONDS_AGO,
                 POOL_MAX_AMAMM_FEE,
                 SURGE_HALFLIFE,
@@ -1419,68 +1417,46 @@ contract BunniHookTest is BaseTest {
                 true, // amAmmEnabled
                 ORACLE_MIN_INTERVAL,
                 MIN_RENT_MULTIPLIER
-            )
+            ),
+            bytes32("")
         );
-        address depositor = address(0x6969);
-
-        // transfer bunniToken
-        // this should trigger:
-        // - before/afterTransfer
-        address recipient = address(0x8008);
-        vm.startPrank(depositor);
-        bunniToken.transfer(recipient, bunniToken.balanceOf(depositor));
-        vm.stopPrank();
-        vm.startPrank(recipient);
-        bunniToken.transfer(depositor, bunniToken.balanceOf(recipient));
-        vm.stopPrank();

-        // withdraw liquidity
-        // this should trigger:
-        // - before/afterWithdraw
-        vm.startPrank(depositor);
-        hub.withdraw(
-            IBunniHub.WithdrawParams({
-                poolKey: key,
-                recipient: depositor,
-                shares: bunniToken.balanceOf(depositor),
-                amount0Min: 0,
-                amount1Min: 0,
-                deadline: block.timestamp,
-                useQueuedWithdrawal: false
-            })
-        );
-        vm.stopPrank();
-
-        // shift LDF to trigger rebalance during the next swap
-        ldf_.setMinTick(-20);
-
-        // make swap
-        // this should trigger:
-        // - before/afterSwap
+        // make swap to trigger beforeSwap
         _mint(currency0, address(this), 1e6);
         IPoolManager.SwapParams memory params = IPoolManager.SwapParams({
-            zeroForOne: true,
-            amountSpecified: -int256(1e6),
-            sqrtPriceLimitX96: TickMath.MIN_SQRT_PRICE + 1
+            zeroForOne: false,
+            amountSpecified: int256(1e6),
+            sqrtPriceLimitX96: TickMath.MAX_SQRT_PRICE - 1
         });
-        vm.recordLogs();
-        _swap(key, params, 0, "");

-        // fill rebalance order
-        // this should trigger:
-        // - afterRebalance
-        Vm.Log[] memory logs = vm.getRecordedLogs();
-        Vm.Log memory orderEtchedLog;
-        for (uint256 i = 0; i < logs.length; i++) {
-            if (logs[i].emitter == address(floodPlain) && logs[i].topics[0] == IOnChainOrders.OrderEtched.selector) {
-                orderEtchedLog = logs[i];
-                break;
-            }
-        }
-        IFloodPlain.SignedOrder memory signedOrder = abi.decode(orderEtchedLog.data, (IFloodPlain.SignedOrder));
-        IFloodPlain.Order memory order = signedOrder.order;
-        _mint(key.currency0, address(this), order.consideration.amount);
-        floodPlain.fulfillOrder(signedOrder);
+        hooklet.setBeforeSwapOverride(true, uint24(SWAP_FEE_BASE), false, uint24(0));
+        vm.expectRevert(
+            abi.encodeWithSelector(
+                CustomRevert.WrappedError.selector,
+                key.hooks,
+                BunniHook.beforeSwap.selector,
+                abi.encodePacked(bytes4(keccak256("MulDivFailed()"))),
+                abi.encodePacked(bytes4(keccak256("HookCallFailed()")))
+            )
+        );
+        _swap(key, params, 0, "");
+
+        int24 tickAtPrice = TickMath.MIN_TICK;
+        uint160 priceOverride = TickMath.getSqrtPriceAtTick(tickAtPrice);
+        hooklet.setBeforeSwapOverride(false, uint24(0), true, priceOverride);
+        vm.expectRevert(
+            abi.encodeWithSelector(
+                CustomRevert.WrappedError.selector,
+                key.hooks,
+                BunniHook.beforeSwap.selector,
+                abi.encodeWithSelector(
+                    TickMath.InvalidTick.selector,
+                    tickAtPrice - ((tickAtPrice % key.tickSpacing + key.tickSpacing) % key.tickSpacing)
+                ),
+                abi.encodePacked(bytes4(keccak256("HookCallFailed()")))
+            )
+        );
+        _swap(key, params, 0, "");
     }
--
2.40.0

```

**Recommended Mitigation:** Update the clamping logic in both `HookletLib::hookletBeforeSwap` and `HookletLib::hookletBeforeSwapView` to subtract one from `SWAP_FEE_BASE` to prevent allowing this as a valid upper bound and align the behavior with other instances where similar validation is already performed:

```diff
- fee = feeOverridden ? uint24(fee.clamp(0, SWAP_FEE_BASE)) : 0;
+ fee = feeOverridden ? uint24(fee.clamp(0, SWAP_FEE_BASE - 1)) : 0;
```

Additionally prevent the overridden price from being specified as corresponding to a tick that is outside the range of usable ricks:

```diff
- sqrtPriceX96 =
-   priceOverridden ? uint160(sqrtPriceX96.clamp(TickMath.MIN_SQRT_PRICE, TickMath.MAX_SQRT_PRICE)) : 0;
+ sqrtPriceX96 =
+   priceOverridden ? uint160(sqrtPriceX96.clamp(TickMath.getSqrtPriceAtTick((TickMath.MIN_TICK / key.tickSpacing) * key.tickSpacing), TickMath.getSqrtPriceAtTick(((TickMath.MAX_TICK / key.tickSpacing) - 1) * key.tickSpacing))) : 0;
```

**Bacon Labs:** Fixed in commits [45643ef](https://github.com/Bunniapp/bunni-v2/pull/135/commits/45643eff21be8d3671bea025aae5ffd11a0f6467) and [0b5a708](https://github.com/Bunniapp/bunni-v2/pull/135/commits/0b5a708e5bafb12308dbab1c8db478ac991bae2f).

**Cyfrin:** Verified. The fee clamping logic has been modified to prevent `SWAP_FEE_BASE` from being used. The price clamping logic has also been modified to bound the override between the sqrt prices corresponding to the minimum and maximum usable ticks.

\clearpage
