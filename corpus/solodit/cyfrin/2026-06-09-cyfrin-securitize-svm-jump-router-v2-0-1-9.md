---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-09-cyfrin-securitize-svm-jump-router-v2-0-1-9
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-06-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-09-cyfrin-securitize-svm-jump-router-v2-0
title: Use a two-step admin transfer flow to reduce the risk of irreversible governance
  mistakes
vuln_class: []
---

# Use a two-step admin transfer flow to reduce the risk of irreversible governance mistakes

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-09-cyfrin-securitize-svm-jump-router-v2.0.md)_

---

**Description:** The router updates the admin in a single transaction. While this is not an exploitable security issue by itself, a one-step transfer increases governance and operational risk because an incorrect address becomes authoritative immediately, with no acceptance step by the new admin.


The current admin transfer flow directly overwrites `jump_router_state.admin` after validating that the new key is non-default and different from the current admin:

```rust
pub fn change_admin_handler(ctx: &mut Context<ChangeAdmin>, new_admin: Pubkey) -> Result<()> {
    let jump_router_state = &mut ctx.accounts.jump_router_state;

    require!(
        new_admin != Pubkey::default(),
        JumpRouterError::DefaultPubkeyNotAllowed
    );

    require!(
        jump_router_state.admin != new_admin,
        JumpRouterError::NoChange
    );

    jump_router_state.admin = new_admin;

    emit!(crate::events::AdminChanged {
        jump_router: jump_router_state.key(),
        admin: ctx.accounts.admin.key(),
        new_admin,
    });

    Ok(())
}
```

Because the transfer completes in one step, any mistake in the destination address immediately changes control of the router. A two-step pattern is generally preferred for privileged role transfers because it requires the nominated admin to explicitly accept the role before the change becomes effective.

**Impact:** It increases the likelihood of governance mistakes, especially during key rotation, incident response, or operational handovers.

**Recommended Mitigation:** Adopt a two-step admin transfer flow.

**Securitize:** Acknowledged.
