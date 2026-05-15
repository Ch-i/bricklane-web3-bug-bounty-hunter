---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-18-cyfrin-securitize-redemptions-v2-0-1-2
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
title: Missing access control in `CollateralLiquidityProvider::setExternalCollateralRedemption`
vuln_class: []
---

# Missing access control in `CollateralLiquidityProvider::setExternalCollateralRedemption`

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-18-cyfrin-securitize-redemptions-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md)_

---

**Description:** The contract `CollateralLiquidityProvider` relies on `externalCollateralRedemption` to provide liquidity and this state variable can be changed via the function `setExternalCollateralRedemption()` as below.
```solidity
CollateralLiquidityProvider.sol
75:     function setExternalCollateralRedemption(address _externalCollateralRedemption) external override {//@audit-issue CRITICAL missing access control
76:         externalCollateralRedemption = IRedemption(_externalCollateralRedemption);
77:     }
```
Looking at the implementation, the function is not protected by any access control and anyone can change `externalCollateralRedemption` to whatever they want.
Note that with a malicious `externalCollateralRedemption`, it is possible to make the core function `supplyTo` useless.

**Impact:** We evaluate the impact to be HIGH because any attacker can change the core state variable `externalCollateralRedemption` as they want that can lead to various critical outcomes including permanent DoS.

**Recommended Mitigation:** Add a `onlyOwner` modifier to the function `setExternalCollateralRedemption()`.

**Securitize:** Fixed in commit [3977ca](https://bitbucket.org/securitize_dev/bc-redemption-sc/commits/3977ca8ffb259a01e8dab894745751cf2150abf4)

**Cyfrin:** Verified.



\clearpage
