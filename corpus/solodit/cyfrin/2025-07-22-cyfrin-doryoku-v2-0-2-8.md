---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-22-cyfrin-doryoku-v2-0-2-8
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-07-22T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-22-cyfrin-doryoku-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-22-cyfrin-doryoku-v2-0
title: StakeCounter Struct Declared but Never Utilized
vuln_class: []
---

# StakeCounter Struct Declared but Never Utilized

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-22-cyfrin-doryoku-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-22-cyfrin-doryoku-v2.0.md)_

---

**Description:** The `clmm_lp_farming` program has a struct `StakeCounter` that includes a field `count`. However this struct is not utilized anywhere in the program:

```rust
#[account]
pub struct StakeCounter {
    pub count: u64,
}

impl StakeCounter {
    pub const LEN: usize = 8;
}
```

**Recommended Mitigation:** Consider removing `StakeCounter` struct with its `LEN` implementation.

**Doryoku:**
Fixed in [fad227e](https://github.com/Warlands-Nft/belo_clmm_lp_farming/commit/fad227e80c53e207a8836365ed0c8449a17f2992).

**Cyfrin:** Verified.
