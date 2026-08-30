---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-2-5
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-03-12T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-12-cyfrin-paladin-valkyrie-v2-0
title: Missing duplicate Incentive Logic can result in Incentive System accounting
  being broken
vuln_class: []
---

# Missing duplicate Incentive Logic can result in Incentive System accounting being broken

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-12-cyfrin-paladin-valkyrie-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md)_

---

**Description:** `IncentiveManager::addIncentiveLogic` allows the owner to add a new Incentive Logic to the list of Incentive Systems:

```solidity
function addIncentiveLogic(address logic) external onlyOwner {
    uint256 _index = nextIncentiveIndex;
    incentiveSystems[_index] = IncentiveSystem(logic, IIncentiveLogic(logic).updateOnSwap());
    incentiveSystemIndex[logic] = _index;
    nextIncentiveIndex++;

    emit NewIncentiveLogic(_index, logic);
}
```

Once added by the owner, an Incentive Logic can call `IncentiveManager::addPoolIncentiveSystem`:

```solidity
function addPoolIncentiveSystem(IncentivizedPoolId id) external onlyIncentiveLogics {
    uint256 _systemId = incentiveSystemIndex[msg.sender];
    if (poolListedIncentiveSystems[id][_systemId]) return;
    poolIncentiveSystems[id].push(_systemId);
    poolListedIncentiveSystems[id][_systemId] = true;
}
```

Given that there is no duplicate validation in `addIncentiveLogic()`, any existing index will be overwritten if this function is called more than once for the same logic address. This would mean that the Incentive Logic could also call `addPoolIncentiveSystem()` multiple times with different indexes being pushed to the `poolIncentiveSystems` array. This is highly likely to happen given that the function is invoked in every call to the permissionless `BaseIncentiveLogic::depositRewards`, and since the notification functions loop over all incentive systems attached to a given pool this would corrupt incentives accounting on the system itself.

**Impact:** Incentive system accounting will be broken if the owner mistakenly calls `IncentiveManager::addIncentiveLogic` more than once for a given Incentive Logic.

**Proof of Concept:** The following test should be added to `IncentiveManager.t.sol`:

```solidity
function test_addDuplicateIncentiveLogic() public {
    manager.addHook(address(hook1));
    hook1.notifyInitialize(pool1, lpToken1);
    hook1.notifyInitialize(pool2, lpToken2);

    vm.expectEmit(true, true, true, true);
    emit NewIncentiveLogic(1, address(logic1));
    manager.addIncentiveLogic(address(logic1));

    assertEq(manager.incentiveSystemIndex(address(logic1)), 1);

    assertEq(manager.poolListedIncentiveSystems(id1, 1), false);
    assertEq(manager.poolListedIncentiveSystems(id1, 2), false);

    logic1.addPoolIncentiveSystem(address(manager), id1);

    assertEq(manager.poolListedIncentiveSystems(id1, 1), true);
    assertEq(manager.poolListedIncentiveSystems(id1, 2), false);

    vm.expectEmit(true, true, true, true);
    emit NewIncentiveLogic(2, address(logic1));
    manager.addIncentiveLogic(address(logic1));

    assertEq(manager.incentiveSystemIndex(address(logic1)), 2);

    assertEq(manager.poolListedIncentiveSystems(id1, 1), true);
    assertEq(manager.poolListedIncentiveSystems(id1, 2), false);

    logic1.addPoolIncentiveSystem(address(manager), id1);

    assertEq(manager.poolListedIncentiveSystems(id1, 1), true);
    assertEq(manager.poolListedIncentiveSystems(id1, 2), true);

    (address system1, bool updateOnSwap1) = manager.incentiveSystems(1);
    assertEq(system1, address(logic1));
    assertEq(updateOnSwap1, false);

    (address system2, bool updateOnSwap2) = manager.incentiveSystems(2);
    assertEq(system2, address(logic1));
    assertEq(updateOnSwap2, false);


    int256 amount = int256(10 ether);

    uint256 prev_balance = logic1.userBalances(id1, user1);
    uint256 prev_user_liquidity = manager.poolUserLiquidity(id1, user1);
    uint256 prev_total_liquidity = manager.poolTotalLiquidity(id1);

    vm.expectEmit(true, true, true, true);
    emit LiquidityChange(id1, address(0), user1, uint256(amount));

    hook1.notifyAddLiquidty(pool1, lpToken1, user1, amount);

    uint256 new_balance = logic1.userBalances(id1, user1);
    uint256 new_user_liquidity = manager.poolUserLiquidity(id1, user1);
    uint256 new_total_liquidity = manager.poolTotalLiquidity(id1);

    assertEq(new_balance, prev_balance + uint256(amount));

    assertEq(new_user_liquidity, prev_user_liquidity + uint256(amount));
    assertEq(new_total_liquidity, prev_total_liquidity + uint256(amount));

    assertEq(manager.getPoolTotalLiquidity(id1), new_total_liquidity);
    assertEq(manager.getPoolUserLiquidity(id1, user1), new_user_liquidity);
}
```

Output showing failed assertion to to duplicated logic:
```bash
Ran 1 test for test/IncentiveManager.t.sol:TestIncentiveManager
[FAIL: assertion failed: 20000000000000000000 != 10000000000000000000] test_addDuplicateIncentiveLogic() (gas: 464110)
Traces:
  [464110] TestIncentiveManager::test_addDuplicateIncentiveLogic()
...
├─ [661] MockIncentiveLogic::userBalances(0xbfc3c7b8004ffcc0067b8de92da164f24769e5112a4f4f571b7f1d7f70c1d9d0, 0x000000000000000000000000000000000001B207) [staticcall]
│   └─ ← [Return] 20000000000000000000 [2e19]
├─ [908] IncentiveManager::poolUserLiquidity(0xbfc3c7b8004ffcc0067b8de92da164f24769e5112a4f4f571b7f1d7f70c1d9d0, 0x000000000000000000000000000000000001B207) [staticcall]
│   └─ ← [Return] 10000000000000000000 [1e19]
├─ [975] IncentiveManager::poolTotalLiquidity(0xbfc3c7b8004ffcc0067b8de92da164f24769e5112a4f4f571b7f1d7f70c1d9d0) [staticcall]
│   └─ ← [Return] 10000000000000000000 [1e19]
├─ [0] VM::assertEq(20000000000000000000 [2e19], 10000000000000000000 [1e19]) [staticcall]
│   └─ ← [Revert] assertion failed: 20000000000000000000 != 10000000000000000000
└─ ← [Revert] assertion failed: 20000000000000000000 != 10000000000000000000
```

**Recommended Mitigation:** Avoid overwriting an existing index for a given logic contract:
```diff
function addIncentiveLogic(address logic) external onlyOwner {
++  if(incentiveSystemIndex[logic] != 0) revert("Already added");
    uint256 _index = nextIncentiveIndex;
    incentiveSystems[_index] = IncentiveSystem(logic, IIncentiveLogic(logic).updateOnSwap());
    incentiveSystemIndex[logic] = _index;
    nextIncentiveIndex++;

    emit NewIncentiveLogic(_index, logic);
}
```

**Paladin:** Fixed by commit [`a7c3dc0`](https://github.com/PaladinFinance/Valkyrie/pull/5/commits/a7c3dc0a3c23fd26aad4d5aac8b1cd0288e5a55d).

**Cyfrin:** Verified. Execution now reverts if the owner attempts to add the same logic twice.
