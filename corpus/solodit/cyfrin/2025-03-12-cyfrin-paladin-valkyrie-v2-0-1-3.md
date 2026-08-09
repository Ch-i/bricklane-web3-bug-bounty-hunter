---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-1-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-03-12T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-12-cyfrin-paladin-valkyrie-v2-0
title: Swaps are not possible on pools registered with Bunni due to incorrect access
  control in `ValkyrieHooklet::afterSwap`
vuln_class: []
---

# Swaps are not possible on pools registered with Bunni due to incorrect access control in `ValkyrieHooklet::afterSwap`

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-12-cyfrin-paladin-valkyrie-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md)_

---

**Description:** `ValkyrieHooklet::afterSwap` has the `onlyBunniHub` modifier applied; however, this hook is invoked from `BunniHook` (using the `BunniHookLogic` library) and not `BunniHub` (using the `BunniHubLogic` library). As such, this will result in a DoS of swap functionality for pools registered with Bunni and configured with the `ValkyrieHooklet`.

```solidity
function afterSwap(
    address,
    PoolKey calldata key,
    IPoolManager.SwapParams calldata,
    SwapReturnData calldata
) external override onlyBunniHub returns (bytes4 selector) {
    PoolId poolId = key.toId();
    if (address(incentiveManager) != address(0)) {
        incentiveManager.notifySwap(poolId, bunniTokens[poolId]);
    }
    return ValkyrieHooklet.afterSwap.selector;
}
```

Related to this, `ValkyrieHooklet::beforeSwap` while a no-op hook is the only non-view function missing access control and should mirror the correct access control applied to `ValkyrieHooklet::afterSwap`.

**Impact:** While the incentive logic is not directly affected, swaps will not be possible for pools registered with Bunni and configured with the `ValkyrieHooklet`, therefore rendering it useless.

**Proof of Concept:** The current `MockBunniHub` includes the following function:

```solidity
function afterDeposit(
    address hooklet,
    address caller,
    IBunniHub.DepositParams calldata params,
    IHooklet.DepositReturnData calldata returnData
) external {
    ValkyrieHooklet(hooklet).afterDeposit(
        caller,
        params,
        returnData
    );
}
```

Therefore, `test_afterSwap()` in `ValkyrieHooklet.t.sol` does not revert; however, this issue will become apparent with a test failure when the test suite is updated to use the actual Bunni v2 codebase.

**Recommended Mitigation:** Apply the correct `onlyBunniHook` modifier to both `ValkyrieHooklet::afterSwap` and `ValkyrieHooklet::beforeSwap`.

**Paladin:** Fixed by commit [`333f26b`](https://github.com/PaladinFinance/Valkyrie/pull/5/commits/333f26bcdad465cae4f7fbdeee8ebfca2ce43659).

**Cyfrin:** Verified. `ValkyrieHooklet::afterSwap` now checks the correct caller using the newly-added `onlyHook` modifier. Note that the `bunniHook` NatSpec has been erroneously copied from `bunniHub`.

**Paladin:** In the latest version of the branch, the Natspec is `/// @dev Modifier to check that the caller is the BunniHook`.

**Cyfrin:** Acknowledged.
