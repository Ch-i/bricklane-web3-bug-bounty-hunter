---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-3-5
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-03-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-12-cyfrin-paladin-valkyrie-v2-0
title: Positions can be locked by malicious re-initialization in the event of multiple
  `ValkyrieSubscriber` contracts being deployed
vuln_class: []
---

# Positions can be locked by malicious re-initialization in the event of multiple `ValkyrieSubscriber` contracts being deployed

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-12-cyfrin-paladin-valkyrie-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md)_

---

**Description:** `IncentiveManager::notifyInitialize` does not currently check whether there is already an assigned hook corresponding to a give pool identifier:

```solidity
function notifyInitialize(PoolId id, address lpToken) external onlyAllowedHooks {
    IncentivizedPoolId _id = _convertToIncentivizedPoolId(id, lpToken);
    listedPools[_id] = true;
    poolLinkedHook[_id] = msg.sender;
}
```

Therefore, if this function can be called again then the permissioned role can be taken, preventing the previous one from executing any of the other methods. While it is understood that there are currently no plans to have multiple deployments of the `ValkyrieSubscriber` contract, a position could be maliciously reinitialized on a new subscriber due to this missing validation in `IncentiveManager::notifyInitialize`.

Note that this is not currently an issue for the hooks as `BaseHook` enforces the initialization invariant, and there is no overlap between these hook positions and those of the subscriber.

**Proof of Concept:** Imagine there are two different instance of `ValkyrieSubscriber` (`subscriberA` and `subscriberB`):
1. Users call `Notifier::subscribe` on their position for `subscriberA`, executing the following:

```solidity
function notifySubscribe(uint256 tokenId, bytes memory /*data*/) external override onlyPositionManager {
    (PoolKey memory poolKey,) = positionManager.getPoolAndPositionInfo(tokenId);
    PoolId poolId = poolKey.toId();

    if(!_initializedPools[poolId]) {
        if (address(incentiveManager) != address(0)) {
            incentiveManager.notifyInitialize(poolId, address(0));
        }
        _initializedPools[poolId] = true;
    }
    ...
}
```

The first user subscription will trigger the `IncentiveManager::notifyInitialize`, assigning the linked hook to `subscriberA`. Notice that any subsequent subscriptions to `subscriberA` will no longer trigger this method.

2. A malicious user calls `Notifier::subscribe` from a position of the same Uniswap pool pointing to `subscriberB`.
This other subscriber will trigger the same functions and `poolLinkedHook` will be assigned to the `subscriberB`.

3. At this point, all users that subscribed to `subscriberA` can no longer interact with their positions. Upon attempting to do so, any action on their positions will trigger a notification on `subscriberA` that will call the `IncentiveManager`, but the execution will fail due to this validation:

```solidity
function notifyAddLiquidty(PoolId id, address lpToken, address account, int256 liquidityDelta)
    external
    onlyAllowedHooks
{
    ...
    if (poolLinkedHook[_id] != msg.sender) revert NotLinkedHook();
    ...
}

function notifyRemoveLiquidty(PoolId id, address lpToken, address account, int256 liquidityDelta)
    external
    onlyAllowedHooks
{
    ...
    if (poolLinkedHook[_id] != msg.sender) revert NotLinkedHook();
    ...
}

function _notifySwap(PoolId id, address lpToken) internal {
    ...
    if (poolLinkedHook[_id] != msg.sender) revert NotLinkedHook();
    ...
}
```

Note that honest users would still be able to subscribe to `subscriberA` but this would result in their positions being locked forever.

The following test should be placed in `ValkyrieSubscriber.t.sol`:

```solidity
function test_MoreThanOneSubscriber() public {
    IncentiveManager incentiveManagerRealImplementation = new IncentiveManager();
    ValkyrieSubscriber subscriberA = new ValkyrieSubscriber(IIncentiveManager(address(incentiveManagerRealImplementation)), PositionManager(payable(address(positionManager))));
    ValkyrieSubscriber subscriberB = new ValkyrieSubscriber(IIncentiveManager(address(incentiveManagerRealImplementation)), PositionManager(payable(address(positionManager))));
    incentiveManagerRealImplementation.addHook(address(subscriberA));
    incentiveManagerRealImplementation.addHook(address(subscriberB));

    IncentivizedPoolId expectedId = IncentivizedPoolKey({ id: id, lpToken: address(0) }).toId();

    // Mock function to route the call to the specific subscriber
    positionManager.setSubscriber(subscriberA);

    // Some user subscribes their position number 0 to subscriberA
    positionManager.notifySubscribe(0, EMPTY_BYTES);

    // Mock function to route the call to the specific subscriber
    positionManager.setSubscriber(subscriberB);

    // Some other user subscribes their position number 5 to subscriberA
    positionManager.notifySubscribe(5, EMPTY_BYTES);

    // Mock function to route the call to the specific subscriber
    positionManager.setSubscriber(subscriberA);

    // At this point the first user that subscribed to SubscriberA will not be able to do anything
    vm.expectRevert();
    positionManager.notifyUnsubscribe(0);

    vm.expectRevert();
    positionManager.notifyBurn(0, address(this), pos2, 195e18, feeDelta);

    vm.expectRevert();
    positionManager.notifyModifyLiquidity(0, 35e18, feeDelta);
}
```

**Impact:** The impact is currently limited due to the intention to only ever deploy a single subscriber contract. If this were to change without applying the recommended mitigation then this would greatly increase the severity.

**Recommended Mitigation:** Add the following validation to `IncentiveManager::notifyInitialize`:

```diff
    function notifyInitialize(PoolId id, address lpToken) external onlyAllowedHooks {
        IncentivizedPoolId _id = _convertToIncentivizedPoolId(id, lpToken);
++      require(poolLinkedHook[_id] == address(0), "Hook already linked");
        listedPools[_id] = true;
        poolLinkedHook[_id] = msg.sender;
    }
```

**Paladin:** Fixed by commit [`ae96366`](https://github.com/PaladinFinance/Valkyrie/pull/5/commits/ae963669375a24716c9f857c3c0bfdfef558725e).

**Cyfrin:** Verified. Pools managed by the `ValkyrieSubscriber` can no longer be re-initialized.
