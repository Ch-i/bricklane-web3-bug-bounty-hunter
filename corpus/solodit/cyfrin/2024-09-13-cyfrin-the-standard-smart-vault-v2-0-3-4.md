---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-09-13-cyfrin-the-standard-smart-vault-v2-0-3-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-09-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md
tags:
- firm:cyfrin
- report:2024-09-13-cyfrin-the-standard-smart-vault-v2-0
title: Native asset cannot be removed using `SmartVaultV4::removeAsset`
vuln_class: []
---

# Native asset cannot be removed using `SmartVaultV4::removeAsset`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md)_

---

**Description:** `SmartVault::removeAsset` allows Smart Vault owners to remove assets from their Vault, including collateral assets so long as the Vault remains fully collateralized. This currently works for ERC-20 collateral tokens; however, there is no handling for the case where `_tokenAddr == address(0)`. This address corresponds to the `NATIVE` symbol in the list of accepted `TokenManager` tokens, but native transfers attempted by `SafeERC20::safeTransfer` fail because this edge case is not considered.

```solidity
function removeAsset(address _tokenAddr, uint256 _amount, address _to) external onlyOwner {
    ITokenManager.Token memory token = getTokenManager().getTokenIfExists(_tokenAddr);
    if (token.addr == _tokenAddr && !canRemoveCollateral(token, _amount)) revert Undercollateralised();
    IERC20(_tokenAddr).safeTransfer(_to, _amount);
    emit AssetRemoved(_tokenAddr, _amount, _to);
}
```

While native collateral withdrawals are already correctly handled by `SmartVaultV4::removeCollateralNative`, this edge case results in an asymmetry between ERC-20 and native asset transfers within `SmartVault::removeAsset`.

**Impact:** Smart Vault owners cannot use `SmartVault::removeAsset` to remove native tokens from their Vault.

**Recommended Mitigation:** Consider handling the case where the native asset is attempted to be removed. Also, the use of events should be reconsidered depending on whether the asset removed is a collateral asset.

```diff
function removeAsset(address _tokenAddr, uint256 _amount, address _to) external onlyOwner {
    ITokenManager.Token memory token = getTokenManager().getTokenIfExists(_tokenAddr);
    if (token.addr == _tokenAddr && !canRemoveCollateral(token, _amount)) revert Undercollateralised();
+   if(_tokenAddr == address(0)) {
+       (bool sent,) = payable(_to).call{value: _amount}("");
+       if (!sent) revert TransferError();
+   } else {
-   IERC20(_tokenAddr).safeTransfer(_to, _amount);
+        IERC20(_tokenAddr).safeTransfer(_to, _amount);
+   }
    emit AssetRemoved(_tokenAddr, _amount, _to);
}
```

**The Standard DAO:** Fixed by commits [`8257c4c`](https://github.com/the-standard/smart-vault/commit/8257c4c267fa86c2c237ff6a2acdcfe94bcfeb20) & [`57d5db4`](https://github.com/the-standard/smart-vault/commit/57d5db47e072d8730c0d0988217db8d66ef565d9).

**Cyfrin:** Verified, native collateral can now be removed via either function.

\clearpage
