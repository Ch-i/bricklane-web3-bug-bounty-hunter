---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-17-cyfrin-securitize-solana-spl-acl-v2-0-1-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-03-17T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-17-cyfrin-securitize-solana-spl-acl-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-17-cyfrin-securitize-solana-spl-acl-v2-0
title: '`setup_extra_metas` forwards PDA signer authority to an unvalidated `gating_program`
  in an admin-only path'
vuln_class: []
---

# `setup_extra_metas` forwards PDA signer authority to an unvalidated `gating_program` in an admin-only path

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-17-cyfrin-securitize-solana-spl-acl-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-17-cyfrin-securitize-solana-spl-acl-v2.0.md)_

---

**Description:** `setup_extra_metas` only checks that the supplied `gating_program` is executable. It does not verify that the target program matches the gate configured for the mint. The CPI helper then invokes that executable with `invoke_signed`, forwarding the `access_control_authority` PDA as a signer-capable account. This path is explicitly admin-only. Under the stated trust model, the admin is already trusted and can configure the gating program elsewhere in the protocol. As a result, this is better characterized as an admin safety / integration-hardening issue than a direct privilege-escalation issue.

```rust
/// CHECK: Gating program
#[account(constraint = gating_program.executable @ AccessControlError::NotExecutable)]
pub gating_program: AccountInfo<'info>,
```

```rust
let ix = Instruction {
    program_id: ctx.accounts.gating_program.key(),
    accounts: accounts_meta,
    data: instruction_data,
};

let mut account_infos = vec![
    ctx.accounts.access_control_authority.to_account_info(),
    ctx.accounts.admin.to_account_info(),
    ctx.accounts.mint_config.to_account_info(),
    ctx.accounts.mint.to_account_info(),
    ctx.accounts.extra_metas.to_account_info(),
    ctx.accounts.system_program.to_account_info(),
];

account_infos.extend_from_slice(ctx.remaining_accounts);

invoke_signed(&ix, &account_infos, signer_seeds)?;
```

**Impact:** The main risk is misconfiguration or malicious frontend / operator confusion: an admin can be tricked into calling `setup_extra_metas` against the wrong executable and unintentionally forward signer privileges into an unexpected CPI target.

**Recommended Mitigation:** Before the CPI, deserialize the relevant Token-ACL config and require the supplied `gating_program` to equal the configured gate for the mint.

**Securitize:** Fixed in [0330e59](https://github.com/securitize-io/bc-solana-spl-acl-sc/commit/0330e59230f11892539ecc75645dddd0aa654985).

**Cyfrin:** Verified.
