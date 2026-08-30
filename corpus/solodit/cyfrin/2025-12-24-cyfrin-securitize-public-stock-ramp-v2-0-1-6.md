---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-1-6
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: '`RedStoneNavProvider::rate` can return zero for non-zero oracle input due
  to rounding in `Helper::normalizeRate`'
vuln_class: []
---

# `RedStoneNavProvider::rate` can return zero for non-zero oracle input due to rounding in `Helper::normalizeRate`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** In `RedStoneNavProvider::rate`, the zero check validates the raw oracle value but not the normalized result:
```solidity
function rate() external view override returns (uint256) {
    uint8 oracleDecimals = priceFeed.decimals();
    uint8 assetDecimals = asset.decimals();
    int256 rsRate = priceFeed.latestAnswer();
    require(rsRate != 0, 'Rate must not be zero');  // @audit Checks raw value only

    // @audit normalized rate never zero checked
    return Helper.normalizeRate(uint256(rsRate), oracleDecimals, assetDecimals);
}
```

The `Helper::normalizeRate` function divides when `fromDecimals > toDecimals`:
```solidity
function normalizeRate(uint256 value, uint8 fromDecimals, uint8 toDecimals) internal pure returns (uint256) {
    if (fromDecimals == toDecimals) {
        return value;
    } else if (fromDecimals > toDecimals) {
        return value / (10**(fromDecimals - toDecimals));  // @audit Can round to zero
    } else {
        return value * (10**(toDecimals - fromDecimals));
    }
}
```

When the raw oracle value is smaller than the divisor, integer division truncates to zero:
```solidity
oracleDecimals = 18 (common for RedStone)
assetDecimals = 6 (like USDC)
rsRate = 5e11 (passes the != 0 check)
divisor = 10^(18 - 6) = 1e12
normalizedRate = 5e11 / 1e12 = 0
```

The `require(rsRate != 0)` passes because `5e11 != 0`, but the function returns `0`.

This could occur with:
- Severely devalued assets approaching zero value
- Misconfigured oracle/asset decimal pairing
- Oracle malfunction returning unexpectedly small values
- Exotic assets with very low unit prices

**Impact:** Any protocol consuming `RedStoneNavProvider::rate` receives zero, potentially causing a number of errors if the protocol doesn't revert such as:
- Incorrect NAV calculations valuing assets at zero
- Potential division-by-zero errors in downstream calculations
- Users trading at incorrect prices, either losing funds or extracting value from the protocol

**Recommended Mitigation:** Add a zero check on the normalized result:
```solidity
function rate() external view override returns (uint256 normalizedRate) {
    uint8 oracleDecimals = priceFeed.decimals();
    uint8 assetDecimals = asset.decimals();
    int256 rsRate = priceFeed.latestAnswer();
    require(rsRate > 0, 'Rate must be positive');

    normalizedRate = Helper.normalizeRate(uint256(rsRate), oracleDecimals, assetDecimals);
    require(normalizedRate > 0, 'Normalized rate is zero');
}
```

**Securitize:** Fixed in commit [f4bed90](https://bitbucket.org/securitize_dev/bc-nav-provider-sc/commits/f4bed908104433d41035215a5315718dcc5669a9).

**Cyfrin:** Verified.
