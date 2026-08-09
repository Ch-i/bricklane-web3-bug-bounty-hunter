---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2-0-1-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-12-17T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2-0
title: Inconsistent token amount in external redemption process of SecuritizeVault's
  liquidate function
vuln_class: []
---

# Inconsistent token amount in external redemption process of SecuritizeVault's liquidate function

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md)_

---

**Description:** In SecuritizeVault's liquidation process with external redemption, there's likely a mismatch between the actual received stable coins from the redemption contract and the amount calculated to send to the liquidator. The vault calculates the output amount using `navProvider.rate()` after the external redemption, but this calculated amount may differ from the actual stable coins received due to rounding discrepancies and rate variations during the redemption process.
```solidity
SecuritizeVault.sol
261:         if (address(0) != address(redemption)) {
262:             IERC20(asset()).approve(address(redemption), assets);
263:             redemption.redeem(assets);//@audit-info this sends underlying token to the redemption, receives stablecoin into this contract
264:             uint256 rate = navProvider.rate();
265:             uint256 decimalsFactor = 10 ** decimals();
266:             // after external redemption, vault gets liquidity to supply msg.sender (assets * nav)
267:             // liquidationToken === stableCoin
268:             liquidationToken.safeTransfer(msg.sender, assets.mulDiv(rate, decimalsFactor, Math.Rounding.Floor));//@audit-issue possible inconsistency in the amoutns. consider sending the balance delta instead
269:         }

```
**Impact:** Users either receive less stable coins than they should (value loss) or the transaction reverts due to insufficient balance when the calculated amount exceeds received tokens, making the liquidation functionality unreliable.

**Recommended Mitigation:** Track actual received stable coins from redemption contract and transfer them.
```solidity
    if (address(0) != address(redemption)) {
        IERC20 liquidityToken = IERC20(redemption.liquidity());
        uint256 balanceBefore = liquidityToken.balanceOf(address(this));
        redemption.redeem(assets);
        uint256 receivedAmount = liquidityToken.balanceOf(address(this)) - balanceBefore;
        liquidityToken.transfer(msg.sender, receivedAmount);
    }
```

**Securitize:** Fixed in commit [ef761a](https://bitbucket.org/securitize_dev/bc-securitize-vault-sc/commits/ef761a654b4015478c82cecd33cc54f7a97d37bb).

**Cyfrin:** Verified.
