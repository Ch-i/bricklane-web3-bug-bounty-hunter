---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-09-cyfrin-securitize-svm-jump-router-v2-0-1-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-06-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-09-cyfrin-securitize-svm-jump-router-v2-0
title: '`MbpsFeeManager` doc comments mislabel milli-basis-points as basis points'
vuln_class: []
---

# `MbpsFeeManager` doc comments mislabel milli-basis-points as basis points

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md)_

---

**Description:** `MbpsFeeManager` operates in milli-basis-points with denominator `100_000`, but its comments call the units "bps" and "Basis points". A basis point denominator would be `10_000`; this implementation uses `100_000`, so one unit is a milli-basis-point.

Current comments:

```rust
programs/bc-solana-jump-router-sc/src/states/fee_manager/mpbs_fee_manager.rs
18:    /// Mbps-based fee manager (basis points)
19:    pub struct MbpsFeeManager {
20:        /// Fee numerator (bps)
21:        pub numerator: u32,
27:        /// Basis points denominator (100,000 = 0.001%)
28:        pub const DENOMINATOR: u32 = 100_000;
```

**Recommended Mitigation:** Replace "bps" / "Basis points" with "milli-bps" / "milli-basis-points" in the comments.

**Securitize:** Fixed in [8eb6e94](https://github.com/securitize-io/bc-bd-router-sc/commit/8eb6e943b9ece1173cd0aaa3647d7e5ef662346a).

**Cyfrin:** Verified.
