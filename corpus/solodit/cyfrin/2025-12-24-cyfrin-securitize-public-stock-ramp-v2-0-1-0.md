---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-1-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: '`RedStoneNavProvider::rate` will return massively inflated value if underlying
  oracle returns a negative value and lacks common oracle validations'
vuln_class: []
---

# `RedStoneNavProvider::rate` will return massively inflated value if underlying oracle returns a negative value and lacks common oracle validations

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** `RedStoneNavProvider::rate` has an underlying oracle price feed which returns an `int256`, then performs an unsafe cast to `uint256`:
```solidity
int256 rsRate = priceFeed.latestAnswer();
require(rsRate != 0, 'Rate must not be zero');
return Helper.normalizeRate(uint256(rsRate), oracleDecimals, assetDecimals);
```

**Impact:** If the underlying oracle returned a negative number, performing an unsafe cast to `uint256` will return an absurdly high rate.

**Recommended Mitigation:** Enforce that the rate returned by the underlying oracle must be greater than zero:
```diff
    function rate() external view override returns (uint256) {
        uint8 oracleDecimals = priceFeed.decimals();
        uint8 assetDecimals = asset.decimals();
        int256 rsRate = priceFeed.latestAnswer();
-       require(rsRate != 0, 'Rate must not be zero');
+       require(rsRate > 0, 'Rate must be greater than zero');
        return Helper.normalizeRate(uint256(rsRate), oracleDecimals, assetDecimals);
    }
```

Also consider adding other common oracle-related checks such as:
* staleness
* min/max price thresholds

**Securitize:** Fixed in commit [ec23faf](https://bitbucket.org/securitize_dev/bc-nav-provider-sc/commits/ec23faf7f773b7a42229cb5f7f6ae3dd51a07772).

**Cyfrin:** Verified.
