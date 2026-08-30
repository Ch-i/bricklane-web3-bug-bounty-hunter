---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-11-cyfrin-strata-v2-1-4-5
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-06-11T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-11-cyfrin-strata-v2-1
title: Superfluous vault support validation can be removed from `pUSDeDepositor::deposit`
vuln_class: []
---

# Superfluous vault support validation can be removed from `pUSDeDepositor::deposit`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-11-cyfrin-strata-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md)_

---

**Description:** If the caller to `pUSDeDepositor::deposit` attempts to deposit a vault token that is not `USDe` or one of those preconfigured with an auto swap path, it will first query `MetaVault::isAssetSupported`:

```solidity
    function deposit(IERC20 asset, uint256 amount, address receiver) external returns (uint256) {
        address user = _msgSender();
        ...
        IMetaVault vault = IMetaVault(address(pUSDe));
@>      if (vault.isAssetSupported(address(asset))) {
            SafeERC20.safeTransferFrom(asset, user, address(this), amount);
            asset.approve(address(vault), amount);
            return vault.deposit(address(asset), amount, receiver);
        }
@>      revert InvalidAsset(address(asset));
    }
```

If the specified vault token fails all validation then it falls through to the `InvalidAsset` custom error; however, this is not strictly necessary as `MetaVault::deposit` already performs the same validation within `MetaVault::requireSupportedVault`:

```solidity
    function deposit(address token, uint256 tokenAssets, address receiver) public virtual returns (uint256) {
        if (token == asset()) {
            return deposit(tokenAssets, receiver);
        }
@>      requireSupportedVault(token);
        ...
    }

    function requireSupportedVault(address token) internal view {
        address vaultAddress = assetsMap[token].asset;
        if (vaultAddress == address(0)) {
@>          revert UnsupportedAsset(token);
        }
    }
```

**Recommended Mitigation:** If it is not intentionally desired to fail early, consider removing the superfluous validation to save gas in the happy path case:

```diff
function deposit(IERC20 asset, uint256 amount, address receiver) external returns (uint256) {
        address user = _msgSender();
        ...
        IMetaVault vault = IMetaVault(address(pUSDe));
--      if (vault.isAssetSupported(address(asset))) {
            SafeERC20.safeTransferFrom(asset, user, address(this), amount);
            asset.approve(address(vault), amount);
            return vault.deposit(address(asset), amount, receiver);
--      }
--      revert InvalidAsset(address(asset));
    }
```

**Strata:** Fixed in commit [7f0c5dc](https://github.com/Strata-Money/contracts/commit/7f0c5dc54d1230589e2d9403b69effd64fb35227).

**Cyfrin:** Verified.
