---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-16-tokentable-solana-unlocker-v2-follow-up-2-4
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-04-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-16-TokenTable-Solana-Unlocker-V2-Follow-Up.md
tags:
- firm:codespect
- report:2025-04-16-tokentable-solana-unlocker-v2-follow-up
title: '[I-05] The fee_collector constraint prevents the unlocker from claiming without
  a fee'
vuln_class: []
---

# [I-05] The fee_collector constraint prevents the unlocker from claiming without a fee

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-16-TokenTable-Solana-Unlocker-V2-Follow-Up.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-16-TokenTable-Solana-Unlocker-V2-Follow-Up.md)_

---

**Files:** [claim_cancelled_actual_tokens.rs](https://github.com/EthSign/tokentable-unlocker-solana/tree/67a39faff7b848ae05c5e3ab45e36b60efcc622e/programs/unlocker-v2-solana/src/instructions/claim_cancelled_actual_tokens.rs#L179), [claim.rs](https://github.com/EthSign/tokentable-unlocker-solana/tree/67a39faff7b848ae05c5e3ab45e36b60efcc622e/programs/unlocker-v2-solana/src/instructions/claim.rs#L285)

**Description:**

The following code indicates that when `unlocker.fee_collector` is set to `pubkey::default()`, the claim will not incur any fees.

```rust
// Fee collector
if ctx.accounts.unlocker.fee_collector != Pubkey::default() {
    require!(
        ctx.accounts.unlocker.fee_collector == ctx.accounts.fee_collector.key(),
        TokenTableError::InvalidFeeCollector
    );
}
```

```rust
pub fn _charge_fees<'info>(...) -> Result<u64> {
    let mut fee_collected: u64 = 0;
    if storage.fee_collector != Pubkey::default() {
        //...
    }

    Ok(fee_collected)
}
```

However, the `fee_collector` constraint in the `claim` and `claim_cancelled_actual_tokens` instructions causes the `unlocker.fee_collector` to fail the constraint check if it is set to `pubkey::default()`, thus preventing the fee-less claim from passing.

```rust
#[account(constraint = fee_collector.key() == unlocker.fee_collector.key())]
pub fee_collector: Program<'info, FeeCollector>,
```

**Impact:** The code’s intended fee-less claim cannot be achieved.

**Recommendation:** Remove the `fee_collector` constraint.

**Status:** Fixed

**Update from TokenTable:** As of [78051afb53579a4e6558519000d6c35f510a5533](https://github.com/EthSign/tokentable-unlocker-solana/pull/8/commits/78051afb53579a4e6558519000d6c35f510a5533), the fee collection mechanism is no longer optional. In [aa48e8ab3c30b65f0e90a3be35cdb81a7f7f9461](https://github.com/EthSign/tokentable-unlocker-solana/pull/8/commits/aa48e8ab3c30b65f0e90a3be35cdb81a7f7f9461), `fee_collector` is an `UncheckedAccount<>` with manual account verification checks.
