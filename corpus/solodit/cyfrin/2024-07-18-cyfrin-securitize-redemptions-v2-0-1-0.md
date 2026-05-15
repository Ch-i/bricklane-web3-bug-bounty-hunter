---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-18-cyfrin-securitize-redemptions-v2-0-1-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-07-18T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-18-cyfrin-securitize-redemptions-v2-0
title: Wrong validation on the `availableLiquidity` in function `SecuritizeRedemption::redeem()`
vuln_class: []
---

# Wrong validation on the `availableLiquidity` in function `SecuritizeRedemption::redeem()`

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-18-cyfrin-securitize-redemptions-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md)_

---

**Description:** The function `SecuritizeRedemption::redeem(uint256 _amount)` is supposed to be used by investors to be able to redeem their assets (DSToken) for liquidity (stable coin). The parameter `_amount` is the amount of asset that the caller wants to redeem.
```solidity
SecuritizeRedemption.sol
77:     function redeem(uint256 _amount) whenNotPaused external override {
78:         uint256 rate = navProvider.rate();
79:         require(rate != 0, "Rate should be defined");
80:         require(asset.balanceOf(msg.sender) >= _amount, "Redeemer has not enough balance");
81:         require(address(liquidityProvider) != address(0), "Liquidity provider should be defined");
82:         require(liquidityProvider.availableLiquidity() >= _amount, "Not enough liquidity");//@audit-issue WRONG
83:
84:         ERC20 stableCoin = ERC20(address(liquidityProvider.liquidityToken()));
85:         uint256 liquidity = _amount * rate / (10 ** stableCoin.decimals());
86:
87:         liquidityProvider.supplyTo(msg.sender, liquidity);
88:         asset.transferFrom(msg.sender, liquidityProvider.recipient(), _amount);
89:
90:         emit RedemptionCompleted(msg.sender, _amount, liquidity, rate);
91:     }
```
Looking at the implementation, there is a line to check if the `liquidityProvider` has enough liquidity.
But it is checking against a wrong value `_amount` that is in fact the amount of asset, not liquidity.
Instead, it must be checked against the `liquidity` value that is calculated afterwards at L85.
This wrong check can lead to a situation where the check passes while the actual `availableLiquidity()` is less than required (if the rate is greater than 1) or the check fails while there are enough liquidity available (if the rate is less than 1).
The second case is more severe than the former one.

**Impact:** We evaluate the risk to be HIGH because the redemption will fail most of the time when the rate is much less than 1 and there is a difference in the number of decimals for asset and liquidity tokens.

**Recommended Mitigation:** Move the validation below the calculation of required liquidity and fix it to compare with a correct value.

**Securitize:** Fixed in commit [3977ca](https://bitbucket.org/securitize_dev/bc-redemption-sc/commits/3977ca8ffb259a01e8dab894745751cf2150abf4)

**Cyfrin:** Verified.
