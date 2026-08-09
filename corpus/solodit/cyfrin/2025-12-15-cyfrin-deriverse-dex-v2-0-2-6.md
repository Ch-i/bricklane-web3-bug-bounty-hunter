---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-2-6
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Missing `last_time` Update in `spot_lp` Causes Incorrect Daily Trade Statistics
vuln_class: []
---

# Missing `last_time` Update in `spot_lp` Causes Incorrect Daily Trade Statistics

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The `spot_lp` function uses `instr_state.header.last_time` to determine if a day has passed, but never updates this field.

In contrast, other trading functions (`swap, new_spot_order, spot_quotes_replace`) update `last_time` via `engine.write_last_tokens()`. This inconsistency causes incorrect daily LP trade statistics when regular trading operations haven't occurred recently.

In `src/program/processor/spot_lp.rs`, the function checks if a day has passed using:

```solidity
if instr_state.header.last_time < fixing_time {
    instr_state.header.lp_prev_day_trades = instr_state.header.lp_day_trades;
    instr_state.header.lp_day_trades = 1;
} else {
    instr_state.header.lp_day_trades += 1;
}
```

However, `instr_state.header.last_time` is never updated in the `spot_lp` function, while other trading functions update it.

Consider the following case:
- Last regular trade (swap/new_spot_order) occurred 1 day ago, setting last_time to that timestamp
- Multiple spot_lp operations occur today
- For each spot_lp:
    - `last_time` remains from 1 day ago
    - `fixing_time` is today's settlement time
    - `last_time < fixing_time` is always true
    - `lp_day_trades` is reset to 1 instead of incrementing


**Impact:** In such case(last regular trade occurred 1 day ago), all LP trades on the same day are counted as the first trade of the day, losing accurate daily statistics.

**Recommended Mitigation:** Update `last_time` in the `spot_lp` function after the day-crossing check.

```rust
instr_state.header.lp_day_trades += 1;
}
instr_state.header.last_time = time;  // Add this line
```

**Deriverse:** Fixed in commit [29281c5](https://github.com/deriverse/protocol-v1/commit/29281c5e489ad01efbb5124e62c45f55aa309348).

**Cyfrin:** Verified.
