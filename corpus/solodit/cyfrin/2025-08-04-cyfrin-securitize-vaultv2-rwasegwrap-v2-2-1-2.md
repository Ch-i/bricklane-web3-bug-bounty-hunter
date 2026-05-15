---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2-1-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-08-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md
tags:
- firm:cyfrin
- report:2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2
title: Incomplete mapping updates in `setVault` function cause vault address inconsistencies
vuln_class: []
---

# Incomplete mapping updates in `setVault` function cause vault address inconsistencies

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md)_

---

**Description:** The `RWASegWrap::setVault` function allows admins to update the vault address for a specific vault ID, but it fails to properly maintain the bidirectional mapping between vault addresses and vault IDs. The function only updates `vaults[id] = vault` but does not update the `vaultIds` mapping, which should map the new vault address to the vault ID and clear the mapping for the old vault address.
This creates inconsistencies in the contract's state where the old vault address remains mapped to the vault ID in the `vaultIds` mapping, while the new vault address is not recognized by the system. The `vaultIds` mapping is critical for vault validation in functions like `isValidVault` and `getAssetId`, and is also used in `_addVault` to prevent duplicate vault registrations. The same issue exists in the `SecuritizeRWASegWrap` contract, which inherits from `RWASegWrap` and uses the same `setVault` implementation.

**Impact:** The incomplete mapping updates can cause vault operations to fail or behave unexpectedly, as the new vault address will not be recognized as valid by the system, while the old vault address may still appear valid even though it's no longer active.

**Recommended Mitigation:** Update the `setVault` function to properly maintain both mappings:

```diff
function setVault(
    address vault,
    uint256 id
) public virtual override onlyRole(DEFAULT_ADMIN_ROLE) idNotZero(id) recognizedVault(id) addressNotZero(vault) {
    address oldVault = vaults[id];
    address investorWallet = vaultIdOwnerWallets[id];
    vaults[id] = vault;
+   delete vaultIds[oldVault];
+   vaultIds[vault] = id;
    emit VaultUpdated(oldVault, vault, id, investorWallet);
}
```

**Securitize:** Fixed in commit [468bae](https://github.com/securitize-io/bc-securitize-vault-sc/commit/468bae9777ad341c700dcf30caec057f6ba101c3).

**Cyfrin:** Verified.
