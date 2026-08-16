---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-22-cyfrin-doryoku-v2-0-2-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-07-22T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-22-cyfrin-doryoku-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-22-cyfrin-doryoku-v2-0
title: Vesting Parameter Updates are Not Constrained Sufficiently
vuln_class: []
---

# Vesting Parameter Updates are Not Constrained Sufficiently

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-22-cyfrin-doryoku-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-22-cyfrin-doryoku-v2.0.md)_

---

**Description:** The `update_vest_params` function in `xbelo` program, allows admin to update minimum-maximum vesting durations, and minimum-maximum burn percentages.
However it doesn't contrained enough to prevent wrong configurations between interconnected variables. Hence it is possible to provide values that will break functionality of functions. For example, `vest_min` can be bigger than `vest_max` which would prevent `vesting` completely considering there will be no valid `vest_duration` that can bypass duration checks.

**Recommended Mitigation:** Consider adding following checks:
```rust
require!(new_vest_max > new_vest_min, ErrorCode::InvalidParams);
require!(new_min_burn_pct > new_max_burn_pct, ErrorCode::InvalidParams);
```
**Doryoku:**
Fixed in [4ecb4a0](https://github.com/Warlands-Nft/xbelo/commit/4ecb4a089595eee98fff5be4f2be570023ca2511).

**Cyfrin:** Verified.
