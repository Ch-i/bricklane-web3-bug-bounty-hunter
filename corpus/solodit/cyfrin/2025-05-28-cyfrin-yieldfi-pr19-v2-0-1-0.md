---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-28-cyfrin-yieldfi-pr19-v2-0-1-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-05-28T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-28-cyfrin-yieldfi_pr19-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-28-cyfrin-yieldfi-pr19-v2-0
title: Avoid unnecessary computation in `dYToken::mintYToken` when `isNewYToken ==
  false`
vuln_class: []
---

# Avoid unnecessary computation in `dYToken::mintYToken` when `isNewYToken == false`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-28-cyfrin-yieldfi_pr19-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-28-cyfrin-yieldfi_pr19-v2.0.md)_

---

**Description:** In the new [`dYToken::mintYToken`](https://github.com/YieldFiLabs/contracts/blob/702a931df3adb2f6e48807203cdc7a92604ea249/contracts/core/tokens/dYTokenL1.sol#L67-L81), there is special logic for handling newly minted `dYTokens`, i.e., tokens generated through deposits or accrued fees:

```solidity
function mintYToken(address to, uint256 shares, bool isNewYToken) external override {
    require(msg.sender == manager, "!manager");
    uint256 assets = convertToAssets(shares);

    // if isNewYToken i.e external deposit has triggered minting of dyToken, we mint yToken to this contract
    if(isNewYToken) {
        // corresponding shares of yToken based on assets
        uint256 yShares = YToken(yToken).convertToShares(assets);
        // can pass isNewYToken here as it is not used in yToken
        ManageAssetAndShares memory manageAssetAndShares = ManageAssetAndShares({
            yToken: yToken,
            shares: yShares,
            assetAmount: assets,
            updateAsset: true,
            isMint: true,
            isNewYToken: isNewYToken
        });
        IManager(manager).manageAssetAndShares(address(this), manageAssetAndShares);
    }
    // minting dYToken to receiver
    _mint(to, shares);
}
```

The `assets` variable is only used within the `if (isNewYToken)` block. Moving its declaration inside the block would save gas when `isNewYToken == false`, by avoiding unnecessary computation:

```diff
function mintYToken(address to, uint256 shares, bool isNewYToken) external override {
    require(msg.sender == manager, "!manager");
-   uint256 assets = convertToAssets(shares);

    // if isNewYToken i.e external deposit has triggered minting of dyToken, we mint yToken to this contract
    if(isNewYToken) {
+       uint256 assets = convertToAssets(shares);
        // corresponding shares of yToken based on assets
        uint256 yShares = YToken(yToken).convertToShares(assets);
```

**YieldFi:** Fixed in commit [`f1f6996`](https://github.com/YieldFiLabs/contracts/commit/f1f69960c4d6d84aa8fe7658ac535a79fb77f505)

**Cyfrin:** Verified. `convertToAssets` now moved inside the if-statmement.

\clearpage
