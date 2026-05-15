---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0-2-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-02-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0
title: DS Token Subscription Can Proceed Without Wallet Identity Verification When
  Registration Accounts Are Omitted
vuln_class: []
---

# DS Token Subscription Can Proceed Without Wallet Identity Verification When Registration Accounts Are Omitted

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md)_

---

**Description:** The `subscribe_ds_token` instruction allows a path where all optional registration/identity accounts are None. In that branch, no CPI registration occurs and there is no on‑chain wallet_identity constraint enforced before the swap executes. Unlike `swap_ds_token`, which always validates `wallet_identity` via PDA constraints, this flow can mint/transfer DS tokens to an unregistered wallet if the asset provider/token does not independently enforce identity checks.

```rust
(None, None, None, None, None, None, None, None, None) => {
    require_eq!(
        register_investor_cpi_data_len,
        0,
        SecuritizeOnRampError::InvalidRegisterInvestorConfig
    );
    require_eq!(
        add_levels_cpi_data_len,
        0,
        SecuritizeOnRampError::InvalidAddLevelsConfig
    );

    // All optional accounts for registering investor and adding levels are None
    require!(
        ctx.accounts.identity_metadata_registry_program.is_none()
            && ctx.accounts.investor.is_none()
            && ctx.accounts.wallet_identity.is_none()
            && ctx.accounts.policy_engine_program.is_none()
            && ctx.accounts.tracker_account.is_none()
            && ctx
                .accounts
                .event_authority_identity_metadata_registry
                .is_none()
            && ctx.accounts.policy_engine.is_none(),
        SecuritizeOnRampError::InvalidRegisterInvestorConfig
    )
}
```

- `swap_ds_token`
```rust
/// Check that the investor wallet is registered
#[account(
    constraint = wallet_identity.wallet == investor_wallet.key()
        @ SecuritizeOnRampError::Forbidden,
    seeds = [investor_wallet.key().as_ref(), asset_mint.key().as_ref()],
    seeds::program = identity_registry::ID,
    bump,
)]
pub wallet_identity: Box<Account<'info, identity_registry::WalletIdentity>>,
```

**Impact:** If DS token enforcement is not guaranteed by the asset provider or token hooks, unregistered wallets may receive DS tokens, violating compliance/identity requirements.

**Recommended Mitigation:** Require wallet_identity verification in subscribe_ds_token when registration is not performed, or enforce that registration CPI accounts must be supplied for DS token subscriptions.

**Securitize:** Fixed in [8d87df5](https://github.com/securitize-io/bc-solana-on-off-ramp-sc/commit/8d87df515949a722d05860bd8f1fa23a1410c901).

**Cyfrin:** Verified.
