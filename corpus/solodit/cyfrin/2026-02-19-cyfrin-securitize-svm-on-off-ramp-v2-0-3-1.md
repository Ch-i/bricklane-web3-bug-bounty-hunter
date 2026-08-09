---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0-3-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-02-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0
title: Redundant `#[instruction(asset_provider)]` Attribute in On-Ramp `UpdateAssetProvider`
vuln_class: []
---

# Redundant `#[instruction(asset_provider)]` Attribute in On-Ramp `UpdateAssetProvider`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md)_

---

**Description:** The `UpdateAssetProvider` accounts struct declares the instruction argument `asset_provider` via `#[instruction(asset_provider: crate::AssetProvider)]`, but no account constraint (e.g. `constraint`, `seeds`, or `has_one`) references this variable.

```rust
#[derive(Accounts)]
#[instruction(asset_provider: crate::AssetProvider)]
pub struct UpdateAssetProvider<'info> {
    pub admin: Signer<'info>,

    #[account(
        mut,
        has_one = admin @ SecuritizeOnRampError::Forbidden,
        seeds = [ON_RAMP_STATE_SEED, on_ramp_state.id.to_le_bytes().as_ref()],
        bump = on_ramp_state.bump,
    )]
    pub on_ramp_state: Box<Account<'info, OnRampState>>,
}
```
 The argument is only used in the handler. The attribute is therefore redundant and can be removed for clarity. So the `#[instruction(asset_provider: ...)]` declaration is redundant.

**Impact:** The relevant code is redundant and can be removed for code quality.

**Recommended Mitigation:** Remove the unused attribute.

**Securitize:** Fixed in [b29a57](https://github.com/securitize-io/bc-solana-on-off-ramp-sc/commit/b29a576d2d9def6eb57461206943e5e115673ee8).

**Cyfrin:** Verified.
