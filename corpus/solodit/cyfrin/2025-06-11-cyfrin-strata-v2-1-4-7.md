---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-11-cyfrin-strata-v2-1-4-7
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-06-11T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-11-cyfrin-strata-v2-1
title: Unnecessarily complex iteration logic in `MetaVault::redeemMetaVaults` can
  be simplified
vuln_class: []
---

# Unnecessarily complex iteration logic in `MetaVault::redeemMetaVaults` can be simplified

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-11-cyfrin-strata-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md)_

---

**Description:** `MetaVault::redeemMetaVaults` is currently implemented as a while loop, indexing the first array element and calling `MetaVault::removeVaultAndRedeemInner` which implements a "replace-and-pop" solution for removing elements from the `assetsArr` array:

```solidity
    function removeVaultAndRedeemInner (address vaultAddress) internal {
        // Redeem
        uint balance = IERC20(vaultAddress).balanceOf(address(this));
        if (balance > 0) {
            IERC4626(vaultAddress).redeem(balance, address(this), address(this));
        }

        // Clean
        TAsset memory emptyAsset;
        assetsMap[vaultAddress] = emptyAsset;
        uint length = assetsArr.length;
        for (uint i = 0; i < length; i++) {
            if (assetsArr[i].asset == vaultAddress) {
@>              assetsArr[i] = assetsArr[length - 1];
@>              assetsArr.pop();
                break;
            }
        }
    }

    function redeemMetaVaults () internal {
        while (assetsArr.length > 0) {
@>          removeVaultAndRedeemInner(assetsArr[0].asset);
        }
    }
```

While this logic is still required for use in `MetaVault::removeVault`, where the contract admin can manually remove a single underlying vault, it would be preferable to avoid re-using this functionality for `MetaVault::redeemMetaVaults`. Instead, starting at the final element and walking backwards would preserve the ordering of the array and avoid unnecessary storage writes.

**Strata:** Fixed in commit [fbb6818](https://github.com/Strata-Money/contracts/commit/fbb6818f5c1f621a25c58a40f1673609ad9611fb) and [98bd92d](https://github.com/Strata-Money/contracts/commit/98bd92d0aed75161332227239859c34161df1bcc).

**Cyfrin:** Verified. The logic has been simplified by iterating over the asset addresses, deleting the individual mapping entries, and finally deleting the array.
