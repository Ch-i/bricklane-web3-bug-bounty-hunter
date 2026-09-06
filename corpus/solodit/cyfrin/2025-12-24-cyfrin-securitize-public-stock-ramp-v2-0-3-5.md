---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-3-5
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: Cache required storage slots in top-level functions then pass cached values
  to child functions
vuln_class: []
---

# Cache required storage slots in top-level functions then pass cached values to child functions

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** A common pattern of inefficiency is when parent functions read certain storage slots, then call child functions (which can themselves call other child functions), and the child functions re-read the same storage slots even though it isn't possible for their values to have changed.

In such cases it is much more efficient for the parent functions to cache the required storage slots once, then pass them as input to child functions:

* `AllowanceLiquidityProvider::supplyTo` - cache `liquidityToken, liquidityProviderWallet`, pass as inputs to `_availableLiquidity`
* `CollateralLiquidityProvider::supplyTo` cache `externalCollateralRedemption, collateralToken, collateralProvider`, pass as inputs to `_availableLiquidity, _liquidityTokenToExternalCollateralToken`
* `SecuritizeOnRamp::subscribe` cache `liquidityToken` pass as inputs to `calculateDsTokenAmount, _executeLiquidityTransfer`
* `SecuritizeOffRamp::redeem` cache `liquidityProvider` pass as input to `_redeem` then use to emit `RedemptionCompleted` event

**Securitize:** Acknowledged for now to avoid a big internal functions refactor.
