---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2-3-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-08-04T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md
tags:
- firm:cyfrin
- report:2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2
title: Gas inefficient approval pattern in liquidation function leads to unnecessary
  gas consumption
vuln_class: []
---

# Gas inefficient approval pattern in liquidation function leads to unnecessary gas consumption

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md)_

---

**Description:** The `SecuritizeVaultV2::_liquidateTo` function performs an approval operation to the redemption contract on every liquidation call when a redemption contract is configured. On line 489, the function calls `IERC20Metadata(asset()).approve(address(redemption), assets)` for each liquidation operation, approving only the exact amount of assets to be redeemed.

This approach is gas inefficient because:

1. **Repetitive SSTORE operations**: Each `approve` call requires an expensive SSTORE operation to update the allowance mapping
2. **Fixed redemption contract**: The redemption contract is set during initialization and cannot be changed afterward, making it safe to grant a permanent approval

The current implementation unnecessarily consumes gas on every liquidation when a more efficient approach would be to grant `type(uint256).max` approval to the redemption contract during initialization.

**Impact:** Every liquidation operation consumes additional gas due to redundant approval calls, increasing transaction costs for users performing liquidations.

**Recommended Mitigation:** Grant maximum approval to the redemption contract during initialization instead of approving on each liquidation:

```diff
function _initialize(
    string memory _name,
    string memory _symbol,
    address _securitizeToken,
    address _redemptionAddress,
    address _liquidationToken,
    address _navProvider
) private {
    // ... existing initialization logic ...

    redemption = ISecuritizeOffRamp(_redemptionAddress);
    liquidationToken = IERC20Metadata(_liquidationToken);
    navProvider = ISecuritizeNavProvider(_navProvider);

+   // Grant maximum approval to redemption contract if it exists
+   if (address(redemption) != address(0)) {
+       bool success = IERC20Metadata(_securitizeToken).approve(address(redemption), type(uint256).max);
+       if (!success) {
+           revert AssetApprovalFailed();
+       }
+   }

    _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
}

function _liquidateTo(address to, uint256 shares) internal {
    if (balanceOf(to) < shares) {
        revert NotEnoughShares();
    }
    uint256 assets = convertToAssets(shares);
    _burn(to, shares);

    emit Liquidate(to, assets, shares);

    if (address(0) != address(redemption)) {
-       bool success = IERC20Metadata(asset()).approve(address(redemption), assets);
-       if (!success) {
-           revert AssetApprovalFailed();
-       }
        uint256 balanceBefore = liquidationToken.balanceOf(address(this));
        redemption.redeem(assets, 0);
        uint256 receivedAmount = liquidationToken.balanceOf(address(this)) - balanceBefore;
        liquidationToken.safeTransfer(to, receivedAmount);
    } else {
        liquidationToken.safeTransfer(to, assets);
    }
}
```
**Securitize:** Acknowledged.

**Cyfrin:** Acknowledged.

\clearpage
