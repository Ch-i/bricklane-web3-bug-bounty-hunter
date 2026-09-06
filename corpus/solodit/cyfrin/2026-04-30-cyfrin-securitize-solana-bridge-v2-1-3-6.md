---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-3-6
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-04-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-30-cyfrin-securitize-solana-bridge-v2-1
title: '`GasLimitUpdate` event in DS bridge uses `u128` fields unnecessarily'
vuln_class: []
---

# `GasLimitUpdate` event in DS bridge uses `u128` fields unnecessarily

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** The DS bridge's `GasLimitUpdate` event widens `gas_limit` from `u64` (its storage type in `BridgeConfig`) to `u128` via `u128::from(old_gas_limit)`. This wastes 16 bytes per field in event data. The USDC bridge's `GasLimitUpdate` event correctly uses `u64`.

```rust
// programs/securitize_bridge/src/events.rs:31-32
pub old_gas_limit: u128,
pub new_gas_limit: u128,
```

**Recommended Mitigation:** Change the `GasLimitUpdate` event fields to `u64` for consistency with the stored type and the USDC bridge pattern.

**Securitize:** Fixed in [ce1b0565](https://github.com/securitize-io/bc-solana-bridge-sc/commit/ce1b056548248856f80ccf1d4f1ce3a18142cae9).

Changed GasLimitUpdate event fields from u128 to u64 in the DS bridge (events.rs and update_gas_limit.rs), matching the storage type in BridgeConfig.executor_gas_limit and bringing it in line with the USDC bridge's GasLimitUpdate event.

**Cyfrin:** Confirmed.
