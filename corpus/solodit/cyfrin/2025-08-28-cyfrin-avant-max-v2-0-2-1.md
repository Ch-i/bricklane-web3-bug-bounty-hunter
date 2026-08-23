---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-28-cyfrin-avant-max-v2-0-2-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-08-28T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-28-cyfrin-avant-max-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-28-cyfrin-avant-max-v2-0
title: Improve `PriceStorage` storage packing
vuln_class: []
---

# Improve `PriceStorage` storage packing

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-28-cyfrin-avant-max-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-28-cyfrin-avant-max-v2.0.md)_

---

**Description:** * `PriceStorage::upperBoundPercentage` and `lowerBoundPercentage` can be safely declared as `uint128` to pack them into the same storage slot:
```diff
- uint256 public upperBoundPercentage;
- uint256 public lowerBoundPercentage;
+ uint128 public upperBoundPercentage;
+ uint128 public lowerBoundPercentage;
```

This reduces gas costs of every call to `PriceStorage::setPrice` where they are read together.

* `IPriceStorage::Price` can safely use `uint128` for `price` and `timestamp` to pack each `Price` struct into the same storage slot:
```diff
interface IPriceStorage {
  struct Price {
-   uint256 price;
-   uint256 timestamp;
+   uint128 price;
+   uint128 timestamp;
  }
```

This saves two storage writes in `PriceStorage::setPrice` when writing to `prices[key]` and `lastPrice`.

**Avant:**
Fixed in commits [0325fcd](https://github.com/Avant-Protocol/Avant-Contracts-Max/commit/0325fcdfb7d78e311fb194845bb27ea541a301a0), [d40fc3d](https://github.com/Avant-Protocol/Avant-Contracts-Max/commit/d40fc3d103a502d2a3ab54939dd43ca8193ca176).

**Cyfrin:** Verified.
