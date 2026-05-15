---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-11-cyfrin-strata-v2-1-2-5
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-06-11T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-11-cyfrin-strata-v2-1
title: Duplicate vaults can be pushed to `assetsArr`
vuln_class: []
---

# Duplicate vaults can be pushed to `assetsArr`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-11-cyfrin-strata-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md)_

---

**Description:** While `MetaVault::addVault` is protected by the `onlyOwner` modifier, there is no restriction on the number of times this function can be called with a given `vaultAddress` as argument:

```solidity
    function addVault(address vaultAddress) external onlyOwner {
        addVaultInner(vaultAddress);
    }

    function addVaultInner (address vaultAddress) internal {
        TAsset memory vault = TAsset(vaultAddress, EAssetType.ERC4626);
        assetsMap[vaultAddress] = vault;
@>      assetsArr.push(vault);

        emit OnVaultAdded(vaultAddress);
    }
```

In such a scenario, the vault will become duplicated within the `assetsArr` array. When called in `pUSDeVault::startYieldPhase`, the core redemption logic of `MetaVault::redeemMetaVaults` continues to function as expected. During the second iteration for the given vault address, the contract balance will simply be zero, so the redemption will be skipped, the `assetsMap` entry will again be re-written to default values, and the duplicate element will be removed from the array:

```solidity
    function removeVaultAndRedeemInner (address vaultAddress) internal {
        // Redeem
        uint balance = IERC20(vaultAddress).balanceOf(address(this));
@>      if (balance > 0) {
@>          IERC4626(vaultAddress).redeem(balance, address(this), address(this));
        }

        // Clean
        TAsset memory emptyAsset;
@>      assetsMap[vaultAddress] = emptyAsset;
        uint length = assetsArr.length;
        for (uint i = 0; i < length; i++) {
            if (assetsArr[i].asset == vaultAddress) {
                assetsArr[i] = assetsArr[length - 1];
@>              assetsArr.pop();
                break;
            }
        }
    }

    /// @dev Internal method to redeem all assets from supported vaults
    /// @notice Iterates through all supported vaults and redeems their assets for the base token
    function redeemMetaVaults () internal {
        while (assetsArr.length > 0) {
@>          removeVaultAndRedeemInner(assetsArr[0].asset);
        }
    }
```

However, if the given vault is removed from the list of supported vaults, `MetaVault::removeVault` will not allow the duplicate entry to be removed since the `requireSupportedVault()` invocation would fail on any subsequent attempt given that the mapping state is already overwritten to `address(0)` in the `removeVaultAndRedeemInner()` invocation:

```solidity
    function requireSupportedVault(address token) internal view {
@>      address vaultAddress = assetsMap[token].asset;
        if (vaultAddress == address(0)) {
            revert UnsupportedAsset(token);
        }
    }

    function removeVault(address vaultAddress) external onlyOwner {
@>      requireSupportedVault(vaultAddress);
        removeVaultAndRedeemInner(vaultAddress);

        emit OnVaultRemoved(vaultAddress);
    }
```

The consequence of this depends on the intentions of the owner:
* If they intend to keep the vault supported, all `MetaVault` functionality relying on the specified asset being a supported vault will revert if it has been attempted by the owner to remove a duplicated vault.
* If they intend to completely remove the vault, this will not be possible; however, it will also not be possible to make any subsequent deposits, so impact is limited to redeeming during the transition to the yield phase rather than instantaneously.

**Impact:** Vault assets could be redeemed later than intended and users could be temporarily prevented from withdrawing their funds.

**Proof of Concept:** The following test should be included in `pUSDeVault.t.sol`:

```solidity
function test_duplicateVaults() public {
    pUSDe.addVault(address(eUSDe));
    pUSDe.removeVault(address(eUSDe));
    assertFalse(pUSDe.isAssetSupported(address(eUSDe)));
    vm.expectRevert();
    pUSDe.removeVault(address(eUSDe));
}
```

**Recommended Mitigation:** Revert if the given vault has already been added.

**Strata:** Fixed in commit [787d1c7](https://github.com/Strata-Money/contracts/commit/787d1c72e86308897f06af775ed30b8dbef4cf2b).

**Cyfrin:** Verified.
