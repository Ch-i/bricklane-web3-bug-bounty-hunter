---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0-3-5
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-02-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0
title: Investor’s dsTokens May Become Locked After His Country Is Banned
vuln_class: []
---

# Investor’s dsTokens May Become Locked After His Country Is Banned

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md)_

---

**Description:** The off-ramp program enforces country-based restrictions during DS token redemption via the [countries_restriction] bitmap stored in [OffRampState]. Before processing any redemption, [redeem_ds_token_handler] reads the investor's country from their on-chain [IdentityAccount] and verifies it is not restricted:
```rust
let redeemer_country = ctx.accounts.identity_account.country;

require!(
    !off_ramp_state
        .countries_restriction
        .is_restricted(redeemer_country),
    SecuritizeOffRampError::RestrictedCountry,
);
```
However, the on-ramp program,  which handles the inverse flow (investor sends liquidity tokens to receive asset tokens) has no country restriction mechanism at all. The [OnRampState] struct lacks a [countries_restriction] field entirely:
```rust
pub struct OnRampState {
    pub id: u64,
    pub admin: Pubkey,
    pub asset_mint: Pubkey,
    pub asset_token_type: TokenType,
    pub liquidity_mint: Pubkey,
    pub nav_provider: NavProvider,
    pub is_paused: bool,
    pub fee_manager: FeeManager,
    pub custodian_wallet: Pubkey,
    pub bump: u8,
    pub on_ramp_authority_bump: u8,
    pub min_subscription_amount: u64,
    pub investor_subscription_enabled: bool,
    pub two_step_transfer: bool,
    pub asset_provider: AssetProvider,
    pub operators: Vec<Pubkey>,
    // No countries_restriction field
}
```
There are no checks implemented for checking investor's country inside all three swap functions:
-  for `swap_spl_tokens` the operator signs, s**o we can trust here that operator would not sign for investors from banned countries**
-  for `subscribe_ds_tokens`, registrar authority signs, so we can assume above here too
-  but for `swap_ds_tokens` only investor signs the transaction while providing his `wallet_identity` account, only check that is made is that `wallet_identity` account belongs to investor signing the transaction, the on-ramp program does not enforce country restrictions when processing `swap_ds_tokens`:
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

Although `swap_ds_tokens` requires that the investor has previously called `subscribe_ds_tokens` (since a `wallet_identity` account must exist), there is no country re-validation during the swap flow.


This creates the following state transition inconsistency:
1. An investor from a non-restricted country calls `subscribe_ds_tokens` and successfully creates their `wallet_identity` or even hold some DS tokens.
2. At a later time, the admin updates the off-ramp `countries_restriction` bitmap and bans the investor’s country.
3. The old investor can still call `swap_ds_tokens` on the on-ramp, since no country restriction is enforced there.
4. The investor acquires additional DS tokens.
5. When attempting to redeem through the off-ramp, `redeem_ds_token_handler` rejects the transaction with `RestrictedCountry`.

Generally, if the investor already held DS tokens before the country was banned, those tokens immediately become non-redeemable. As a result, DS tokens can become economically locked: the investor holds a token but cannot exit via the protocol’s designated redemption mechanism which is more of a design flaw. This lock persists unless the admin later removes the country restriction on the off-ramp, which may contradict the regulatory rationale for imposing the restriction.

**Impact:** Investors whose country becomes restricted after registration:
- Can continue acquiring DS tokens through `swap_ds_tokens`
- Cannot redeem those tokens through the off-ramp
- May have pre-existing DS tokens that become permanently non-redeemable

Investors from restricted countries can acquire asset tokens through the on-ramp that they are unable to redeem through the off-ramp. This results in locked funds from the investor.

**Recommended Mitigation:** Add a [countries_restriction] field (identical [CountriesRestriction] bitmap) to [OnRampState] and enforce country checks in all investor-facing on-ramp instructions..

**Securitize:** Acknowledged; this is expected behavior and aligns with the requirements.

\clearpage
