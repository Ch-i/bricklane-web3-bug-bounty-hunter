---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-11
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Lack of slippage in `spot_lp` liquidity operations due to relying on the changing
  `header.crncy_tokens` and `header.asset_tokens`
vuln_class: []
---

# Lack of slippage in `spot_lp` liquidity operations due to relying on the changing `header.crncy_tokens` and `header.asset_tokens`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The `spot_lp` function lacks slippage protection when adding or removing liquidity.

In most cases, the function calculates the required asset and currency tokens based on the current pool state at execution time, **without allowing users to specify minimum output amounts or maximum acceptable slippage**. This exposes users to unfavorable execution prices due to pool state changes between transaction submission and execution.

In `src/program/processor/spot_lp.rs`, when adding liquidity (lines 189-194), the function directly calculates the required tokens based on the current pool state:

```rust
trade_crncy_tokens = ((instr_state.header.crncy_tokens + instr_state.header.pool_fees)
    as f64
    * amount as f64
    / instr_state.header.ps as f64) as i64;
trade_asset_tokens = (instr_state.header.asset_tokens as f64 * amount as f64
    / instr_state.header.ps as f64) as i64;
```

The pool's asset_tokens and crncy_tokens are modified during normal trading operations (as seen in `engine.rs` via `change_tokens` and `change_mints`).

```rust
                self.change_tokens(traded_qty, side)?;
                self.change_mints(traded_mints, side)?;
                self.log_amm(traded_qty, traded_mints, side);
```

However, the spot_lp function:
- Does not allow users to specify minimum acceptable output amounts (similar to Uniswap V2's `amountAMin `and `amountBMin`)
- Does not validate that the execution price is within an acceptable range

**Impact:** Users can suffer unexpected losses when adding/removing liquidity due to pool state changes

**Recommended Mitigation:** Add slippage protection parameters to SpotLpData structure and Implement validation checks after calculating `trade_asset_tokens` and `trade_crncy_tokens`

**Deriverse:** Fixed in commit [337383](https://github.com/deriverse/protocol-v1/commit/3373834b7988ba52810515f514664e0c80ca2c8c).

**Cyfrin:** Verified.
