---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-2-7
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
title: Inconsistent Price Reference Used for Trade Execution Logic in `new_spot_order`
  and `swap`
vuln_class: []
---

# Inconsistent Price Reference Used for Trade Execution Logic in `new_spot_order` and `swap`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The `new_spot_order` and `swap` functions use different methods to obtain the reference price (`px`) for determining whether orders should execute, which creates inconsistency in the codebase.


In `src/program/processor/new_spot_order.rs`:
```rust
let px = engine.market_px();
```

In `src/program/processor/swap.rs`:
```rust
let px = engine.state.header.last_px;
```

In `src/program/processor/spot_quotes_replace.rs`:
```rust
let px = engine.state.header.last_px;
```

**Difference:**

The `market_px()` function (lines 1898-1906 in `engine.rs`) returns:
- `best_ask` if `best_ask < last_px`
- `best_bid` if `best_bid > last_px`
- `last_px` otherwise

This means `market_px()` may return an order book price (`best_ask` or `best_bid`) rather than the actual last traded price (`last_px`).

**Impact:** While both functions use `|| engine.cross(...)` as a fallback, the different `px` values may not directly cause security vulnerabilities, it may lead to subtle behavioral differences since:

- The `px` value is passed to `drv_update`, which uses it for fixing price calculations.
- Also, the `px` value is passed to `write_last_tokens`, which uses it to set `last_close` and `day_low` when crossing day boundaries.

**Recommended Mitigation:** Standardize the price reference across all spot trading functions.

**Deriverse:** Fixed in commit [f7e57dc](https://github.com/deriverse/protocol-v1/commit/f7e57dcf4bac3b7ec6bf4fdc07198abb7a9a443e).

**Cyfrin:** Verified
