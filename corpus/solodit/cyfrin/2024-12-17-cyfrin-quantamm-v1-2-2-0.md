---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-17-cyfrin-quantamm-v1-2-2-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-12-17T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-quantamm-v1.2.md
tags:
- firm:cyfrin
- report:2024-12-17-cyfrin-quantamm-v1-2
title: '`UpdateWeightRunner::performUpdate` reverts on underflow when new multiplier
  is zero'
vuln_class: []
---

# `UpdateWeightRunner::performUpdate` reverts on underflow when new multiplier is zero

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-17-cyfrin-quantamm-v1.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-quantamm-v1.2.md)_

---

**Description:** In [`UpdateWeightRunner::_calculateMultiplerAndSetWeights`](https://github.com/QuantAMMProtocol/QuantAMM-V1/blob/7213401491f6a8fd1fcc1cf4763b15b5da355f1c/pkg/pool-quantamm/contracts/UpdateWeightRunner.sol#L433-L504), the new multiplier is determined by calculating the [change in weight over time](https://github.com/QuantAMMProtocol/QuantAMM-V1/blob/7213401491f6a8fd1fcc1cf4763b15b5da355f1c/pkg/pool-quantamm/contracts/UpdateWeightRunner.sol#L447).

To protect against unexpected values, a "last valid timestamp" for the multiplier is calculated in the section [here](https://github.com/QuantAMMProtocol/QuantAMM-V1/blob/7213401491f6a8fd1fcc1cf4763b15b5da355f1c/pkg/pool-quantamm/contracts/UpdateWeightRunner.sol#L453-L485).

When there is no change in weight, the multiplier becomes zero. This scenario is handled by a special case in the following code:
```solidity
int256 currentLastInterpolationPossible = type(int256).max;

for (uint i; i < local.currentWeights.length; ) {
    // ...

    if (blockMultiplier > int256(0)) {
        weightBetweenTargetAndMax = upperGuardRail - local.currentWeights[i];
        // ...
        blockTimeUntilGuardRailHit = weightBetweenTargetAndMax / blockMultiplier;
    } else if (blockMultiplier == int256(0)) {
        blockTimeUntilGuardRailHit = type(int256).max; // @audit if blockMultiplier is 0 this is max
    } else {
        weightBetweenTargetAndMax = local.currentWeights[i] - local.absoluteWeightGuardRail18;
        // ...
        blockTimeUntilGuardRailHit = weightBetweenTargetAndMax / int256(uint256(-1 * blockMultiplier));
    }
    // ...
}
// ...

//next expected update + time beyond that
currentLastInterpolationPossible += int40(uint40(block.timestamp));
```
If the weights remain unchanged and the multiplier is `0`, `currentLastInterpolationPossible` is set to `type(int256).max`. Consequently, the statement `currentLastInterpolationPossible += int40(uint40(block.timestamp))` will revert due to integer overflow.

The same overflow can also potentially happen if the multiplier is very small in the other branches as `weightBetweenTargetAndMax / blockMultiplier` could blow up.

**Impact:** Whenever the new multiplier is `0` (or extremely large), the call to `UpdateWeightRunner::performUpdate` will revert. This prevents updates from being executed when weights remain constant or under certain edge cases.

**Proof of Concept:** Add the following test to `pkg/pool-quantamm/test/foundry/UpdateWeightRunner.t.sol`:
```solidity
function testUpdatesFailsWhenMultiplierIsZero() public {
    vm.startPrank(owner);
    updateWeightRunner.setApprovedActionsForPool(address(mockPool), 3);
    vm.stopPrank();
    int256[] memory initialWeights = new int256[](4);
    initialWeights[0] = 0;
    initialWeights[1] = 0;
    initialWeights[2] = 0;
    initialWeights[3] = 0;

    // Set initial weights
    mockPool.setInitialWeights(initialWeights);

    int216 fixedValue = 1000;
    chainlinkOracle = deployOracle(fixedValue, 3601);

    vm.startPrank(owner);
    updateWeightRunner.addOracle(OracleWrapper(chainlinkOracle));
    vm.stopPrank();

    vm.startPrank(address(mockPool));

    address[][] memory oracles = new address[][](1);
    oracles[0] = new address[](1);
    oracles[0][0] = address(chainlinkOracle);

    uint64[] memory lambda = new uint64[](1);
    lambda[0] = 0.0000000005e18;
    updateWeightRunner.setRuleForPool(
        IQuantAMMWeightedPool.PoolSettings({
            assets: new IERC20[](0),
            rule: IUpdateRule(mockRule),
            oracles: oracles,
            updateInterval: 1,
            lambda: lambda,
            epsilonMax: 0.2e18,
            absoluteWeightGuardRail: 0.2e18,
            maxTradeSizeRatio: 0.2e18,
            ruleParameters: new int256[][](0),
            poolManager: addr2
        })
    );
    vm.stopPrank();

    vm.startPrank(addr2);
    updateWeightRunner.InitialisePoolLastRunTime(address(mockPool), 1);
    vm.stopPrank();

    vm.warp(block.timestamp + 10000000);
    mockRule.CalculateNewWeights(
        initialWeights,
        new int256[](0),
        address(mockPool),
        new int256[][](0),
        new uint64[](0),
        0.2e18,
        0.2e18
    );
    vm.expectRevert();
    updateWeightRunner.performUpdate(address(mockPool));
}

```

**Recommended Mitigation:** Consider guarding against overflow:
```diff
  //next expected update + time beyond that
+ if(currentLastInterpolationPossible < int256(type(int40).max)) {
      currentLastInterpolationPossible += int40(uint40(block.timestamp));
+ }
```

**QuantAMM:** Fixed in [`9b7a998`](https://github.com/QuantAMMProtocol/QuantAMM-V1/commit/9b7a998fca97fcb239c72d2cd762d9dc59e6ce8e)

**Cyfrin:** Verified. Overflow now prevented.
