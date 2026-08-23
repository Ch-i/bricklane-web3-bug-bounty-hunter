---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-3-7
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-04-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-30-cyfrin-securitize-solana-bridge-v2-1
title: '`format!` used where `.to_string()` suffices for country conversion'
vuln_class: []
---

# `format!` used where `.to_string()` suffices for country conversion

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** In `BridgeDsTokens::handler`:

```rust
// programs/securitize_bridge/src/instructions/bridge/bridge_ds_tokens.rs:331
country: format!("{}", ctx.accounts.investor.country),
```

`.to_string()` (which uses the `Display` trait) is equivalent, shorter, and more idiomatic.

**Recommended Mitigation:** Replace with `ctx.accounts.investor.country.to_string()`.

**Securitize:** Fixed in [0b78bf](https://github.com/securitize-io/bc-solana-bridge-sc/commit/0b78bfa8d7068f2c84080f450a1c8194e8fa0533).

Replaced `format!("{}", identity.country)` with `identity.country.to_string()` in `bridge_ds_tokens.rs`.

**Cyfrin:** Confirmed.
