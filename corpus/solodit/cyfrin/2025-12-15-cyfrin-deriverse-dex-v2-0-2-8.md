---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-2-8
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Missing Signer and New Account Validation for `asset_token_program_acc` in
  `new_instrument`
vuln_class: []
---

# Missing Signer and New Account Validation for `asset_token_program_acc` in `new_instrument`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The `new_instrument` instruction lacks validation checks for `asset_token_program_acc` when creating a new asset token account. Unlike `new_base_crncy` which explicitly validates that the program token account is a signer and a new account, `new_instrument` omits these checks, leading to inconsistent error handling.

In new_instrument.rs, when `is_new_account(asset_token_acc)` is true, the code directly calls `TokenState::create_token` which internally calls `create_programs_token_account`. This function requires `asset_token_program_acc` to be a signer because it performs system operations:

```rust
    if is_new_account(asset_token_acc) {
        let decimals = *asset_mint
            .data
            .borrow()
            .get(MINT_DECIMALS_OFFSET)
            .ok_or_else(|| drv_err!(DeriverseErrorKind::InvalidClientDataFormat))?
            as u32;

        if !(MIN_DECS_COUNT..=MAX_DECS_COUNT).contains(&decimals) {
            bail!(DeriverseErrorKind::InvalidDecsCount {
                decs_count: decimals,
                min: MIN_DECS_COUNT,
                max: MAX_DECS_COUNT,
                token_address: *asset_mint.key,
            });
        }

        #[cfg(feature = "native_mint_2022")]
        if *asset_mint.key == spl_token::native_mint::ID {
            bail!(LegacyNativeMintNotSupported);
        }
        #[cfg(not(feature = "native_mint_2022"))]
        if *asset_mint.key == spl_token_2022::native_mint::ID {
            bail!(Token2022NativeMintNotSupported);
        }

        TokenState::create_token(
            root_state,
            asset_mint,
            asset_token_acc,
            drvs_auth_acc,
            &drvs_auth,
            bump_seed,
            program_id,
            asset_token_program_acc,
            token_program,
            signer,
            decimals,
        )?;
```

However, new_instrument does not validate:
- Whether `asset_token_program_acc.is_signer` is true
- Whether `asset_token_program_acc` is a new account (`is_new_account(asset_token_program_acc)`)

This is required, however, in the comment, indicating that when creating a new token, this account should be a signer.

```rust
///
/// [*Incorrect Price Validation When Creating `NewInstrumentData` Struct during `NewInstrumentInstruction` instruction*](#incorrect-price-validation-when-creating-newinstrumentdata-struct-during-newinstrumentinstruction-instruction) - Asset Tokens Program Account `[SPL, if new_token signer]` - Spl token account
///
```

In contrast, `new_base_crncy.rs` explicitly performs these validations:

```rust
if is_new_account(token_acc) {
    if !is_new_account(program_acc) {
        bail!(InvalidNewAccount { ... });
    }
    if !program_acc.is_signer {
        return Err(drv_err!(MustBeSigner { ... }));
    }
    // ...
}
```

Note: similar works for `new_root_account`, do we also need to check the signer for that?

```rust
///
/// [*typo error in variables*](#typo-error-in-variables) - Deriverse Program Account `[SPL]` - Spl token account
///
```

**Impact:**
- Inconsistent error handling: different validation patterns across similar instructions, causing failures occur during CPI calls rather than early validation

**Recommended Mitigation:** Add explicit validation checks in new_instrument.rs when `is_new_account(asset_token_acc)` is true, matching the pattern in `new_base_crncy.rs`

**Deriverse:** Fixed in commit [96f4e923](https://github.com/deriverse/protocol-v1/commit/96f4e92343fce5610ed89a3063bfed053bc578e5).

**Cyfrin:** Verified.
