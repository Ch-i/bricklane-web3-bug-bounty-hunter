---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-3-5
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-04-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-30-cyfrin-securitize-solana-bridge-v2-1
title: Magic numbers in `securitize_usdc_bridge::initialize` for default config values
vuln_class: []
---

# Magic numbers in `securitize_usdc_bridge::initialize` for default config values

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** The USDC bridge `Initialize::handler` hardcodes default values without named constants:

```rust
// programs/securitize_usdc_bridge/src/instructions/admin/initialize.rs:37,40
config.executor_gas_limit = 2_000_000;
config.min_finality_threshold = 2000;
```

**Recommended Mitigation:** Define named constants with documentation:

```rust
pub const DEFAULT_EXECUTOR_GAS_LIMIT: u64 = 2_000_000;
pub const DEFAULT_MIN_FINALITY_THRESHOLD: u32 = 2_000;
```

**Securitize:** Fixed in [32d3afff](https://github.com/securitize-io/bc-solana-bridge-sc/commit/32d3afffa6fe1896d43c1f1eab7af38c7c973b18).

Partially applicable: executor_gas_limit is no longer hardcoded - it was converted to a validated handler parameter in a prior audit fix. The min_finality_threshold = 2000 value is Circle's CCTP V2 "Standard" finality constant. We extracted it into a named constant CCTP_STANDARD_FINALITY_THRESHOLD in constants.rs with a doc comment.

**Cyfrin:** Confirmed.
