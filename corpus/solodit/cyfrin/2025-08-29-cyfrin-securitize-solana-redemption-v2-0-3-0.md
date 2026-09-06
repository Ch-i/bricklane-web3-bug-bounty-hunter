---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-29-cyfrin-securitize-solana-redemption-v2-0-3-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-08-29T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-29-cyfrin-securitize-solana-redemption-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-29-cyfrin-securitize-solana-redemption-v2-0
title: Fee collector field ambiguity wallet vs token account
vuln_class: []
---

# Fee collector field ambiguity wallet vs token account

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-29-cyfrin-securitize-solana-redemption-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-29-cyfrin-securitize-solana-redemption-v2.0.md)_

---

**Description:** `FeeManager::collector` is a `Pubkey` named like a wallet, but every place that uses it expects a **token account address** for the liquidity mint. In `initialize` and `update_fee_manager` you require `fee_collector_ta.address == fee_manager.fee_collector()` and enforce `token::mint = liquidity_token_mint`.

If an integrator sets `collector` to a wallet pubkey instead of the token account pubkey, the instruction fails or fees route incorrectly across environments.

```rust
/// Fee manager enum for fee strategies
pub enum FeeManager {
    /// Mbps-based fee manager
    MbpsFeeManager(MbpsFeeManager),
}
```
```rust
/// Mbps-based fee manager (basis points)
pub struct MbpsFeeManager {
    /// Fee numerator (bps)
    pub numerator: u32,
    /// Fee collector address
    pub collector: Pubkey,
}
```

**Recommended Mitigation:** Rename the field to `collector_token_account` to reflect intent.

**Securitize:** Fixed in [ab7f4d2](https://github.com/securitize-io/bc-solana-redemption-sc/commit/ab7f4d2f9110df2bf37ec1d2c8f7e2f4b1545310).

**Cyfrin:** Verified.
