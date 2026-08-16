---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-3-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: Cache storage to prevent identical storage reads
vuln_class: []
---

# Cache storage to prevent identical storage reads

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** Reading from storage is expensive, cache storage to prevent identical storage reads:

* `SecuritizeAmmNavProvider::_pricingFromCurveBuy, _pricingFromCurveSell` - cache `priceScaleFactor`
* `SecuritizeAmmNavProvider::_checkAndResetBaseline` - cache `lastAnchorPriceWad, lastMarketStatus` prior to first `if` statement
* `AllowanceLiquidityProvider::_availableLiquidity` - cache `liquidityToken, liquidityProviderWallet`
* `BaseOffRamp::_redeem` - cache `asset`
* `BaseOnRamp::_executeLiquidityTransfer` - cache `liquidityToken, feeManager, bridgeChainId, USDCBridge`

**Securitize:** Fixed in commits [e631361](https://bitbucket.org/securitize_dev/bc-nav-provider-sc/commits/e631361371ccaabceabd8ba1a200f4fd1200e54f), [ea883b9](https://github.com/securitize-io/bc-on-off-ramp-sc/commit/ea883b99af2eb802ffe49c7338379b1e31cd76de), [d32d6a0](https://bitbucket.org/securitize_dev/bc-nav-provider-sc/commits/d32d6a0d6cf9a4215360deb11711740450d1db48).

**Cyfrin:** Verified.
