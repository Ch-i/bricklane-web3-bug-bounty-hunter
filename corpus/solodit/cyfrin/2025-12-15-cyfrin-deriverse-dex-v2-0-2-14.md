---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-2-14
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Missing Fixing Window Data Accumulation After Daily Reset in `drv_update`
vuln_class: []
---

# Missing Fixing Window Data Accumulation After Daily Reset in `drv_update`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** When `drv_update` resets fixing data for a new day, the current `last_asset_tokens` and `last_crncy_tokens` are discarded instead of being accumulated into the new day's fixing data, leading to incomplete fixing price calculations.

In `src/state/instrument.rs`, the `drv_update` function handles daily reset logic:
```rust
if current_date > last_fixing_date {
    // Calculate new fixing price based on previous day's data
    let new_fixing_px: i64 = if self.header.fixing_crncy_tokens
        > get_dec_factor(self.header.crncy_token_decs_count)
    {
        (self.header.fixing_crncy_tokens as f64 * self.header.dec_factor as f64
            / self.header.fixing_asset_tokens as f64) as i64
    } else {
        prev_px
    };
    self.header.fixing_asset_tokens = 0;  // Reset
    self.header.fixing_crncy_tokens = 0;  // Reset
    self.header.fixing_time = time;
    // ... update variance and fixing_px
} else {
    // Only accumulate if within fixing window
    let sec = time % DAY;
    if last_asset_tokens > 0 && (SETTLEMENT - FIXING_DURATION..SETTLEMENT).contains(&sec) {
        self.header.fixing_asset_tokens += last_asset_tokens;
        self.header.fixing_crncy_tokens += last_crncy_tokens;
    }
}
```

When entering a new day (`current_date > last_fixing_date`), the code resets `fixing_asset_tokens` and `fixing_crncy_tokens` to `0`
However, if the current time time is still within the fixing window (S`ETTLEMENT - FIXING_DURATION..SETTLEMENT`), the current `last_asset_tokens` and `last_crncy_tokens` should be accumulated into the new day's fixing data. **Currently, these values are discarded after reset, and the code does not check if the current time is within the fixing window**


**Impact:** Trading volume that occurs immediately after the daily reset but within the fixing window is not included in the fixing price calculation.

**Recommended Mitigation:** After resetting the fixing data, check if the current time is within the fixing window and accumulate the current data if applicable.

**Deriverse:** Fixed in commit [d17502c5](https://github.com/deriverse/protocol-v1/commit/d17502c5b1c9fc44abad88365f7d60b3b3325a26).

**Cyfrin:** Verified.
