---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-08-cyfrin-strata-tranches-v2-0-3-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-10-08T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-08-cyfrin-strata-tranches-v2-0
title: Inconsistent APR boundary validation between `AprPairFeed` and `Accounting`
vuln_class: []
---

# Inconsistent APR boundary validation between `AprPairFeed` and `Accounting`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-08-cyfrin-strata-tranches-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md)_

---

**Description:** There is a mismatch between APR boundary validation constants in `AprPairFeed` and `Accounting` contracts. The `AprPairFeed` accepts negative APRs down to -50%, but the `Accounting` contract rejects any negative APR values, thus data deemed valid by the oracle is rejected during normalization.

```solidity

// AprPairFeed
int64 private constant APR_BOUNDARY_MAX =    2e12; // 200%
int64 private constant APR_BOUNDARY_MIN = -0.5e12; // -50%

     /// @dev Validates that the given APR is within acceptable bounds
    function ensureValid(int64 answer) internal pure {
        require(
            APR_BOUNDARY_MIN <= answer && answer <= APR_BOUNDARY_MAX,
            "INVALID_APR"
        );


// Accounting
int64   private constant APR_BOUNDARY_MAX = 200e12;
int64   private constant APR_BOUNDARY_MIN = 0;

    function normalizeAprFromFeed (/* SD7x12 */ int64 apr) internal pure returns (UD60x18) {
        require(
            APR_BOUNDARY_MIN <= apr && apr <= APR_BOUNDARY_MAX,
            "invalid apr"
        );
```

**Impact:** Protocol DoS: When the feed contains valid negative APR data (between -50% and 0%), the Accounting.normalizeAprFromFeed() function will revert, preventing:

- APR updates via `updateAprs()`;
- Index calculations in `updateIndexes()`;
- Proper accounting updates during deposit/withdrawal flows;

**Recommended Mitigation:** Align the two contracts:

```diff
// Accounting.sol
- int64   private constant APR_BOUNDARY_MIN = 0;
+ int64   private constant APR_BOUNDARY_MIN = -0.5e12; // -50%
```

**Strata:**
Fixed in commit [c80308](https://github.com/Strata-Money/contracts-tranches/commit/c803089861f92533468ee5a31852e7cebaf49e8f) by enforcing APR range on the `Accounting` to not be negative, instead, negative APRs reported from the feed will be considered, Seniors won't have negative APRs.

**Cyfrin:** Verified.
