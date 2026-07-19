---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0-2-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-02-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0
title: Missing Executable Check for NAV Provider in `update_nav_provider`
vuln_class: []
---

# Missing Executable Check for NAV Provider in `update_nav_provider`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md)_

---

**Description:** The on-ramp program’s `update_nav_provider` instruction accepts the new NAV provider only via **instruction data** (`NavProvider`) and does not validate that the embedded program ID refers to an executable program.

```rust
pub fn update_nav_provider_handler(
    ctx: &mut Context<UpdateNavProvider>,
    nav_provider: NavProvider,
) -> Result<()> {
```

The off-ramp program’s equivalent instruction accepts the new NAV provider as an **account** and enforces `#[account(executable)]`, ensuring the stored value is a valid program.

```rust
    /// New NAV provider program (must be executable)
    ///
    /// CHECK: Admin must provide a valid NAV provider program
    #[account(executable)]
    pub new_nav_provider: AccountInfo<'info>,
}
```

For On-ramp, `NavProvider` is deserialized from instruction data and  Any pubkey can be written into state. The new NAV provider is passed only as instruction data and there is no account and no executable check.

**Impact:** This inconsistency allows the on-ramp to store an arbitrary pubkey (e.g. a non-executable account or PDA) as the NAV provider program ID, which can cause failed CPIs, unexpected behavior, or misuse if other code trusts this value.

**Recommended Mitigation:** Align the on-ramp with the off-ramp by ensuring the new NAV provider is validated as an executable program.

**Securitize:** Fixed in [b4ba06a](https://github.com/securitize-io/bc-solana-on-off-ramp-sc/commit/b4ba06a8ab722b8770bffd46b10c85102104b0c8).

**Cyfrin:** Verified.
