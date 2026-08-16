---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-17-cyfrin-octodefi-v2-0-1-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-07-17T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-17-cyfrin-octodefi-v2-0
title: DoS of strategy execution due to array indices out of bounds
vuln_class: []
---

# DoS of strategy execution due to array indices out of bounds

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-17-cyfrin-octodefi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md)_

---

**Description:** `StrategyBuilderPlugin._validateStep()` intends to enforce that the condition results reference a new index that does not exceed the maximum step index:

```solidity
function _validateStep(StrategyStep memory step, uint256 maxStepIndex) internal pure {
    if (step.condition.result0 > maxStepIndex || step.condition.result1 > maxStepIndex) {
        revert InvalidNextStepIndex();
    }
}
```

However, given `maxStepIndex` is passed as the array length, this fails to account for zero indexing and as a it is possible to add a strategy that reverts during execution due to array index out of bounds if an off-by-one index is specified.

**Impact:** Strategies can be created that will cause DoS of execution.

**Proof of Concept:** The following test can be added to `StrategyBuilderPlugin.t.sol`:

```solidity
function test_executeStrategy_OOB() external {
    uint256 numSteps = 2;
    IStrategyBuilderPlugin.StrategyStep[] memory steps = _createStrategySteps(numSteps);
    steps[0].condition.result0 = 2;
    steps[0].condition.result1 = 2;
    uint32 strategyID = 222;

    deal(address(account1), 100 ether);

    //Mocks
    vm.mockCall(
        feeController,
        abi.encodeWithSelector(IFeeController.getTokenForAction.selector),
        abi.encode(address(0), false)
    );

    vm.mockCall(
        feeController,
        abi.encodeWithSelector(IFeeController.functionFeeConfig.selector),
        abi.encode(IFeeController.FeeConfig({feeType: IFeeController.FeeType.Deposit, feePercentage: 0}))
    );
    vm.mockCall(feeController, abi.encodeWithSelector(IFeeController.minFeeInUSD.selector), abi.encode(0));

    //Act
    vm.startPrank(address(account1));
    strategyBuilderPlugin.createStrategy(strategyID, creator, steps);

    strategyBuilderPlugin.executeStrategy(strategyID);
    vm.stopPrank();

    //Assert
    assertEq(tokenReceiver.balance, numSteps * 2 * TOKEN_SEND_AMOUNT);
}
```

**Recommended Mitigation:** should be >= to account for zero indexing

```diff
    function _validateStep(StrategyStep memory step, uint256 maxStepIndex) internal pure {
--      if (step.condition.result0 > maxStepIndex || step.condition.result1 > maxStepIndex) {
++      if (step.condition.result0 >= maxStepIndex || step.condition.result1 >= maxStepIndex) {
            revert InvalidNextStepIndex();
        }
    }
```

**OctoDeFi:** Fixed in PR [\#15](https://github.com/octodefi/strategy-builder-plugin/pull/15).

**Cyfrin:** Verified. Validation now uses the correct operator.
