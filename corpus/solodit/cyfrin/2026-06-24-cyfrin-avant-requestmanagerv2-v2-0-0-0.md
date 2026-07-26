---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-24-cyfrin-avant-requestmanagerv2-v2-0-0-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-06-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-24-cyfrin-avant-requestmanagerv2-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-24-cyfrin-avant-requestmanagerv2-v2-0
title: Missing input validation in admin setters across `PriceStorage, RequestsManagerV2`
vuln_class: []
---

# Missing input validation in admin setters across `PriceStorage, RequestsManagerV2`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-24-cyfrin-avant-requestmanagerv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-24-cyfrin-avant-requestmanagerv2-v2.0.md)_

---

**Description:** Several admin-only setters validate only a trivial degenerate input and accept other values that are syntactically valid but break pricing or settlement. Each is independently low-severity (admin recovers by re-calling the setter), but they share one root cause: the accepted input domain is wider than the safe domain.

1. **`PriceStorage::setLowerBoundPercentage, setUpperBoundPercentage`** accept any value in `(0, 1e18]`, with neither a sane floor nor a sane cap.

   Both setters reject only `0` and values strictly greater than `BOUND_PERCENTAGE_DENOMINATOR` (1e18) (`src/PriceStorage.sol:56-72`). The per-update bounds in `setPrice` are computed as `lastPriceValue +/- lastPriceValue * percentage / 1e18` (`src/PriceStorage.sol:38-44`). At the high end, a bound at or near `1e18` drives the lower bound to `0`, so a single `setPrice` can crash the price to 1 wei and the next `completeMint` mints a vastly inflated amount.

   At the low end, a percentage small enough that the band `lastPriceValue * percentage / 1e18` rounds down to zero (or, at the canonical `1e18` price scale, to a ~1-wei width that rejects every realistic update) collapses the band to `upperBound == lowerBound == lastPriceValue`; every genuine price change then reverts `InvalidPriceRange`.

   Because the per-update band check is computed from `lastPrice` and applies to every key, even a fresh key cannot publish a value outside the band (write-once-per-key at `src/PriceStorage.sol:34` only blocks overwriting an existing key), so the oracle is frozen until the admin widens the bound.

2. **`RequestsManagerV2::setTreasury`** and the constructor accept the self-address `address(this)`.

   Both validate only that the treasury is non-zero (`src/RequestsManagerV2.sol:139-143`, constructor at `src/RequestsManagerV2.sol:113`); neither rejects `address(this)`.

   With `treasuryAddress == address(this)`, the `completeMint` deposit forward becomes a self-transfer no-op that commingles deposits with escrow (`src/RequestsManagerV2.sol:298`), and `completeBurn` requires a self-allowance that is normally absent, so every burn settlement reverts on `safeTransferFrom` (`src/RequestsManagerV2.sol:425`) until the treasury is re-pointed.

**Recommended Mitigation:**
- `PriceStorage::setLowerBoundPercentage, setUpperBoundPercentage`: bound each percentage within a sane closed band rather than `(0, 1e18]` - enforce both a floor large enough that the per-update band cannot round down to a sub-update width at the protocol's price scale, and a cap materially below `1e18` (e.g. `0.5e18`) consistent with the intended 5% / 33% regime. `initialize` routes through these setters, so the fix covers initialization.

- `RequestsManagerV2::setTreasury` and constructor: reject `address(this)` in addition to the existing non-zero check (e.g. revert when `_treasuryAddress == address(this)`).

**Avant:** Acknowledged; `PriceStorage` is pre-exisiting and deployed immutably but we will note this for future deployments. `RequestsManagerV2::setTreasury` we accept as a deployment-time admin responsibility.

\clearpage
