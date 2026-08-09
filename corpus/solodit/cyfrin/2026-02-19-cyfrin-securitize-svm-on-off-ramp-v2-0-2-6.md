---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0-2-6
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-02-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0
title: Countries restriction defaults to empty on initialize, allowing all jurisdictions
  to use the protocol
vuln_class: []
---

# Countries restriction defaults to empty on initialize, allowing all jurisdictions to use the protocol

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md)_

---

**Description:** When a new off-ramp state is created via `initialize`, `countries_restriction` is hardcoded to `CountriesRestriction::default()` (an all-zero bitmap). No country is therefore restricted until an admin explicitly calls `update_countries_restriction`.

```rust
    let off_ramp_state_inst = OffRampState {
        admin: ctx.accounts.admin.key(),
        asset_mint: ctx.accounts.asset_mint.key(),
        asset_policy,
        asset_token_type,
        bump: ctx.bumps.off_ramp_state,

        id: counter,
        is_paused: false,
        off_ramp_authority_bump: ctx.bumps.off_ramp_authority,
        nav_provider,
        liquidity_mint: ctx.accounts.liquidity_mint.key(),
        fee_manager,
        countries_restriction: CountriesRestriction::default(),
        operators: vec![],
        two_step_transfer: false,
        liquidity_provider,
    };
```


`CountriesRestriction` is a 32-byte bitmap; the default is all zeros:

```rust
/// Bitmap for restricting up to 256 countries
#[derive(AnchorDeserialize, AnchorSerialize, Clone, Debug, InitSpace, Default)]
pub struct CountriesRestriction([u8; 32]);
```

With all bits zero, `is_restricted(idx)` is false for every country index:

```rust
    /// Returns true if the country is restricted
    pub fn is_restricted(&self, idx: u8) -> bool {
        let byte = self.0[(idx / 8) as usize];
        let bit = idx % 8;
        (byte & (1 << bit)) != 0
    }
```

User redemption enforces the restriction here:

```rust
    require!(
        !off_ramp_state
            .countries_restriction
            .is_restricted(redeemer_country),
        SecuritizeOffRampError::RestrictedCountry,
    );
```


So from the first `initialize` until the first `update_countries_restriction` (and if that call is forgotten or delayed, indefinitely), no country is restricted and users from any jurisdiction can redeem.

**Impact:** **Compliance / regulatory risk**: If the protocol is required to restrict certain countries from launch (e.g., sanctions or licensing), the default behavior is non-compliant until an admin updates the bitmap.

**Recommended Mitigation:** Add an optional (or required) argument to the `initialize` instruction so the deployer can set the initial bitmap in the same transaction.

**Securitize:** Acknowledged, We wouldn't want to make the init logic heavier and tightly coupled with compliance config. And the admin, can always combine the initialize and update_countries_restriction instructions into one transaction if needed.
