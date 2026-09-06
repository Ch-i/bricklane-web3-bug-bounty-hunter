---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-11-cyfrin-strata-v2-1-3-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-06-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-11-cyfrin-strata-v2-1
title: Use explicit sizes instead of `uint`
vuln_class: []
---

# Use explicit sizes instead of `uint`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-11-cyfrin-strata-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md)_

---

**Description:** While `uint` defaults to `uint256`, it is considered good practice to use the explicit types including the size and to avoid using `uint`:
```solidity
predeposit/yUSDeDepositor.sol
65:        uint beforeAmount = asset.balanceOf(address(this));
73:        uint pUSDeShares = pUSDeDepositor.deposit(asset, amount, address(this));

predeposit/MetaVault.sol
53:        uint baseAssets = IERC4626(token).previewRedeem(tokenAssets);
54:        uint shares = previewDeposit(baseAssets);
70:        uint baseAssets = previewMint(shares);
71:        uint tokenAssets = IERC4626(token).previewWithdraw(baseAssets);
211:        uint balance = IERC20(vaultAddress).balanceOf(address(this));
219:        uint length = assetsArr.length;
220:        for (uint i = 0; i < length; i++) {
240:    function redeemRequiredBaseAssets (uint baseTokens) internal {
241:        for (uint i = 0; i < assetsArr.length; i++) {
243:            uint totalBaseTokens = vault.previewRedeem(vault.balanceOf(address(this)));

predeposit/pUSDeVault.sol
62:            uint total_sUSDe = sUSDe.balanceOf(address(this));
63:            uint total_USDe = sUSDe.previewRedeem(total_sUSDe);
65:            uint total_yield_USDe = total_USDe - Math.min(total_USDe, depositedBase);
67:            uint y_pUSDeShares = balanceOf(caller);
68:            uint caller_yield_USDe = total_yield_USDe.mulDiv(shares, y_pUSDeShares, Math.Rounding.Floor);
121:            uint sUSDeAssets = sUSDe.previewWithdraw(assets);
138:        uint USDeBalance = USDe.balanceOf(address(this));
171:        uint USDeBalance = USDe.balanceOf(address(this));

predeposit/yUSDeVault.sol
38:        uint pUSDeAssets = super.totalAssets();
39:        uint USDeAssets = _convertAssetsToUSDe(pUSDeAssets, true);
43:    function _convertAssetsToUSDe (uint pUSDeAssets, bool withYield) internal view returns (uint256) {
44:        uint sUSDeAssets = pUSDeVault.previewRedeem(withYield ? address(this) : address(0), pUSDeAssets);
45:        uint USDeAssets = sUSDe.previewRedeem(sUSDeAssets);
59:        uint underlyingUSDe = _convertAssetsToUSDe(pUSDeAssets, false);
60:        uint yUSDeShares = _valueMulDiv(underlyingUSDe, totalAssets(), totalAccruedUSDe(), Math.Rounding.Floor);
74:        uint underlyingUSDe = _valueMulDiv(yUSDeShares, totalAccruedUSDe(), totalAssets(), Math.Rounding.Ceil);
75:        uint pUSDeAssets = pUSDeVault.previewDeposit(underlyingUSDe);

```

**Strata:** Fixed in commit [61f5910](https://github.com/Strata-Money/contracts/commit/61f591088754e2666355307cf1e11e6440af8572).

**Cyfrin:** Verified.
