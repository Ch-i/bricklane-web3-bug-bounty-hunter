---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-09-cyfrin-securitize-svm-jump-router-v2-0-1-6
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-06-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-09-cyfrin-securitize-svm-jump-router-v2-0
title: Source filename `mpbs_fee_manager.rs` has transposed letters
vuln_class: []
---

# Source filename `mpbs_fee_manager.rs` has transposed letters

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md)_

---

**Description:** The file defining `MbpsFeeManager` is named `mpbs_fee_manager.rs`, but the type and terminology use `Mbps` for milli-basis-points. The transposed filename makes the module harder to find and can propagate into future imports.

Current locations:

```rust
programs/bc-solana-jump-router-sc/src/states/fee_manager/mpbs_fee_manager.rs
19:    pub struct MbpsFeeManager {

programs/bc-solana-jump-router-sc/src/states/fee_manager/mod.rs
2: mod mpbs_fee_manager;
5: pub use mpbs_fee_manager::*;
```

**Recommended Mitigation:** Rename the file to `mbps_fee_manager.rs` and update the module declarations in `programs/bc-solana-jump-router-sc/src/states/fee_manager/mod.rs`.

**Securitize:** Fixed in [194d314](https://github.com/securitize-io/bc-bd-router-sc/commit/194d314fcc09e165efbe8173a5d6a504e8ac40e4).

**Cyfrin:** Verified.
