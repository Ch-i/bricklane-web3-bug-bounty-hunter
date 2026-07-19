---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-1-4
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
title: '`SecuritizeAmmNavProvider` virtual reserve rounding erosion can lead to denial
  of service'
vuln_class: []
---

# `SecuritizeAmmNavProvider` virtual reserve rounding erosion can lead to denial of service

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** The virtual AMM's constant-product math erodes `k` through integer division truncation on every trade:
```solidity
// In `_curveBuy`:
newQuote = Y + amountInQuote;
newBase = kLocal / newQuote;  // Rounds down

// After trade execution:
baseReserves = newBase;
quoteReserves = newQuote;
k = newBase * newQuote;  // New k ≤ old k due to truncation
```

Each trade can lose up to `(denominator - 1)` from k. Over many trades, `baseReserves` (or `quoteReserves` for sells) progressively decreases.

The `_checkAndResetBaseline` function can accelerate this by locking in depleted reserves when market status changes from OPEN → CLOSED:
```solidity
if (shouldReset) {
    uint256 newBase = baseReserves;  // Uses current depleted value
    uint256 newQuote = (newBase * anchorPriceWad) / WAD;
    _resetBaseline(newBase, newQuote);  // k = newBase * newQuote (tiny)
}
```

Once k becomes sufficiently small, a single trade can round reserves to zero:
```solidity
// If k = 1, quoteReserves = 1, and amountInQuote = 2:
newQuote = 1 + 2 = 3;
newBase = 1 / 3 = 0;  // Rounds to zero

// Trade completes (deltaBase = 1 passes the check), then:
baseReserves = 0;
k = 0 * 3 = 0;
```

All subsequent trades revert at the `initialized` modifier:
```solidity
modifier initialized() {
    require(baseReserves > 0 && quoteReserves > 0, "uninitialized");
    // ...
}
```

**Impact:** Denial of service for all trade execution until admin manually calls `resetBaseline` to restore valid reserves.

**Recommended Mitigation:** Add minimum reserve thresholds to prevent reserves from falling into the danger zone. This could be done using new admin-configurable storage slots and should be based on the decimals of the `asset`:
```diff
+ uint256 public minReserves;

function initialize(uint256 _baseReserves, uint256 _quoteReserves, address _asset) public onlyProxy initializer {
    // ... existing checks ...

    asset = IERC20Metadata(_asset);
+   uint8 d = asset.decimals();
+   uint256 minReservesTemp = 10 ** d;  // 1 whole token minimum

+   require(_baseReserves >= minReservesTemp, "baseReserves too small");
+   require(_quoteReserves >= minReservesTemp, "quoteReserves too small");
+   minReserves = minReservesTemp;

    // ... rest of initialization
}

function _resetBaseline(uint256 newBase, uint256 newQuote) internal {
    require(newBase > 0, "newBase=0");
    require(newQuote > 0, "newQuote=0");

+   uint256 minReservesCache = minReserves;
+   require(newBase >= minReservesCache, "newBase too small");
+   require(newQuote >= minReservesCache, "newQuote too small");

    // ... rest of function
}

function _curveBuy(uint256 amountInQuote) internal view initialized returns (uint256 curvePriceWad, uint256 newBase, uint256 newQuote) {
    require(amountInQuote > 0, "amountInQuote=0");

    uint256 X = baseReserves;
    uint256 Y = quoteReserves;
    uint256 kLocal = k;

    newQuote = Y + amountInQuote;
    newBase = kLocal / newQuote;

+   require(newBase >= minReserves, "base reserves too low");

    uint256 deltaBase = X - newBase;
    require(deltaBase > 0, "deltaBase=0");

    curvePriceWad = (amountInQuote * WAD) / deltaBase;
}

function _curveSell(uint256 amountInBase) internal view initialized returns (uint256 curvePriceWad, uint256 newBase, uint256 newQuote) {
    require(amountInBase > 0, "amountInBase=0");

    uint256 X = baseReserves;
    uint256 Y = quoteReserves;
    uint256 kLocal = k;

    newBase = X + amountInBase;
    newQuote = kLocal / newBase;

+   require(newQuote >= minReserves, "quote reserves too low");

    uint256 deltaQuote = Y - newQuote;
    require(deltaQuote > 0, "deltaQuote=0");

    curvePriceWad = (deltaQuote * WAD) / amountInBase;
}
```

Another benefit of enforcing minimum reserves is a consistent pattern of high-profile mainnet hacks have involved attackers manipulating pool reserves to very low wei amounts; enforcing minimum reserves acts as defensive programming technique helping to reduce the attack surface available to hackers.

**Securitize:** Fixed in commit [1919a89](https://bitbucket.org/securitize_dev/bc-nav-provider-sc/commits/1919a8993ec7e0cd9f1931b4bb02ec622321c0fe).

**Cyfrin:** Verified.
