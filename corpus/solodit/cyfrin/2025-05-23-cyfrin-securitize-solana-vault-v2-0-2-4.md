---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-23-cyfrin-securitize-solana-vault-v2-0-2-4
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-05-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-23-cyfrin-securitize-solana-vault-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-23-cyfrin-securitize-solana-vault-v2-0
title: '`Liquidate` Event Emits Shares and Assets in Wrong Order'
vuln_class: []
---

# `Liquidate` Event Emits Shares and Assets in Wrong Order

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-23-cyfrin-securitize-solana-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-23-cyfrin-securitize-solana-vault-v2.0.md)_

---

**Description:** The `Liquidate` event is fired making `shares` as the second parameter and `assets` as the third parameter

> bc-solana-vault-sc/programs/sc-vault/src/instructions/liquidator/liquidate.rs#liquidate_handler
```rust
    emit!(crate::events::Liquidate {
        liquidator: ctx.accounts.liquidator.key(),
2:      shares,
3:      assets,
    });
```

But the event construction is not like this, as `assets` are the second parameter not third. and shares is the third parameter not second.

> bc-solana-vault-sc/programs/sc-vault/src/events.rs
```rust
#[event]
pub struct Liquidate {
    pub liquidator: Pubkey,
2:  pub assets: u64,
3:  pub shares: u64,
}
```

There is also another thing to point out here, which is `assets` themselves. As the `assets` will be transferred to the  liquidator if the vault is not activating `redemption`, but in case of supporting redemption the actual amount transferred to the liquidator is `liquidation_amount`. This may cause confusion at case weather assets are the actual received balance, or what.

**Impact:** Incorrect event emission leads to incorrect tracking, analysis of the liquidation process.


**Recommended Mitigation:**
- Swap assets position with shares position
```diff
    emit!(crate::events::Liquidate {
        liquidator: ctx.accounts.liquidator.key(),
-       shares,
        assets,
+       shares,
    });
```
- And for `liquidation_amount` this can be mitigated by adding another parameter for `liquidation_amount` (default is zero if no Redemption is not supported)

**Securitize:** Fixed in [c766076](https://github.com/securitize-io/bc-solana-vault-sc/commit/c7660762f01943c3d0fe6e6074cf3bea682b7093).

**Cyfrin:** Verified

\clearpage
