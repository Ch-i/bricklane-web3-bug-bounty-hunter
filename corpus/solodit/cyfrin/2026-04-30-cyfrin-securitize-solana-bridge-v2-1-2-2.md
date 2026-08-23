---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-2-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-04-30T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-30-cyfrin-securitize-solana-bridge-v2-1
title: '`UsdcBridgeConfig::max_executor_fee` defaults to zero, disabling the executor
  fee cap'
vuln_class: []
---

# `UsdcBridgeConfig::max_executor_fee` defaults to zero, disabling the executor fee cap

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** `UsdcBridgeConfig::max_executor_fee` is initialized to 0 in `initialize.rs:38`. In `SendUsdcCrossChainDeposit::handler`, the fee cap check at line 186 is skipped when the value is 0:

```rust
if config.max_executor_fee != 0 {
    require_gte!(config.max_executor_fee, exec_amount, ...);
}
```

An authorized bridge caller can set `exec_amount` to any value up to the config PDA's available SOL.

**Impact:** Defense-in-depth gap. Whitelisted bridge callers could drain config PDA excess SOL through inflated executor fees. Mitigated by the bridge caller trust model.

**Recommended Mitigation:** Always enforce the cap:

```rust
require_gte!(config.max_executor_fee, exec_amount, UsdcBridgeError::ExecutorFeeExceedsMax);
```

Or initialize `max_executor_fee` to a sensible non-zero default.

**Securitize:** Fixed in [8207188e](https://github.com/securitize-io/bc-solana-bridge-sc/commit/8207188e56624e0c8fae02ba472d1a1fad93dc94).

Made max_executor_fee a required non-zero argument to initialize (and rejected zero in update_max_executor_fee), and removed the if != 0 guard in send_usdc_cross_chain_deposit so the per-call cap exec_amount <= max_executor_fee is now unconditionally enforced.

**Cyfrin:** Confirmed.
