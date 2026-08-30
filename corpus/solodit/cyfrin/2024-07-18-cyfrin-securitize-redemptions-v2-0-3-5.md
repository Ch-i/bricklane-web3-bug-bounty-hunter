---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-18-cyfrin-securitize-redemptions-v2-0-3-5
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-07-18T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-18-cyfrin-securitize-redemptions-v2-0
title: Missing input validation in `CollateralLiquidityProvider::setExternalCollateralRedemption`
vuln_class: []
---

# Missing input validation in `CollateralLiquidityProvider::setExternalCollateralRedemption`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-18-cyfrin-securitize-redemptions-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md)_

---

**Description:** _Note that this finding assumes the other finding about access control is mitigated_.
The contract `CollateralLiquidityProvider` relies on `externalCollateralRedemption` to process redemption.
The function `supplyTo()`  is the core function of this contract.
```solidity
CollateralLiquidityProvider.sol
61:     function supplyTo(address _redeemer, uint256 _amount) whenNotPaused onlySecuritizeRedemption public override {
62:         //take collateral funds from collateral provider
63:         IERC20(externalCollateralRedemption.asset()).transferFrom(collateralProvider, address(this), _amount);
64:
65:         //approve external redemption
66:         IERC20(externalCollateralRedemption.asset()).approve(address(externalCollateralRedemption), _amount);
67:
68:         //get liquidity
69:         externalCollateralRedemption.redeem(_amount);
70:
71:         //supply _redeemer
72:         liquidityToken.transfer(_redeemer, _amount);
73:     }
```
Looking at the L69 with L72, the function is assuming that `liquidityToken = externalCollateralRedemption.liquidity`.
But this is not validated in the function `setExternalCollateralRedemption` and there is a risk to cause an inconsistency.

**Impact:** We evaluate the impact to be LOW assuming the function will be protected by a proper access control mitigating the other finding.

**Recommended Mitigation:** Validate that `liquidityToken = externalCollateralRedemption.liquidity` in the function `setExternalCollateralRedemption()`.

**Securitize:** Fixed in commit [3977ca](https://bitbucket.org/securitize_dev/bc-redemption-sc/commits/3977ca8ffb259a01e8dab894745751cf2150abf4)

**Cyfrin:** Verified.

\clearpage
