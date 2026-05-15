---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-0-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: Zero `curvePriceWad` from rounding causes incorrect pricing or denial of service
vuln_class: []
---

# Zero `curvePriceWad` from rounding causes incorrect pricing or denial of service

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** The curve price calculation in `SecuritizeAmmNavProvider::_curveBuy` can round to zero when reserves become imbalanced:
```solidity
curvePriceWad = (amountInQuote * WAD) / deltaBase;
```

Mathematically, this simplifies to:
```solidity
curvePriceWad = WAD * (quoteReserves + amountInQuote) / baseReserves

// Proof of simplification:
// Step 1: Expand `deltaBase`
newQuote = Y + amountInQuote

newBase = k / newQuote
        = (X * Y) / (Y + amountInQuote)

deltaBase = X - newBase
          = X - (X * Y) / (Y + amountInQuote)

// Step 2: Find common denominator
deltaBase = X * (Y + amountInQuote) / (Y + amountInQuote) - (X * Y) / (Y + amountInQuote)
          = (X * Y + X * amountInQuote - X * Y) / (Y + amountInQuote)
          = (X * amountInQuote) / (Y + amountInQuote)

// Step 3: Substitute into curvePriceWad
curvePriceWad = (amountInQuote * WAD) / deltaBase
              = (amountInQuote * WAD) / [(X * amountInQuote) / (Y + amountInQuote)]
              = (amountInQuote * WAD) * (Y + amountInQuote) / (X * amountInQuote)
              = WAD * (Y + amountInQuote) / X

Since X = baseReserves, Y = quoteReserves therefore:
curvePriceWad = WAD * (quoteReserves + amountInQuote) / baseReserves
```

For `curvePriceWad` to round to zero:
```solidity
// WAD = 1e18 gives:
1e18 * (quoteReserves + amountInQuote) < baseReserves
```

This state is reachable through repeated sell operations which increase `baseReserves` while depleting `quoteReserves`. For example, if `quoteReserves = 1` and `amountInQuote = 1`, the condition becomes `baseReserves > 2e18`.

When `curvePriceWad` rounds down to zero and is subsequently passed to `_pricingFromCurveBuy`:
```solidity
uint256 r0Wad = (quoteBaseline * WAD) / baseBaseline;
uint256 mWad = (curvePriceWad * WAD) / r0Wad;  // @audit 0

uint256 baseExecPriceWad = (anchorPriceWad * mWad) / WAD;  // @audit 0

// @audit Since 0 < anchorPriceWad, enter the `else` statement:
uint256 diff = anchorPriceWad - baseExecPriceWad;  // @audit = anchorPriceWad
execPriceWad = anchorPriceWad - (diff / priceScaleFactor);

// @audit With default `priceScaleFactor = 2`:
execPriceWad = anchorPriceWad - anchorPriceWad/2 = anchorPriceWad/2

// With `priceScaleFactor = 1`:
execPriceWad = anchorPriceWad - anchorPriceWad = 0
baseOut = (amountInQuote * WAD) / execPriceWad;  // Division by zero → REVERT
```

The same issue exists in `_curveSell`:
```solidity
curvePriceWad = (deltaQuote * WAD) / amountInBase;
```

If `baseReserves` is small and `quoteReserves` is large (from repeated buys), a sell with large `amountInBase` produces tiny `deltaQuote`, rounding `curvePriceWad` to zero.

**Impact:** Two distinct failure modes depending on `priceScaleFactor`:

| Condition | Result |
|-----------|--------|
| `curvePriceWad = 0`, `scaleFactor ≥ 2` | Buyer receives tokens at ~50% of anchor price; seller receives ~50% premium |
| `curvePriceWad = 0`, `scaleFactor = 1` | Division by zero causes permanent DoS for affected trade direction |

A router contract relying on these prices would transfer incorrect token amounts, potentially causing loss of funds for liquidity providers or the protocol.

**Recommended Mitigation:** Add minimum curve price validation in both curve functions to protect against the case where `curvePriceWad` rounds down to zero:
```diff
function _curveBuy(uint256 amountInQuote) internal view initialized returns (uint256 curvePriceWad, uint256 newBase, uint256 newQuote) {
    require(amountInQuote > 0, "amountInQuote=0");

    uint256 X = baseReserves;
    uint256 Y = quoteReserves;
    uint256 kLocal = k;

    newQuote = Y + amountInQuote;
    newBase = kLocal / newQuote;

    uint256 deltaBase = X - newBase;
    require(deltaBase > 0, "deltaBase=0");

    curvePriceWad = (amountInQuote * WAD) / deltaBase;
+   require(curvePriceWad > 0, "curvePriceWad=0");
}

function _curveSell(uint256 amountInBase) internal view initialized returns (uint256 curvePriceWad, uint256 newBase, uint256 newQuote) {
    require(amountInBase > 0, "amountInBase=0");

    uint256 X = baseReserves;
    uint256 Y = quoteReserves;
    uint256 kLocal = k;

    newBase = X + amountInBase;
    newQuote = kLocal / newBase;

    uint256 deltaQuote = Y - newQuote;
    require(deltaQuote > 0, "deltaQuote=0");

    curvePriceWad = (deltaQuote * WAD) / amountInBase;
+   require(curvePriceWad > 0, "curvePriceWad=0");
}
```

Additionally, consider enforcing a minimum `priceScaleFactor` of 2 to prevent division-by-zero in the pricing functions:
```solidity
function setPriceScaleFactor(uint256 newScaleFactor) external onlyRole(DEFAULT_ADMIN_ROLE) {
-   require(newScaleFactor > 0, "scaleFactor = 0");
+   require(newScaleFactor >= 2, "scaleFactor must be >= 2");

    uint256 oldScaleFactor = priceScaleFactor;
    priceScaleFactor = newScaleFactor;

    emit PriceScaleFactorUpdated(oldScaleFactor, newScaleFactor);
}
```

**Securitize:** Fixed in commit [bcd6e87](https://bitbucket.org/securitize_dev/bc-nav-provider-sc/commits/bcd6e87a866f83ed33b468b9dd2acebac9eca1fd).

**Cyfrin:** Verified.
