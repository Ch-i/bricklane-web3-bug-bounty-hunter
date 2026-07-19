---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-3-13
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-04-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-30-cyfrin-securitize-solana-bridge-v2-1
title: '`initialize` does not pin `usdc_mint` to the canonical Solana USDC mint'
vuln_class: []
---

# `initialize` does not pin `usdc_mint` to the canonical Solana USDC mint

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** `initialize` accepts any SPL mint and creates a separate `UsdcBridgeConfig` instance keyed by that mint. This matches the program’s per-mint deployment model, **but it places responsibility on operators and tooling to pass the intended cluster-specific USDC mint during setup.**

```rust
    /// USDC mint. Constraint: valid SPL mint.
    #[account(
        mint::token_program = token_program,
    )]
    pub usdc_mint: Box<Account<'info, Mint>>,
```


**Impact:** If the owner initializes the bridge with the wrong mint, they may create an unusable or unintended bridge instance for that mint.

**Recommended Mitigation:** Document the expected cluster-specific USDC mint more explicitly, and optionally add SDK/CLI safeguards or warnings for known devnet/mainnet USDC mint addresses.

**Securitize:** Acknowledged. The per-mint deployment model is intentional to support multiple clusters (mainnet vs devnet USDC mints differ). initialize is gated on the program upgrade authority (fix for https://github.com/securitize-io/bc-solana-bridge-sc/issues/3), so only the trusted owner - who operates from internal deployment runbooks - can call it. An incorrect mint produces a distinct, unused UsdcBridgeConfig PDA (seeds include usdc_mint), so no funds are at risk and no collision with the correct instance is possible.
