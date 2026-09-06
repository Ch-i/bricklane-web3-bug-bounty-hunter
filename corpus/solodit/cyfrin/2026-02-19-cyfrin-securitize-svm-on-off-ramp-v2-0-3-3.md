---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0-3-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-02-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0
title: Off-Ramp `update_fee_manager` Does Not Validate `liquidity_mint`
vuln_class: []
---

# Off-Ramp `update_fee_manager` Does Not Validate `liquidity_mint`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md)_

---

**Description:** In the on-ramp program, `update_fee_manager` explicitly binds the instruction to a `liquidity_mint` by requiring `on_ramp_state` to have `has_one = liquidity_mint` and by passing a `liquidity_mint` account.

```rust
    #[account(
        mut,
        has_one = liquidity_mint @ SecuritizeOnRampError::InvalidMint,
        has_one = admin @ SecuritizeOnRampError::Forbidden,
        seeds = [ON_RAMP_STATE_SEED, on_ramp_state.id.to_le_bytes().as_ref()],
        bump = on_ramp_state.bump,
    )]
    pub on_ramp_state: Box<Account<'info, OnRampState>>,

    #[account(
        mint::token_program = liquidity_token_program,
    )]
    pub liquidity_mint: Box<InterfaceAccount<'info, Mint>>,

    pub liquidity_token_program: Interface<'info, TokenInterface>,
```

The off-ramp program’s `update_fee_manager` does not perform any `liquidity_mint`-based check, even though `OffRampState` also has a `liquidity_mint` field. This inconsistency can make it easier to target the wrong state by mistake and weakens alignment between the two programs.

```
    #[account(
        mut,
        has_one = admin @ SecuritizeOffRampError::Forbidden,
        seeds = [OFF_RAMP_STATE_SEED, off_ramp_state.id.to_le_bytes().as_ref()],
        bump = off_ramp_state.bump,
    )]
    pub off_ramp_state: Box<Account<'info, OffRampState>>,
```

**Impact:** On-ramp and off-ramp diverge in how they constrain `update_fee_manager`. Requiring the liquidity mint account and `has_one = liquidity_mint` would make the “which state for which mint” invariant explicit and align off-ramp with on-ramp and with other off-ramp instructions.

**Recommended Mitigation:** Align off-ramp with on-ramp and with other off-ramp instructions.

**Securitize:** Fixed in [bbcdfe0](https://github.com/securitize-io/bc-solana-on-off-ramp-sc/commit/bbcdfe045b6a2983b7d54a220a1fe31032a3e3e8).

**Cyfrin:** Verified.
