---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2-0-0-1
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-09-17T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2-0
title: Revoking an SPL mint authority permanently prevents subsequent registrar initialization
vuln_class: []
---

# Revoking an SPL mint authority permanently prevents subsequent registrar initialization

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2.0.md)_

---

**Description:** The updated `Initialize` accounts require `asset_mint` to have a live mint authority matching the supplied `asset_mint_authority` account:

```rust
#[account(mint::authority = asset_mint_authority)]
pub asset_mint: InterfaceAccount<'info, anchor_spl::token_interface::Mint>,

/// CHECK: Bound to the mint by the constraint above. Its owner and contents decide whether the
/// registrar is created for a DS or an SPL token.
pub asset_mint_authority: UncheckedAccount<'info>,
```

Anchor 0.31.1 expands `mint::authority` into a comparison against `COption::Some(asset_mint_authority.key())`:

```rust
if asset_mint.mint_authority
    != COption::Some(asset_mint_authority.key())
{
    return Err(ErrorCode::ConstraintMintMintAuthority.into());
}
```

No account can satisfy this constraint when the Token-2022 mint's authority has been permanently revoked to `COption::None`. Account validation therefore fails before `initialize_handler` reaches `detect_token_config` and classifies the mint as SPL.

This live mint-authority requirement is unnecessary for the SPL branch itself. After classification, `require_spl_mint_accounts` validates that the account is a Token-2022 mint and that its freeze authority is controlled by the ACL:

```rust
fn require_spl_mint_accounts(
    ctx: &Context<Initialize>,
    asset_mint: &Pubkey,
) -> Result<()> {
    require!(
        ctx.accounts.identity_registry.is_none(),
        VaultRegistrarError::IdentityRegistryNotAllowed
    );

    require_token_2022_mint(&ctx.accounts.asset_mint)?;

    let freeze_authority_type =
        FreezeAuthorityType::from_mint(&ctx.accounts.asset_mint)?;
    let mint_config = ctx.accounts.mint_config.as_ref().map(|a| a.as_ref());

    freeze_authority_type.require_mint_config(asset_mint, mint_config)
}
```

Later SPL registration and thaw operations likewise depend on the ACL-controlled freeze authority rather than the mint authority. The SDK independently enforces the same restriction by rejecting initialization whenever `mint.mintAuthority` is absent.

Consequently, an otherwise valid ACL-managed asset that finalizes issuance by revoking its mint authority cannot create a registrar afterward, even though its freeze authority and every account required for SPL registration and thawing remain valid. Because setting a Token-2022 authority to `None` is irreversible, the asset cannot restore the authority merely to satisfy initialization.

**Impact:** ACL-managed assets that revoke mint authority before registrar setup are permanently excluded from the registrar's SPL integration path. They cannot onboard vaults through a newly created registrar unless the program is upgraded or the registrar was initialized before revocation.

The issue requires no attacker, does not affect registrars created before revocation, and depends on whether authority revocation is a supported asset lifecycle. If every current and planned asset intentionally retains a live mint authority, this is instead a deployment prerequisite that should be documented and enforced operationally.

**Recommended Mitigation:** Decouple SPL classification from the existence of a mint authority:

- Make `asset_mint_authority` optional and remove the unconditional `mint::authority` account constraint.
- When `asset_mint.mint_authority` is `Some`, require the supplied authority account to match before using it for DS classification.
- When it is `None`, permit only the SPL branch and continue enforcing Token-2022 ownership and the ACL-backed freeze-authority checks.
- Preserve the existing DS invariant that a DS mint must have the expected asset-controller mint authority.
- Update the SDK so a missing mint authority is passed as the optional account state instead of rejected client-side.

**Securitize:** Fixed in commit [a4d0208](https://github.com/securitize-io/bc-solana-whitelister/commit/a4d020862ff72ae4a88782efe3a3588d20f1d82b).

**Cyfrin:** Verified.
