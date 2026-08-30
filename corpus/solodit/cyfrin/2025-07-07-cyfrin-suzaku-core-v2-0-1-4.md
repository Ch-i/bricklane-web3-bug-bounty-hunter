---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-1-4
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-07-07T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-07-cyfrin-suzaku-core-v2-0
title: Inconsistent stake calculation due to mutable `vaultManager` reference in `AvalancheL1Middleware`
vuln_class: []
---

# Inconsistent stake calculation due to mutable `vaultManager` reference in `AvalancheL1Middleware`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-07-cyfrin-suzaku-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md)_

---

**Description**

The `AvalancheL1Middleware` contract permits updating the `vaultManager` reference. However, doing so can introduce **critical inconsistencies** in logic that depends on stateful or historical data tied to the original `vaultManager`. Key issues include:

* **Vaults registered in the original manager are not migrated** to the new one.
* **Time-based metadata** like `enabledTime` and `disabledTime` resets upon re-registration, misaligning historical activity.
* Core logic in `getOperatorStake()` depends on `_wasActiveAt()`, which checks whether a vault was active during a given epoch.
* Replacing the `vaultManager` disrupts this check, leading to:

  * Ignored historical stakes
  * Miscounted or missed vaults
  * Incorrect stake attribution

This breaks key protocol guarantees across the middleware and compromises correctness in systems like staking(node creation) and rewards.

**Illustrative Flow**

1. Register vault `V1` in the original `vaultManager`.
2. Replace with `vaultManagerV2` via `setVaultManager()`.
3. Re-register `V1` in `vaultManagerV2` — note: `enabledTime` is reset.
4. Query `getOperatorStake()` for an epoch before re-registration.
5. `_wasActiveAt()` returns `false`, excluding the stake.

**Impact**

* **Data Inconsistency**: `getOperatorStake()` may return incorrect values.
* **Broken Epoch Tracking**: Epoch-based logic dependent on vault state (like `_wasActiveAt`) becomes unreliable.

**Proof of Concept**

```solidity
    function test_changeVaultManager() public {
        // Move forward to let the vault roll epochs
        uint48 epoch = _calcAndWarpOneEpoch();

        uint256 operatorStake = middleware.getOperatorStake(alice, epoch, assetClassId);
        console2.log("Operator stake (epoch", epoch, "):", operatorStake);
        assertGt(operatorStake, 0);

        MiddlewareVaultManager vaultManager2 = new MiddlewareVaultManager(address(vaultFactory), owner, address(middleware));

        vm.startPrank(validatorManagerAddress);
        middleware.setVaultManager(address(vaultManager2));
        vm.stopPrank();

        uint256 operatorStake2 = middleware.getOperatorStake(alice, epoch, assetClassId);
        console2.log("Operator stake (epoch", epoch, "):", operatorStake2);
        assertEq(operatorStake2, 0);
    }

```

**Recommended Mitigation**

Consider eliminating the ability to arbitrarily update the `vaultManager` once the middleware is initialized. Flexibility to update this variable introduces unintended side-effects that likely expand the attack surface.

**Suzaku:**
Fixed in commit [35f6e56](https://github.com/suzaku-network/suzaku-core/pull/155/commits/35f6e5604c9d3ea77ad38424bb7587f4977f2146).

**Cyfrin:** Verified.
