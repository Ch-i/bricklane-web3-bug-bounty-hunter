---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-18-cyfrin-securitize-solana-whitelister-v2-0-2-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-03-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-18-cyfrin-securitize-solana-whitelister-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-18-cyfrin-securitize-solana-whitelister-v2-0
title: Permissionless `Initialize` and Counter Saturation Edge Case
vuln_class: []
---

# Permissionless `Initialize` and Counter Saturation Edge Case

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-18-cyfrin-securitize-solana-whitelister-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-18-cyfrin-securitize-solana-whitelister-v2.0.md)_

---

**Description:** There is no access control on `initialize`. Any payer can create a `VaultRegistrarState` with any `admin` (who must sign) and any `asset_mint`:

```rust
#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(mut)]
    pub payer: Signer<'info>,

    pub admin: Signer<'info>,
    // ...
    pub asset_mint: InterfaceAccount<'info, anchor_spl::token_interface::Mint>,
    // ...
}
```

This allows arbitrary actors to create registrars with arbitrary configurations, which may pollute the namespace and complicate discovery of legitimate registrars.

Additionally, when the global counter reaches `u64::MAX`, `saturating_add(1)` saturates and subsequent `initialize` calls will fail because the PDA for that id already exists.


```rust
ctx.accounts.vault_registrar_counter.set_inner(VaultRegistrarCounter {
    count: id.saturating_add(1),
    bump: ctx.bumps.vault_registrar_counter,
});
```

When `count` reaches `u64::MAX`, it saturates and stays at `u64::MAX`. The next `initialize` call will attempt to create a `vault_registrar_state` with seeds `[VAULT_REGISTRAR_STATE_SEED, u64::MAX.to_le_bytes()]`, but that PDA already exists from the previous successful init. The `init` constraint will fail because the account cannot be created twice.

**Impact:**
- **Permissionless**: Spam or low-quality registrars may be created, but no direct security impact since each registrar is isolated.
- **Counter saturation**: Theoretically prevents new registrars once `u64::MAX` is reached. Reaching this value is economically infeasible.


**Recommended Mitigation:** If this intentional, document the permissionless design as intentional.

**Securitize:** Fixed in [4a09894](https://github.com/securitize-io/bc-solana-whitelister/commit/4a09894fe802d324d7dceee0442ab873841e4c3d).

**Cyfrin:** Verified.
