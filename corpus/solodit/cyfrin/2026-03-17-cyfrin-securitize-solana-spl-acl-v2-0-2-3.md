---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-17-cyfrin-securitize-solana-spl-acl-v2-0-2-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-03-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-17-cyfrin-securitize-solana-spl-acl-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-17-cyfrin-securitize-solana-spl-acl-v2-0
title: Incorrect Documentation Comment for `create_config_handler`
vuln_class: []
---

# Incorrect Documentation Comment for `create_config_handler`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-17-cyfrin-securitize-solana-spl-acl-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-17-cyfrin-securitize-solana-spl-acl-v2.0.md)_

---

**Description:** The doc comment for `create_config_handler` incorrectly describes the behavior of `delete_config_handler`. The comment states "Delete mint config and sent lamports to receiver" when the function actually creates a mint config via CPI to the token-acl program.

```rust
/// Delete mint config and sent lamports to receiver
pub fn create_config_handler<'info>(
    ctx: Context<'_, '_, '_, 'info, CreateConfig<'info>>,
) -> Result<()> {
    cpi::srfc_37::create_config::handler(&ctx)?;

    emit_cpi!(events::CreateConfig {
        access_control_state_key: ctx.accounts.access_control_state.key(),
        admin: ctx.accounts.admin.key(),
        mint: ctx.accounts.mint.key(),
        mint_config: ctx.accounts.mint_config.key(),
    });

    Ok(())
}
```

**Impact:** Developers may misinterpret the function's purpose, leading to confusion and potential misuse during future development.

**Recommended Mitigation:** Update the doc comment to accurately describe the function's behavior.

**Securitize:** Fixed in [2c439f9](https://github.com/securitize-io/bc-solana-spl-acl-sc/commit/2c439f929f6a1e4413483f98ff392746204fb450).

**Cyfrin:** Verified.
