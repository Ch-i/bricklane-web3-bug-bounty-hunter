---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-3-4
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-03-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-12-cyfrin-paladin-valkyrie-v2-0
title: Unsafe downcast in `ValkyrieSubscriber::toInt256` could silently overflow
vuln_class: []
---

# Unsafe downcast in `ValkyrieSubscriber::toInt256` could silently overflow

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-12-cyfrin-paladin-valkyrie-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md)_

---

**Description:** While it is highly unlikely that liquidity amounts will ever get close to overflowing `int256` for tokens with a reasonable number of decimals, there is an unsafe downcast in `ValkyrieSubscriber::toInt256` from `uint256` that could silently overflow:

```solidity
function toInt256(uint256 y) internal pure returns (int256 z) {
    z = int256(y);
}
```

This function is called with `notifySubscribe()`, `notifyUnsubscribe()`, and `notifyBurn()`, so a silent overflow could have serious consequences for incentive accounting.

**Impact:** The impact is limited as malicious pools are unlikely to be added for incentives. Nevertheless, the below proof of concept demonstrates how an attacker could abuse incentives by notifying a small removal of liquidity when in fact they unsubscribe their position.

**Proof of Concept:** The following test should be added to `ValkyrieSubscriber.t.sol`:

```solidity
function test_notifyUnsubscribe_Overflow() public {
    IncentivizedPoolId expectedId = IncentivizedPoolKey({ id: id, lpToken: address(0) }).toId();

    positionManager.notifySubscribe(0, EMPTY_BYTES);
    positionManager.notifySubscribe(5, EMPTY_BYTES);

    uint256 amount = uint256(type(int256).max);
    uint256 halfAmount = amount / 2;
    // add half the amount twice to overflow int256
    positionManager.notifyModifyLiquidity(5, int256(halfAmount), feeDelta);
    positionManager.notifyModifyLiquidity(5, int256(halfAmount), feeDelta);

    (IncentivizedPoolId receivedId, address account, int256 liquidityDelta) =
    incentiveManager.lastNotifyAddData(address(subscriber));

    assertEq(IncentivizedPoolId.unwrap(receivedId), IncentivizedPoolId.unwrap(expectedId));
    assertEq(account, owner2);
    assertEq(liquidityDelta, (int256(halfAmount)));

    // now remove full amount
    console.log("unsubscribing: notifies removal of all liquidity");
    positionManager.notifyUnsubscribe(5);

    (receivedId, account, liquidityDelta) =
    incentiveManager.lastNotifyRemoveData(address(subscriber));

    assertEq(IncentivizedPoolId.unwrap(receivedId), IncentivizedPoolId.unwrap(expectedId));
    assertEq(account, owner2);
    uint256 deltaU256 = uint256(-liquidityDelta);
    console.log("actually notified removal of %s liquidity due to overflow", deltaU256 / 1e18);
    assertGt(amount, deltaU256);
    console.log("unsubscribe removed all %s liquidity but reported different delta", amount / 1e18);
}
```

Output:
```bash
[PASS] test_notifyUnsubscribe_Overflow() (gas: 256275)
Logs:
  unsubscribing: notifies removal of all liquidity
  actually notified removal of 220 liquidity due to overflow
  unsubscribe removed all 57896044618658097711785492504343953926634992332820282019728 liquidity but reported different delta
```

**Recommended Mitigation:**
```diff
    function toInt256(uint256 y) internal pure returns (int256 z) {
++   if(y > uint256(type(int256).max)) revert("Overflow");
        z = int256(y);
    }
```

**Paladin:** Fixed by commit [`82ec6ff`](https://github.com/PaladinFinance/Valkyrie/pull/5/commits/82ec6ffafed645deab127f69c8c3798ba976f621).

**Cyfrin:** Verified. The OpenZeppelin `SafeCast` library is now used to perform checked downcasts.
