---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2-1-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-08-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md
tags:
- firm:cyfrin
- report:2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2
title: Unsafe ERC20 operations can cause unexpected failures with non-standard tokens
vuln_class: []
---

# Unsafe ERC20 operations can cause unexpected failures with non-standard tokens

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md)_

---

**Description:** The protocol uses direct `IERC20.transferFrom` and `IERC20.approve` function calls instead of OpenZeppelin's `SafeERC20` library wrappers. This creates compatibility issues with tokens that do not return boolean values or have non-standard implementations.

The primary occurrence is in `RWASegWrap::_pullAndApprove`, which is a critical internal function used during deposit and mint operations. When users call `depositById` or `mintById`, the wrapper contract attempts to transfer assets from the caller and approve the vault for spending. With tokens like USDT, the `approve` function may fail when trying to approve from a non-zero allowance to another non-zero value, or the `transferFrom` may not return a boolean value, causing the transaction to revert unexpectedly.

Similar unsafe operations are found in:
- `SecuritizeVault::liquidate` - uses `IERC20Metadata(asset()).approve(address(redemption), assets)`
- `SecuritizeVaultV2::_liquidateTo` - uses `IERC20Metadata(asset()).approve(address(redemption), assets)`

These functions handle core protocol operations, including asset deposits, share minting, and liquidations, making them critical for normal protocol functionality.

**Impact:** Users may be unable to deposit assets or liquidate shares when using tokens with non-standard ERC20 implementations, leading to failed transactions and degraded user experience.

**Recommended Mitigation:** Replace all direct `IERC20` calls with `SafeERC20` equivalents. Add the SafeERC20 import to `RWASegWrap.sol` and update the unsafe operations:

```diff
// Add import to RWASegWrap.sol
+import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

contract RWASegWrap is ... {
+   using SafeERC20 for IERC20;

    function _pullAndApprove(address caller, uint256 assets, uint256 vaultId) internal {
        ISegregatedVault vault = ISegregatedVault(vaults[vaultId]);
-       bool success = IERC20(asset).transferFrom(caller, address(this), assets);
-       if (!success) {
-           revert AssetTransferFailed();
-       }
-       success = IERC20(asset).approve(address(vault), assets);
-       if (!success) {
-           revert AssetApprovalFailed();
-       }
+       IERC20(asset).safeTransferFrom(caller, address(this), assets);
+       IERC20(asset).forceApprove(address(vault), assets);
    }
}
```

For the SecuritizeVault contracts:

```diff
// In SecuritizeVault.liquidate
-IERC20Metadata(asset()).approve(address(redemption), assets);
+IERC20Metadata(asset()).forceApprove(address(redemption), assets);

// In SecuritizeVaultV2._liquidateTo
-bool success = IERC20Metadata(asset()).approve(address(redemption), assets);
-if (!success) {
-    revert AssetApprovalFailed();
-}
+IERC20Metadata(asset()).forceApprove(address(redemption), assets);
```

**Securitize:** Fixed in commit [b64b27](https://github.com/securitize-io/bc-rwa-seg-wrap-sc/commit/b64b2772c6584d9133763a1c128a32d2df9d5ff0).

**Cyfrin:** Verified.
