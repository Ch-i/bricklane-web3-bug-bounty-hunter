---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2-1-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-08-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md
tags:
- firm:cyfrin
- report:2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2
title: Upgradeable contract initializer not disabled in constructor allows implementation
  contract initialization
vuln_class: []
---

# Upgradeable contract initializer not disabled in constructor allows implementation contract initialization

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md)_

---

**Description:** The `SegregatedVault` contract is designed as an upgradeable contract using the UUPS (Universal Upgradeable Proxy Standard) pattern, inheriting from `BaseContract` which extends `UUPSUpgradeable`. However, the implementation contract fails to disable its initializer in the constructor, creating a security vulnerability.

In UUPS upgradeable contracts, the implementation contract should have its initializer disabled in the constructor to prevent direct initialization of the implementation contract itself. Without this protection, an attacker could potentially call `SegregatedVault::initialize` directly on the implementation contract, granting themselves admin privileges and potentially disrupting the intended proxy-based upgrade mechanism.

The `SegregatedVault::initialize` function grants `DEFAULT_ADMIN_ROLE` to `msg.sender`, which would be the attacker if called directly on the implementation. This could allow unauthorized access to admin-only functions like role management and contract upgrades.

Similar issues exist in other upgradeable contracts in the codebase:
- `SecuritizeVaultV2` in the bc-securitize-vault-sc module lacks constructor initializer disabling
- `SecuritizeVault` in the bc-securitize-vault-sc module lacks constructor initializer disabling
- `RWASegWrap` lacks constructor initializer disabling
- `SecuritizeRWASegWrap` lacks constructor initializer disabling

All these contracts follow the same pattern of inheriting from `BaseContract` and implementing UUPS upgradeability without properly securing the implementation contract.

**Impact:** An attacker could initialize the implementation contract directly to gain unauthorized admin privileges and potentially compromise the upgrade mechanism for all proxy instances.

**Recommended Mitigation:** Add a constructor that disables the initializer to prevent direct initialization of the implementation contract:

```diff
contract SegregatedVault is ERC4626Upgradeable, ISegregatedVault, IVaultAccessControl, BaseContract {

+   /// @custom:oz-upgrades-unsafe-allow constructor
+   constructor() {
+       _disableInitializers();
+   }
```

Apply the same fix to other affected upgradeable contracts: `SecuritizeVaultV2`, `SecuritizeVault`, `RWASegWrap`, and `SecuritizeRWASegWrap`.

**Securitize:** Fixed in commits [1261ec](https://github.com/securitize-io/bc-securitize-vault-sc/commit/1261ec95e1f080c628193e19a00bc9e6808ffbaa) and [1a2f4c](https://github.com/securitize-io/bc-rwa-seg-wrap-sc/commit/1a2f4c5a4d52e297e2662c15ba50aae30238c093).

**Cyfrin:** Verified.
