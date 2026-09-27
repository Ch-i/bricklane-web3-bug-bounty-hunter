---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2-0-3-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-09-17T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2-0
title: Cache repeated `access_control_authority_pda` and `mint_config_pda` derivations
  to cut redundant hashing in the SPL register and thaw flow
vuln_class: []
---

# Cache repeated `access_control_authority_pda` and `mint_config_pda` derivations to cut redundant hashing in the SPL register and thaw flow

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2.0.md)_

---

**Description:** `register_vault_spl` and `thaw_vault_token_account_spl` resolve the same ACL PDAs several times per execution: `FreezeAuthorityType::from_mint` derives `access_control_authority_pda` and `mint_config_pda`, and the subsequent `require_valid` validation chain re-derives those same addresses again, so a single PDA can be derived with `find_program_address` up to four times in one instruction.

```rust
programs/vault-registrar/src/utils/freeze_authority_type.rs
  30:        if freeze_authority == access_control_authority_pda(&mint_key) {
  34:        if freeze_authority == mint_config_pda(&mint_key) {
 102:        let acl_authority = access_control_authority_pda(asset_mint);
 123:                    mint_config_pda(asset_mint),
 147:        mint_config_pda(asset_mint),
 168:        access_control_authority_pda(asset_mint),

programs/vault-registrar/src/utils/access_control.rs
  28:        access_control_authority_pda(asset_mint),

programs/vault-registrar/src/instructions/register_vault_spl.rs
 107:    let freeze_authority_type = FreezeAuthorityType::from_mint(&ctx.accounts.asset_mint)?;
 111:        .require_valid(&asset_mint, freeze_authority_type)?;
 115:        .require_valid(&asset_mint, freeze_authority_type)?;

programs/vault-registrar/src/instructions/thaw_vault_token_account_spl.rs
  81:    let freeze_authority_type = FreezeAuthorityType::from_mint(&ctx.accounts.asset_mint)?;
  85:        .require_valid(&asset_mint, freeze_authority_type)?;
```

**Recommended Mitigation:** Resolve each PDA once per instruction and thread the values through the validation chain instead of re-deriving them. For example, have `FreezeAuthorityType::from_mint` also return the resolved authority and mint-config keys, or introduce a small context struct the `require_*` methods accept:

```rust
pub struct FreezeContext {
    pub kind: FreezeAuthorityType,
    pub acl_authority: Pubkey,
    pub mint_config: Option<Pubkey>,
}

impl FreezeContext {
    pub fn from_mint(asset_mint: &InterfaceAccount<Mint>) -> Result<Self> {
        let mint_key = asset_mint.key();
        let freeze_authority: Pubkey = asset_mint.freeze_authority.into()
            .ok_or(VaultRegistrarError::MintNotAclManaged)?;
        let acl_authority = access_control_authority_pda(&mint_key);
        if freeze_authority == acl_authority {
            return Ok(Self { kind: FreezeAuthorityType::AcProgram, acl_authority, mint_config: None });
        }
        let mint_config = mint_config_pda(&mint_key);
        if freeze_authority == mint_config {
            return Ok(Self { kind: FreezeAuthorityType::AcProgramWithSrfc37, acl_authority, mint_config: Some(mint_config) });
        }
        Err(VaultRegistrarError::MintNotAclManaged.into())
    }
}
```

The `require_freeze_authority_accounts`, `require_mint_config`, and `require_acl_backed_mint_config` methods then take the precomputed `acl_authority` and `mint_config` pubkeys instead of calling `find_program_address` again, collapsing the duplicated authority and mint-config derivations to one each per instruction. The distinct `access_control_state_pda` is still derived by `require_access_control_state` and is not part of the context, so the worst-case sRFC-37 path drops from up to eight `find_program_address` calls per instruction to three.

**Securitize:** Fixed in commit [515847](https://github.com/securitize-io/bc-solana-whitelister/commit/5158473503d4ec9d2ad7c83b1365a023be601c71).

**Cyfrin:** Verified.

\clearpage
