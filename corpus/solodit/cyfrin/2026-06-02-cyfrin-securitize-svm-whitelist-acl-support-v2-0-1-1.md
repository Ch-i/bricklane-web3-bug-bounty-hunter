---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-02-cyfrin-securitize-svm-whitelist-acl-support-v2-0-1-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-06-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-02-cyfrin-securitize-svm-whitelist-acl-support-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-02-cyfrin-securitize-svm-whitelist-acl-support-v2-0
title: SPL sRFC-37 access-control thaw forwards caller-selected CPI accounts without
  tying them to the validated authority path
vuln_class: []
---

# SPL sRFC-37 access-control thaw forwards caller-selected CPI accounts without tying them to the validated authority path

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-02-cyfrin-securitize-svm-whitelist-acl-support-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-02-cyfrin-securitize-svm-whitelist-acl-support-v2.0.md)_

---

**Description:** For an sRFC-37 mint whose Token ACL `MintConfig.freeze_authority` is the `spl-token-access-control` authority PDA, `FreezeAuthorityType::from_mint_and_freeze_authority` re-derives the access-control authority PDA from the mint, verifies it matches the supplied `srfc37_authority`, and returns `AcProgramWithSrfc37`:

```rust
let ac_program_authority = Pubkey::find_program_address(
    &[
        spl_token_access_control::constants::ACCESS_CONTROL_AUTHORITY_SEED,
        mint.key().as_ref(),
    ],
    &spl_token_access_control::ID,
)
.0;
if ac_program_authority == srfc37_authority.key() {
    require!(
        authority.key() != srfc37_authority.key(),
        SplWhitelistErrorCode::InvalidFreezeAuthorityType
    );
    return Ok(Self::AcProgramWithSrfc37);
}
```

The wrapper has authoritatively established, from the mint alone, the identity of the access-control authority for this thaw.

The `AcProgramWithSrfc37` branch of `thaw_account` then takes the next five entries of `remaining_accounts` and forwards them as the downstream CPI accounts:

```rust
Self::AcProgramWithSrfc37 => {
    require!(
        additional_accounts.len() == self.additional_accounts_len(),
        SplWhitelistErrorCode::InvalidFreezeAuthorityType
    );

    let access_control_authority = &additional_accounts[0];
    let access_control_state = &additional_accounts[1];
    let event_authority = &additional_accounts[2];
    let program = &additional_accounts[3];
    require!(
        *program.key == spl_token_access_control::ID,
        SplWhitelistErrorCode::InvalidFreezeAuthorityType
    );
    let token_acl_program = &additional_accounts[4];
    require!(
        *token_acl_program.key == TOKEN_ACL,
        SplWhitelistErrorCode::InvalidFreezeAuthorityType
    );

    let ac_program_thaw_accounts =
        spl_token_access_control::cpi::accounts::ThawAccount {
            access_control_authority: access_control_authority.to_account_info(),
            access_control_state: access_control_state.to_account_info(),
            authority: authority.to_account_info(),
            event_authority: event_authority.to_account_info(),
            ...
        };
```

The slot-to-CPI mapping is:

| Index | Slot in CPI | Wrapper-side check |
|-------|-------------|--------------------|
| `[0]` | `access_control_authority` | none |
| `[1]` | `access_control_state` | none |
| `[2]` | `event_authority` | none |
| `[3]` | `spl-token-access-control` program | program ID equality |
| `[4]` | Token ACL program | program ID equality |

The first three slots are accepted unconditionally. The wrapper does not require `additional_accounts[0] == srfc37_authority` (which it already derived), does not re-derive `[ACCESS_CONTROL_STATE_SEED, mint]` for slot `[1]`, and does not re-derive the `#[event_cpi]` event authority PDA for slot `[2]`.

This is currently safe only because the pinned `spl-token-access-control` revalidates these accounts through its own Anchor PDA constraints on `ThawAccount`:

```rust
#[account(
    seeds = [ACCESS_CONTROL_STATE, mint.key().as_ref()],
    bump = access_control_state.bump,
)]
pub access_control_state: Account<'info, AccessControlState>,

#[account(
    seeds = [ACCESS_CONTROL_AUTHORITY_SEED, mint.key().as_ref()],
    bump,
)]
pub access_control_authority: AccountInfo<'info>,
```

The wrapper has performed the classification work to know what the correct accounts must be, then discards that knowledge and relies on downstream constraints to catch mismatches.

This is the only freeze-authority mode with the gap: `SystemAccount` and `AcProgram` pass the Anchor-validated `freeze_authority` directly into the CPI rather than reading authority-bearing slots from `remaining_accounts`, and `SystemAccountWithSrfc37` only forwards the Token ACL program account (which is checked against `TOKEN_ACL`).


**Recommended Mitigation:** In the `AcProgramWithSrfc37` branch, derive `access_control_authority`, `access_control_state`, and the `__event_authority` PDA from the mint under `spl_token_access_control::ID`, and require `additional_accounts[0..3]` to equal those derivations before constructing the CPI. Apply the same change to the `AcProgram` branch's `access_control_state` and `event_authority` slots.

**Securitize:** Acknowledged.
