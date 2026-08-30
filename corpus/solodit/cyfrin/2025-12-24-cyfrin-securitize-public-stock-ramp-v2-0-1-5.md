---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-1-5
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
title: Missing zero output validation in `SecuritizeAmmNavProvider` quote and buy
  functions
vuln_class: []
---

# Missing zero output validation in `SecuritizeAmmNavProvider` quote and buy functions

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** `SecuritizeAmmNavProvider::quoteBuyBase, quoteSellBase, executeBuyBase, executeSellBase` lack validation that output values are non-zero. Apart from issues already mentioned where rounding down to zero can occur, there are multiple other calculation points which can result in the final return values of these functions round down to zero:

**1. `baseOut` in buy operations:**
```solidity
baseOut = (amountInQuote * WAD) / rawExecPriceWad;
```

Rounds to zero when `amountInQuote < rawExecPriceWad / 1e18`. For example, if `rawExecPriceWad = 100e18` (100 quote per base), any `amountInQuote < 100` produces `baseOut = 0`.

**2. `quoteOut` in sell operations:**
```solidity
quoteOut = (amountInBase * rawExecPriceWad) / WAD;
```

Rounds to zero when `amountInBase * rawExecPriceWad < 1e18`. For example, if `rawExecPriceWad = 1e16` (0.01 quote per base), any `amountInBase < 100` produces `quoteOut = 0`.

**3. `execPrice` in both directions:**
```solidity
uint256 scaleDown = 10 ** (18 - d);
execPrice = rawExecPriceWad / scaleDown;
```

Rounds to zero when `rawExecPriceWad < scaleDown`. For a 6-decimal asset, `scaleDown = 1e12`, so any `rawExecPriceWad < 1e12` produces `execPrice = 0`.

These conditions can occur through:
- Small trade amounts relative to price
- Extreme price deviations from curve imbalance (as described in another issue)
- Low-decimal assets with unfavorable price scaling

**Impact:** When zero outputs are returned the potential negative outcomes include:

1. **Silent fund loss** — A router calling `executeBuyBase` or `executeSellBase` may transfer real tokens. The NAV provider returns `baseOut = 0` or `quoteOut = 0`, but the router may not distinguish this from a legitimate trade. In a worst-case scenario the user could send tokens and receive nothing, though this is unlikely.

2. **State corruption** — Virtual reserves update based on a trade that produced zero output:
```solidity
   baseReserves = newBase;
   quoteReserves = newQuote;
   k = newBase * newQuote;
```
The AMM state reflects input that was "absorbed" without corresponding output.

3. **Broken invariants** — The constant-product invariant assumes balanced input/output. Zero-output trades violate this assumption and skew future pricing.

4. **Misleading quotes** — The view functions `quoteBuyBase` and `quoteSellBase` return zero outputs without reverting, causing off-chain integrations to display incorrect expectations.

**Recommended Mitigation:** Add zero-output validation to all four functions:
```diff
function executeBuyBase(
    uint256 amountInQuote,
    uint256 anchorPriceWad,
    uint8 marketStatus
) external onlyRole(EXECUTOR_ROLE) returns (uint256 baseOut, uint256 execPrice) {
    // ... existing logic ...
    if (marketStatus == CLOSED_MARKET) {
        (baseOut, rawExecPriceWad) = _pricingFromCurveBuy(amountInQuote, curvePriceWad, anchorPriceWad);
    } else if (marketStatus == OPEN_MARKET) {
        rawExecPriceWad = anchorPriceWad;
        baseOut = (amountInQuote * WAD) / rawExecPriceWad;
    } else {
        revert("invalid market status");
    }

+   require(baseOut > 0, "baseOut=0");

    baseReserves = newBase;
    quoteReserves = newQuote;
    k = newBase * newQuote;

    _recordTrade(marketStatus, anchorPriceWad);

    uint8 d = asset.decimals();
    require(d <= 18, "decimals > 18");
    uint256 scaleDown = 10 ** (18 - d);

    execPrice = rawExecPriceWad / scaleDown;

+   require(execPrice > 0, "execPrice=0");

    emit ExecuteBuy(msg.sender, amountInQuote, baseOut, rawExecPriceWad);
}

function executeSellBase(
    uint256 amountInBase,
    uint256 anchorPriceWad,
    uint8 marketStatus
) external onlyRole(EXECUTOR_ROLE) returns (uint256 quoteOut, uint256 execPrice) {
    // ... existing logic ...
    if (marketStatus == CLOSED_MARKET) {
        (quoteOut, rawExecPriceWad) = _pricingFromCurveSell(amountInBase, curvePriceWad, anchorPriceWad);
    } else if (marketStatus == OPEN_MARKET) {
        rawExecPriceWad = anchorPriceWad;
        quoteOut = (amountInBase * rawExecPriceWad) / WAD;
    } else {
        revert("invalid market status");
    }

+   require(quoteOut > 0, "quoteOut=0");

    baseReserves = newBase;
    quoteReserves = newQuote;
    k = newBase * newQuote;

    _recordTrade(marketStatus, anchorPriceWad);

    uint8 d = asset.decimals();
    require(d <= 18, "decimals > 18");
    uint256 scaleDown = 10 ** (18 - d);

    execPrice = rawExecPriceWad / scaleDown;

+   require(execPrice > 0, "execPrice=0");

    emit ExecuteSell(msg.sender, amountInBase, quoteOut, rawExecPriceWad);
}

function quoteBuyBase(
    uint256 amountInQuote,
    uint256 anchorPriceWad,
    uint8 marketStatus
) external view returns (uint256 baseOut, uint256 execPrice) {
    // ... existing logic ...
+   require(baseOut > 0, "baseOut=0");

    execPrice = rawExecPriceWad / scaleDown;
+   require(execPrice > 0, "execPrice=0");
}

function quoteSellBase(
    uint256 amountInBase,
    uint256 anchorPriceWad,
    uint8 marketStatus
) external view returns (uint256 quoteOut, uint256 execPrice) {
    // ... existing logic ...
+   require(quoteOut > 0, "quoteOut=0");

    execPrice = rawExecPriceWad / scaleDown;
+   require(execPrice > 0, "execPrice=0");
}
```

**Securitize:** Fixed in commit [affb350](https://bitbucket.org/securitize_dev/bc-nav-provider-sc/commits/affb35097f9b638d6b1cfe4f58b42fdf79bc8778).

**Cyfrin:** Verified.
