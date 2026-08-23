---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-2-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-07-07T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-07-cyfrin-suzaku-core-v2-0
title: Vault limit cannot be modified if vault Is already enabled
vuln_class: []
---

# Vault limit cannot be modified if vault Is already enabled

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-07-cyfrin-suzaku-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md)_

---

**Description**

The `updateVaultMaxL1Limit` function reverts with `MapWithTimeData__AlreadyEnabled` when attempting to increase or decrease the vault limit if the vault is already enabled. This behavior occurs due to the call to `vaults.enable(vault)` within the function, which fails when the vault is already in an enabled state.

```solidity
function updateVaultMaxL1Limit(address vault, uint96 assetClassId, uint256 vaultMaxL1Limit) external onlyOwner {
    if (!vaults.contains(vault)) {
        revert AvalancheL1Middleware__NotVault(vault);
    }
    if (vaultToAssetClass[vault] != assetClassId) {
        revert AvalancheL1Middleware__WrongVaultAssetClass();
    }

    _setVaultMaxL1Limit(vault, assetClassId, vaultMaxL1Limit);

    if (vaultMaxL1Limit == 0) {
        vaults.disable(vault);
    } else {
        vaults.enable(vault);
    }
}
```

**Impact**

Calling `updateVaultMaxL1Limit` with a non-zero `vaultMaxL1Limit` for an already-enabled vault results in a revert, breaking the expected behavior. The current design requires the vault to be explicitly disabled before setting a new non-zero limit and enabling it again. This workflow is unintuitive and introduces unnecessary friction for the contract owner or administrator.

**Proof of Concept**

The following test will fail due to the described behavior. Add it to the `AvalancheL1MiddlewareTest`:

```solidity
function testUpdateVaultMaxL1Limit() public {
    vm.startPrank(validatorManagerAddress);

    // Attempt to update to a new non-zero limit while vault is already enabled
    vaultManager.updateVaultMaxL1Limit(address(vault), 1, 500 ether);

    vm.stopPrank();
}
```

**Recommended Mitigation**

Consider modifying the logic inside `updateVaultMaxL1Limit` to check the current enabled state before attempting to enable or disable. Only call `vaults.enable(vault)` or `vaults.disable(vault)` if there is an actual state transition.

**Suzaku:**
Fixed in commit [a9f6aaa](https://github.com/suzaku-network/suzaku-core/pull/155/commits/a9f6aaa92bd3800335c4d8085225a23a38c58b34).

**Cyfrin:** Verified.
