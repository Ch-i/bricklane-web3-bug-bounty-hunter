---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-22-cyfrin-doryoku-v2-0-1-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-07-22T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-22-cyfrin-doryoku-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-22-cyfrin-doryoku-v2-0
title: Hard-coded `9` decimals for xBELO mint can mismatch underlying BELO mint
vuln_class: []
---

# Hard-coded `9` decimals for xBELO mint can mismatch underlying BELO mint

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-22-cyfrin-doryoku-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-22-cyfrin-doryoku-v2.0.md)_

---

**Description:** During `initialize` the program creates the xBELO receipt token like this:

```rust
#[account(
    init, payer = admin,
    mint::decimals = 9,            // ← hard-coded
    mint::authority = state,
    mint::freeze_authority = state
)]
pub xgkhan_mint: Account<'info, Mint>,
```

The number of decimals is fixed at **9** instead of copying `belo_mint.decimals`.
If the canonical BELO mint was deployed with any other precision (e.g., 6 or 18), the 1 : 1 accounting assumption between BELO locked in the vault and xBELO outstanding is violated.

**Impact:** This can break the 1 : 1 accounting assumption between BELO and xBELO.


**Recommended Mitigation:** * At `initialize`, **read the decimals of `gkhan_mint` and reuse them**:

```diff
      #[account(
          init, payer=admin,
-         mint::decimals=9,
+         mint::decimals=gkhan_mint.decimals,
          mint::authority=state,
          mint::freeze_authority=state
      )]
      pub xgkhan_mint: Account<'info, Mint>,
```

**Doryoku:**
Fixed in [74212b7](https://github.com/Warlands-Nft/xbelo/commit/74212b762fc90a0a1060522f50e5be96bf10a892).

**Cyfrin:** Verified.
