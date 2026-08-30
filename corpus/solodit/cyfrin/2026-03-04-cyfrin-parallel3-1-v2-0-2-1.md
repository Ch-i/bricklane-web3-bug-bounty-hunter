---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-parallel3-1-v2-0-2-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-03-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-04-cyfrin-parallel3-1-v2-0
title: RewardHandler can be used to call OdosRouterV2 methods other than `swap`
vuln_class: []
---

# RewardHandler can be used to call OdosRouterV2 methods other than `swap`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-parallel3.1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md)_

---

**Description:** `RewardsHandler::sellRewards` takes a `bytes memory payload` as its second argument which allows governance and trusted sellers to call any method of `OdosRouterV2` ([0xCf5540fFFCdC3d510B18bFcA6d2b9987b0772559](https://etherscan.io/address/0xCf5540fFFCdC3d510B18bFcA6d2b9987b0772559)).

The `amountOut` is decoded on L50

```solidity
amountOut = abi.decode(result, (uint256));
```

However, some of the methods don't return a `uint256`.  Notably, `OdosRouterV2::swapMulti` returns a `uint256[]`.
This will happily be decoded by `abi.decode` incorrectly, mostly likely to an array offset of `0x20 == 32`.

In the case of `collatInfo.isManaged > 0` this will cause 32 wei of the collateral to be sent to the managed fund with the rest being trapped in the `RewardHandler` contract.

**Impact:** The collateral will be trapped in the `RewardHandler` contract. Since it is unlikely other methods besides `swap` will be called this is assessed as a Low severity finding.

**Proof of Concept:**
- tests/units/parallel-protocolRewardHandlerManaged.t.sol
```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.28;

import { IERC20 } from "@openzeppelin/contracts/interfaces/IERC20.sol";

import { MockTokenPermit } from "tests/mock/MockTokenPermit.sol";
import { MockManager } from "tests/mock/MockManager.sol";
import { CyfrinMockOdosRouter } from "tests/mock/parallel-protocolMockOdosRouter.sol";

import "contracts/parallelizer/Storage.sol";
import "contracts/utils/Constants.sol";

import "../Fixture.sol";

contract CyfrinRewardHandlerManagedTest is Fixture {
  IERC20 internal tokenA;
  CyfrinMockOdosRouter internal odosMock;
  MockManager internal managerEurA;
  MockManager internal managerEurB;

  function setUp() public override {
    super.setUp();
    tokenA = IERC20(address(new MockTokenPermit("tokenA", "tokenA", 18)));
    odosMock = new CyfrinMockOdosRouter();
    vm.etch(ODOS_ROUTER, address(odosMock).code);

    managerEurA = new MockManager(address(eurA));
    IERC20[] memory subCollaterals = new IERC20[](1);
    subCollaterals[0] = eurA;
    managerEurA.setSubCollaterals(subCollaterals, "");
    ManagerStorage memory managerData =
      ManagerStorage({ subCollaterals: subCollaterals, config: abi.encode(ManagerType.EXTERNAL, abi.encode(address(managerEurA))) });
    vm.prank(governor);
    parallelizer.setCollateralManager(address(eurA), true, managerData);

    // Manage eurB as well so swapMulti can increase multiple collaterals, and the last increased (eurB) is invested.
    managerEurB = new MockManager(address(eurB));
    IERC20[] memory subCollateralsB = new IERC20[](1);
    subCollateralsB[0] = eurB;
    managerEurB.setSubCollaterals(subCollateralsB, "");
    ManagerStorage memory managerDataB =
      ManagerStorage({ subCollaterals: subCollateralsB, config: abi.encode(ManagerType.EXTERNAL, abi.encode(address(managerEurB))) });
    vm.prank(governor);
    parallelizer.setCollateralManager(address(eurB), true, managerDataB);
  }


  /*
   *  When a token like USDM is used the amount actually transferred by a call to ODOS_ROUTER.swap
   *  can be less than the `amountOut` returned.
   *
   *  This causes a revert in RewardHandler::sellRewards#L68
   */
  function test_cyfrin_SellRewards_RevertWhen_AmountOutOverstatesManagedIncrease() public {
    uint256 amountIn = 100e18;
    uint256 amountOutTransferred = 50e6;
    uint256 amountOutReturned = 100e6;
    bytes memory payload = abi.encodeWithSelector(
      parallel-protocolMockOdosRouter.swapSkewed.selector,
      amountIn,
      amountOutTransferred,
      amountOutReturned,
      address(tokenA),
      address(eurA)
    );

    vm.startPrank(governor);
    deal(address(tokenA), address(parallelizer), amountIn);
    deal(address(eurA), ODOS_ROUTER, amountOutTransferred);
    parallelizer.changeAllowance(tokenA, ODOS_ROUTER, amountIn);
    vm.expectRevert();
    parallelizer.sellRewards(0, payload);
    vm.stopPrank();
  }

  function test_cyfrin_SellRewards_CanStrandManagedCollateralWhen_AmountOutUnderstatesIncrease() public {
    uint256 amountIn = 100e18;
    uint256 amountOutTransferred = 100e6;
    uint256 amountOutReturned = 40e6;
    bytes memory payload = abi.encodeWithSelector(
      parallel-protocolMockOdosRouter.swapSkewed.selector,
      amountIn,
      amountOutTransferred,
      amountOutReturned,
      address(tokenA),
      address(eurA)
    );

    vm.startPrank(governor);
    deal(address(tokenA), address(parallelizer), amountIn);
    deal(address(eurA), ODOS_ROUTER, amountOutTransferred);
    parallelizer.changeAllowance(tokenA, ODOS_ROUTER, amountIn);
    parallelizer.sellRewards(0, payload);
    vm.stopPrank();

    assertEq(eurA.balanceOf(address(parallelizer)), amountOutTransferred - amountOutReturned);
  }

  /*
   *  This test demonstrates that it is possible to call `swapMulti` using `RewardsHandler::sellRewards`
   *
   *  This method returns at uint256[] (not a uint256) but will happily be decoded by abi.decode to
   *  the value 0x20 == 32. (This is the offset value for the array in the return data)
   *
   *  This results in only 32 wei of the token being returned to a managed fund, the rest being
   *  stranded in the RewardHandler contract.
   */
  function test_cyfrin_SellRewards_SwapMulti_ReturnsUintArray_DecodesTo32_StrandsCollateral() public {
    uint256 amountIn = 100e18;

    // We'll increase multiple collaterals (eurA then eurB). RewardHandler will pick the last increased collateral
    // in the collateral list for managed investing logic.
    uint256 eurAOut = 1_000_000; // 1e6 (eurA has 6 decimals)
    uint256 eurBOut = 2_000_000_000_000; // 2e12 (eurB has 12 decimals)

    parallel-protocolMockOdosRouter.inputTokenInfo[] memory inputs = new parallel-protocolMockOdosRouter.inputTokenInfo[](1);
    inputs[0] = parallel-protocolMockOdosRouter.inputTokenInfo({ tokenAddress: address(tokenA), amountIn: amountIn, receiver: ODOS_ROUTER });

    parallel-protocolMockOdosRouter.outputTokenInfo[] memory outputs = new parallel-protocolMockOdosRouter.outputTokenInfo[](2);
    outputs[0] = parallel-protocolMockOdosRouter.outputTokenInfo({ tokenAddress: address(eurA), relativeValue: 0, receiver: address(parallelizer) });
    outputs[1] = parallel-protocolMockOdosRouter.outputTokenInfo({ tokenAddress: address(eurB), relativeValue: 0, receiver: address(parallelizer) });

    // Fund the ODOS router with the output tokens so it can transfer them to the diamond.
    deal(address(eurA), ODOS_ROUTER, eurAOut);
    deal(address(eurB), ODOS_ROUTER, eurBOut);

    bytes memory payload = abi.encodeWithSelector(
      parallel-protocolMockOdosRouter.swapMulti.selector,
      inputs,
      outputs,
      uint256(1),
      bytes(""),
      address(0),
      uint32(0)
    );

    vm.startPrank(governor);
    deal(address(tokenA), address(parallelizer), amountIn);
    parallelizer.changeAllowance(tokenA, ODOS_ROUTER, amountIn);
    parallelizer.sellRewards(0, payload);
    vm.stopPrank();

    // swapMulti returns a `uint256[]` so RewardHandler's `abi.decode(result,(uint256))` reads the first word,
    // which is the offset (0x20), i.e. 32. It will then transfer/invest only 32 units of the chosen managed
    // collateral (eurB), leaving the rest stranded on the diamond.
    assertEq(eurB.balanceOf(address(managerEurB)), 32);
    assertEq(eurB.balanceOf(address(parallelizer)), eurBOut - 32);

    // eurA was also received by the diamond, but because the last increased collateral was eurB, eurA isn't invested.
    assertEq(eurA.balanceOf(address(managerEurA)), 0);
    assertEq(eurA.balanceOf(address(parallelizer)), eurAOut);
  }
}
```

- tests/mock/parallel-protocolMockOdosRouter.sol
```solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity 0.8.28;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

/*
 *  This contract mocks the OdosRouterV2 at address 0xCf5540fFFCdC3d510B18bFcA6d2b9987b0772559
 *  (see contracts/utils/Constants.sol)
 *
 *  - `swapSkewed` is not a method of OdosRouterV2 but closely resembles `swap`.
 *     It has one extra argument to reflect that the `amountOut` returned from
 *     the `swap` method can be different to the amount actually transferred
 *     for tokens like USDM and stETH
 *
 *  - `swapMulti` has the same signature as in OdosRouterV2 and mimicks its behaviour.
 */
contract CyfrinMockOdosRouter {
  using SafeERC20 for IERC20;

  // Match the real OdosRouterV2 swapMulti signature closely so the selector is realistic.
  struct inputTokenInfo {
    address tokenAddress;
    uint256 amountIn;
    address receiver;
  }

  struct outputTokenInfo {
    address tokenAddress;
    uint256 relativeValue;
    address receiver;
  }

  function swapSkewed(
    uint256 amountIn,
    uint256 amountOutTransferred,
    uint256 amountOutReturned,
    address tokenIn,
    address tokenOut
  )
    external
    returns (uint256)
  {
    IERC20(tokenIn).safeTransferFrom(msg.sender, address(this), amountIn);
    IERC20(tokenOut).safeTransfer(msg.sender, amountOutTransferred);
    return amountOutReturned;
  }

  function swapMulti(
    inputTokenInfo[] memory inputs,
    outputTokenInfo[] memory outputs,
    uint256, /* valueOutMin */
    bytes calldata, /* pathDefinition */
    address, /* executor */
    uint32 /* referralCode */
  )
    external
    payable
    returns (uint256[] memory amountsOut)
  {
    // Minimal behavior: pull all provided inputs from caller and send fixed amounts to each output receiver.
    // The important part for the RewardHandler bug is that this returns a `uint256[]`, not a `uint256`.
    for (uint256 i; i < inputs.length; ++i) {
      if (inputs[i].tokenAddress != address(0) && inputs[i].amountIn > 0) {
        IERC20(inputs[i].tokenAddress).safeTransferFrom(msg.sender, address(this), inputs[i].amountIn);
      }
    }

    amountsOut = new uint256[](outputs.length);
    for (uint256 i; i < outputs.length; ++i) {
      // Transfer the full output-token balance held by the router to the designated receiver.
      // RewardHandler will decode this `uint256[]` as a single `uint256` and read the first word (0x20 == 32).
      amountsOut[i] = IERC20(outputs[i].tokenAddress).balanceOf(address(this));
      if (amountsOut[i] > 0) IERC20(outputs[i].tokenAddress).safeTransfer(outputs[i].receiver, amountsOut[i]);
    }
  }
}
```

**Recommended Mitigation:** The modified function below:
- only allows for calls to `OdosRouterV2` that return `uint256`
- finds the amount of tokens received by comparing the delta of balances before and after the swap
- invests this amount in the `collatInfo.isManaged` case
- reverts if somehow more than one collateral token was received from the `OdosRouterV2` call

```diff
  function sellRewards(uint256 minAmountOut, bytes memory payload) external nonReentrant returns (uint256 amountOut) {
    ParallelizerStorage storage ts = s.transmuterStorage();
    if (!LibDiamond.checkCanCall(msg.sender, msg.data) && ts.isSellerTrusted[msg.sender] == 0) revert NotTrusted();
    address[] memory list = ts.collateralList;
    uint256 listLength = list.length;
    uint256[] memory balances = new uint256[](listLength);
    // Getting the balances of all collateral assets of the protocol to see if those do not decrease during
    // the swap: this is the only way to check that collateral assets have not been sold
    // Not checking the `subCollaterals` here as swaps should try to increase the balance of one collateral
    for (uint256 i; i < listLength; ++i) {
      balances[i] = IERC20(list[i]).balanceOf(address(this));
     }
     uint256 tokenPBalance = IERC20(address(ts.tokenP)).balanceOf(address(this));
+    // Only allow OdosRouterV2 single-swap entrypoints
+    if (payload.length < 4) revert InvalidSwap();
+    bytes4 selector = bytes4(payload);
+    if (
+      selector != IOdosRouterV2.swapCompact.selector &&
+      selector != IOdosRouterV2.swap.selector &&
+      selector != IOdosRouterV2.swapPermit2.selector
+    ) revert InvalidSwap();
     //solhint-disable-next-line
     (bool success, bytes memory result) = ODOS_ROUTER.call(payload);
     if (!success) _revertBytes(result);
-    amountOut = abi.decode(result, (uint256));
-    if (amountOut < minAmountOut) revert TooSmallAmountOut();
     if (IERC20(address(ts.tokenP)).balanceOf(address(this)) < tokenPBalance) revert InvalidTokens();
-    bool hasIncreased;
+    uint256 increases;
     address collateral;
+    uint256 balanceDelta;
     for (uint256 i; i < listLength; ++i) {
       uint256 newBalance = IERC20(list[i]).balanceOf(address(this));
       if (newBalance < balances[i]) {
         revert InvalidSwap();
       } else if (newBalance > balances[i]) {
-        hasIncreased = true;
+        increases++;
         collateral = list[i];
-        emit RewardsSoldFor(list[i], newBalance - balances[i]);
+        balanceDelta = newBalance - balances[i];
+        emit RewardsSoldFor(list[i], balanceDelta);
       }
     }
-    if (!hasIncreased) revert InvalidSwap();
+    if (increases != 1) revert InvalidSwap();
+    if (balanceDelta < minAmountOut) revert TooSmallAmountOut();
     Collateral storage collatInfo = s.transmuterStorage().collaterals[collateral];
     if (collatInfo.isManaged > 0) {
-      IERC20(collateral).safeTransfer(LibManager.transferRecipient(collatInfo.managerData.config), amountOut);
-      LibManager.invest(amountOut, collatInfo.managerData.config);
+      IERC20(collateral).safeTransfer(LibManager.transferRecipient(collatInfo.managerData.config), balanceDelta);
+      LibManager.invest(balanceDelta, collatInfo.managerData.config);
     }
   }
```

**Parallel:** Acknowledged
