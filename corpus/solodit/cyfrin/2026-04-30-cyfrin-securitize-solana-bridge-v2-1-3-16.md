---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-3-16
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
title: '`PauseStatusChanged` is not mint-self-describing for off-chain consumers'
vuln_class: []
---

# `PauseStatusChanged` is not mint-self-describing for off-chain consumers

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** The event is currently defined as:

  ```rust
  #[event]
  pub struct PauseStatusChanged {
      pub bridge_instance: Pubkey,
      pub paused: bool,
  }

and `set_paused` emits:

  emit!(PauseStatusChanged {
      bridge_instance: ctx.accounts.config.key(),
      paused,
  });

At this point the program already has access to config.asset_mint, because the config PDA is constrained with:

```rust
seeds = [BridgeConfig::SEED_PREFIX, config.asset_mint.as_ref()]
```

So the omitted field is available at emission time, but is not surfaced in the event payload.


**Impact:** The practical effect is limited to off-chain observability.

**Recommended Mitigation:** If better observability is desired, add `asset_mint` to `PauseStatusChanged` so pause/unpause activity can be attributed directly from the event stream without extra resolution.

**Securitize:** Fixed in [0d9595](https://github.com/securitize-io/bc-solana-bridge-sc/commit/0d9595ee6844da7d3e2cbe2c4bd6b11ce0247e5d).
Fixed in both programs: PauseStatusChanged now includes the token mint (asset_mint for securitize_bridge, usdc_mint for securitize_usdc_bridge) alongside bridge_instance and paused, so pause/unpause activity can be attributed directly from the event stream without an additional account fetch.

**Cyfrin:** Confirmed.

\clearpage
