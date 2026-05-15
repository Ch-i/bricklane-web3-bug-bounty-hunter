---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-18-cyfrin-securitize-redemptions-v2-0-1-1
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
title: Missing access control in `CollateralLiquidityProvider::setCollateralProvider`
vuln_class: []
---

# Missing access control in `CollateralLiquidityProvider::setCollateralProvider`

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-18-cyfrin-securitize-redemptions-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md)_

---

**Description:** The contract `CollateralLiquidityProvider` relies on `collateralProvider` to pull the collateral and process redemption in liquidity token. This state variable can be changed via the function `setCollateralProvider()` as below.
```solidity
CollateralLiquidityProvider.sol
79:     function setCollateralProvider(address _collateralProvider) external {//@audit-issue CRITICAL missing access control
80:         collateralProvider = _collateralProvider;
81:     }
```
Looking at the implementation, the function is not protected by any access control and anyone can change `collateralProvider ` to whatever they want.
Note that with a malicious `collateralProvider `, it is possible to make the function `availableLiquidity` to return zero all the time.

**Impact:** We evaluate the impact to be HIGH because any attacker can change the core state variable `collateralProvider ` as they want that can lead to various critical outcomes including permanent DoS.

**Recommended Mitigation:** Add a `onlyOwner` modifier to the function `setCollateralProvider()`.

**Securitize:** Fixed in commit [3977ca](https://bitbucket.org/securitize_dev/bc-redemption-sc/commits/3977ca8ffb259a01e8dab894745751cf2150abf4)

**Cyfrin:** Verified.
