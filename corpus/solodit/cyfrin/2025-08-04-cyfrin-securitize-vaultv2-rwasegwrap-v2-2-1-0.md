---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2-1-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-08-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md
tags:
- firm:cyfrin
- report:2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2
title: Missing storage gap in upgradeable parent contract causes storage slot collision
  risk
vuln_class: []
---

# Missing storage gap in upgradeable parent contract causes storage slot collision risk

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md)_

---

**Description:** The `VaultDeployer` abstract contract is designed to be upgradeable and inherited by child contracts `SegregatedVaultDeployer` and `SecuritizeVaultDeployer`. However, `VaultDeployer` lacks storage gap variables to reserve space for future upgrades.

Currently, `VaultDeployer` declares three state variables:
- `address public navProvider`
- `address internal admin`
- `address public upgradeableBeacon`

The child contracts add their own state variables after the parent's storage:
- `SecuritizeVaultDeployer` adds `redemptionAddress` and `feeManager`
- `SegregatedVaultDeployer` currently adds no additional state variables

In upgradeable contracts, when a parent contract adds new state variables in future versions, those variables are allocated to storage slots immediately following the existing parent variables. This will overwrite the storage slots currently occupied by child contract variables, leading to storage collision and data corruption.

While `BaseContract` (the grandparent) properly implements storage gaps with `uint256[50] private __gap`, the intermediate `VaultDeployer` contract breaks this pattern by not reserving space for its own future expansion.

**Impact:** If future versions of `VaultDeployer` add new state variables, they will overwrite child contract storage slots causing data corruption and potentially rendering deployed contracts unusable.

**Recommended Mitigation:** Add storage gap variables to `VaultDeployer` contract to reserve space for future upgrades. Choose either traditional storage gaps or ERC-7201 namespaced storage:

**Option 1: Traditional Storage Gap**
```diff
abstract contract VaultDeployer is IVaultDeployer, BaseContract {
    bytes32 public constant AGGREGATOR_ROLE = keccak256("AGGREGATOR_ROLE");

    address public navProvider;
    address internal admin;
    address public upgradeableBeacon;

+   // Reserve storage slots for future VaultDeployer upgrades
+   uint256[47] private __gap;

    // ... rest of contract
}
```

**Option 2: ERC-7201 Namespaced Storage**
```diff
abstract contract VaultDeployer is IVaultDeployer, BaseContract {
    /// @custom:storage-location erc7201:securitize.storage.VaultDeployer
    struct VaultDeployerStorage {
        address navProvider;
        address admin;
        address upgradeableBeacon;
    }

    // keccak256(abi.encode(uint256(keccak256("securitize.storage.VaultDeployer")) - 1)) & ~bytes32(uint256(0xff))
    bytes32 private constant VAULT_DEPLOYER_STORAGE_LOCATION = 0x...;

    function _getVaultDeployerStorage() private pure returns (VaultDeployerStorage storage $) {
        assembly {
            $.slot := VAULT_DEPLOYER_STORAGE_LOCATION
        }
    }

    // Update all variable access to use the storage struct
    // ... rest of contract
}
```

**Securitize:** Fixed in commit [3048c3](https://github.com/securitize-io/bc-securitize-vault-sc/commit/3048c3ee21d18fe3a30c4d55ec96332f379bbcdc).

**Cyfrin:** Verified.
