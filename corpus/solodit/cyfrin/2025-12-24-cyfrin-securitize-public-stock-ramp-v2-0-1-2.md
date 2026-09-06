---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-1-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: Lack of Price Feed Update Function in `RedStoneNavProvider`
vuln_class: []
---

# Lack of Price Feed Update Function in `RedStoneNavProvider`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** The `RedStoneNavProvider` contract sets the RedStone price feed address during initialization but provides no mechanism to update it afterwards. The priceFeed is set once in the `RedStoneNavProvider::initialize` function and becomes immutable for the lifetime of the contract:

```solidity
function initialize(address _priceFeed, address _asset) public onlyProxy initializer {
        __BaseDSContract_init();
        priceFeed = IPriceFeed(_priceFeed);
        asset = IERC20Metadata(_asset);
    }
```
The contract declares the `priceFeed` as a public state variable but offers no admin function to update it, f the RedStone oracle address needs to be changed due to:
* Oracle migration to a new address
* Oracle deprecation or compromise
* Need to switch to a different price feed
* Oracle upgrade or maintenance

The only solution is to:
1. Deploy a new `RedStoneNavProvider` contract with the new feed address
2. Call `updateNavProvider()` on all `OnRamp/OffRamp` contracts using this provider
3. Potentially requiring governance votes or multi-sig operations

**Impact:** Requires complete contract redeployment instead of a simple parameter update in case of the `priceFeed` need to be changed.

**Recommended Mitigation:** Add an admin-controlled function to update the price feed address.

**Securitize:** Fixed in commit [4146a77](https://bitbucket.org/securitize_dev/bc-nav-provider-sc/commits/4146a77b4e5d3a72e67f164ef6e1ca3a12c99657).

**Cyfrin:** Verified.
