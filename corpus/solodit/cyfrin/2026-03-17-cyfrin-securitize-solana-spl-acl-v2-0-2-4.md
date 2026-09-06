---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-17-cyfrin-securitize-solana-spl-acl-v2-0-2-4
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-03-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-17-cyfrin-securitize-solana-spl-acl-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-17-cyfrin-securitize-solana-spl-acl-v2-0
title: '`new_freeze_authority` Omitted from `DeleteConfig` Event'
vuln_class: []
---

# `new_freeze_authority` Omitted from `DeleteConfig` Event

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-17-cyfrin-securitize-solana-spl-acl-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-17-cyfrin-securitize-solana-spl-acl-v2.0.md)_

---

**Description:** The `DeleteConfig` event does not include the `new_freeze_authority` field, even though the instruction transfers the mint's freeze authority to this account. This creates an incomplete audit trail and prevents off-chain indexers from knowing who holds freeze authority after a config deletion.

```rust
/// Delete mint config and sent lamports to receiver
pub fn delete_config_handler<'info>(
    ctx: Context<'_, '_, '_, 'info, DeleteConfig<'info>>,
) -> Result<()> {
    cpi::srfc_37::delete_config::handler(&ctx)?;

    emit_cpi!(events::DeleteConfig {
        access_control_state_key: ctx.accounts.access_control_state.key(),
        admin: ctx.accounts.admin.key(),
        mint: ctx.accounts.mint.key(),
        mint_config: ctx.accounts.mint_config.key(),
        receiver: ctx.accounts.receiver.key(),
    });

    Ok(())
}
```

By contrast, `SetFreezeAuthority` and `SetMintAuthority` events include both old_authority and new_authority, establishing the pattern that authority changes should be logged.


**Impact:** Audit trail: Off-chain systems cannot determine who holds freeze authority after a `DeleteConfig `without parsing on-chain account state.
Indexing: Indexers and analytics tools cannot fully reconstruct authority history from events alone.


**Recommended Mitigation:** Add `new_freeze_authority` to the `DeleteConfig` event struct.

**Securitize:** Fixed in [0fbfe5d](https://github.com/securitize-io/bc-solana-spl-acl-sc/commit/0fbfe5dce3c7d3c9d2e7d003535c4564928193f8).

**Cyfrin:** Verified.
