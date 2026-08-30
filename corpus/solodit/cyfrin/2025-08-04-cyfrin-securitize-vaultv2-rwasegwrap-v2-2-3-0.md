---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2-3-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-08-04T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md
tags:
- firm:cyfrin
- report:2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2
title: Unnecessary `_msgSender()` call in `_resolveVaultId` when `caller` parameter
  is available
vuln_class: []
---

# Unnecessary `_msgSender()` call in `_resolveVaultId` when `caller` parameter is available

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md)_

---

**Description:** In `RWASegWrap::_resolveVaultId()`, the function receives a `caller` parameter representing the address for which a vault ID should be resolved, but when calling `_addVault()`, it uses `_msgSender()` instead of the provided `caller` parameter. This creates an unnecessary function call and potential inconsistency since the `caller` parameter already contains the correct address.

```solidity
function _resolveVaultId(address caller) internal returns (uint256) {
    uint256 vaultId = getVaultId(caller);
    if (vaultId == 0) {
        vaultId = ++latestVaultId;
        ISegregatedVault vault = _deployVault(vaultId);
        _addVault(address(vault), vaultId, _msgSender()); // <- use caller directly
    }
    return vaultId;
}
```

**Impact:** The unnecessary `_msgSender()` call results in additional gas consumption and reduces code clarity by using different variables that should represent the same address.

**Recommended Mitigation:** Replace `_msgSender()` with the `caller` parameter in the `_addVault()` call:

```diff
function _resolveVaultId(address caller) internal returns (uint256) {
    uint256 vaultId = getVaultId(caller);
    if (vaultId == 0) {
        vaultId = ++latestVaultId;
        ISegregatedVault vault = _deployVault(vaultId);
-       _addVault(address(vault), vaultId, _msgSender());
+       _addVault(address(vault), vaultId, caller);
    }
    return vaultId;
}
```

**Securitize:** Fixed in commit [3e16e8](https://github.com/securitize-io/bc-securitize-vault-sc/commit/3e16e88ea071e3365e7fd0b70789b22c0f717ccd).

**Cyfrin:** Verified.
