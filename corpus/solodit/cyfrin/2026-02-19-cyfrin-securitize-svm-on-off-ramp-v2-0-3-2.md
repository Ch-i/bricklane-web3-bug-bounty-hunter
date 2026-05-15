---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0-3-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-02-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0
title: Incompatible NavProviders can be set, which could fail swaps temporarily
vuln_class: []
---

# Incompatible NavProviders can be set, which could fail swaps temporarily

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md)_

---

**Description:** The protocol has two distinct swap token types, `Dstoken` and `SplToken`. Each tokenType is coupled with specific `NavProvider`. DsTokens require StandardNavProvider where splTokens require AmmNavProvider.. If wrong NavProviders are set, it throws errors:
In case of ds tokens' swaps
```rust
        NavProvider::AmmNavProvider(_) => {
            return err!(SecuritizeOnRampError::UnsupportedNavProvider);
        }
```
In case of spl tokens' swaps:
```rust
        NavProvider::StandardNavProvider(_) => {
            return err!(SecuritizeOnRampError::UnsupportedNavProvider)
        }
```
However, the `update_nav_provider_handler` instruction does'nt make sure the passed in `NavProviders` are compatible with the tokenType of particular onramp, admin can mistakenly set incompitable NavProviders and hence swaps would fail until type is fixed.

Note: similarly `update_asset_provider_handler` lacks incompatibility validation too

**Impact:** Temporarily swap failures.

**Recommended Mitigation:** Add compatibility validation:
```rust
pub fn update_nav_provider_handler(
    ctx: &mut Context<UpdateNavProvider>,
    nav_provider: NavProvider,
) -> Result<()> {
    let on_ramp_state = &mut ctx.accounts.on_ramp_state;

    let old_nav_provider = on_ramp_state.nav_provider;

    require!(
        old_nav_provider != nav_provider,
        SecuritizeOnRampError::NoChange
    );

    // Validate NavProvider is compatible with asset_token_type
    match (&on_ramp_state.asset_token_type, &nav_provider) {
        (TokenType::DsToken, NavProvider::AmmNavProvider(_)) => {
            return err!(SecuritizeOnRampError::UnsupportedNavProvider);
        }
        (TokenType::SplToken, NavProvider::StandardNavProvider(_)) => {
            return err!(SecuritizeOnRampError::UnsupportedNavProvider);
        }
        _ => {}
    }

    on_ramp_state.nav_provider = nav_provider;

    // ...existing code...
    Ok(())
}
```
**Securitize:** Fixed in [d14f30e](https://github.com/securitize-io/bc-solana-on-off-ramp-sc/commit/d14f30e6b549999addef7bdc9e80824435ca9acc).

**Cyfrin:** Verified.
