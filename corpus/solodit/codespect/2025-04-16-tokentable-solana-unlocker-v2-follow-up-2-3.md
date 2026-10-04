---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-16-tokentable-solana-unlocker-v2-follow-up-2-3
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-04-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-16-TokenTable-Solana-Unlocker-V2-Follow-Up.md
tags:
- firm:codespect
- report:2025-04-16-tokentable-solana-unlocker-v2-follow-up
title: '[I-04] Redundant code'
vuln_class: []
---

# [I-04] Redundant code

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-16-TokenTable-Solana-Unlocker-V2-Follow-Up.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-16-TokenTable-Solana-Unlocker-V2-Follow-Up.md)_

---

**Files:** [utils.rs](https://github.com/EthSign/tokentable-unlocker-solana/tree/67a39faff7b848ae05c5e3ab45e36b60efcc622e/programs/unlocker-v2-solana/src/instructions/utils.rs#L54), [collect_fee.rs](https://github.com/EthSign/tokentable-unlocker-solana/tree/67a39faff7b848ae05c5e3ab45e36b60efcc622e/programs/fee-collector/src/instructions/collect_fee.rs#L29), [get_fee.rs](https://github.com/EthSign/tokentable-unlocker-solana/tree/67a39faff7b848ae05c5e3ab45e36b60efcc622e/programs/fee-collector/src/instructions/get_fee.rs#L17)

**Description:**

The protocol contains multiple pieces of redundant code.

1. When obtaining the special configuration `fee_bips` if `fee_bips` equals `BIPS_PRECISION(10000)` it will be set to 0;

```rust
pub fn collect_fee(
    ctx: Context<CollectFee>,
    fee_token: Pubkey,
    _project_id: String,
    token_transferred: u64
) -> Result<u64> {
    //...
    let mut fee_bips = ctx.accounts.fee.bips;

    if fee_bips == BIPS_PRECISION {
        fee_bips = 0;
    }
```

However, this logic is redundant because `fee_bips` is already restricted to not exceed `MAX_FEE(1000)` during configuration.

2. In the `claim()` instruction of the Unlocker program it is imperative to validate the provided `fee_collector` program account if it matches the one held within the unlocker account. This is done directly within the `claim()` inside `claim.rs` file:

```rust
if ctx.accounts.unlocker.fee_collector != Pubkey::default() {
    require!(
        ctx.accounts.unlocker.fee_collector == ctx.accounts.fee_collector.key(),
        TokenTableError::InvalidFeeCollector
    );
}
```

Later in the code, `_claim()` is called, which calls `_after_claim()`, which calls `_charge_fees()`. Inside it we can find the same unnecessary validation:

```rust
require!(
    fee_collector.key() == storage.fee_collector.key(),
    TokenTableError::UnsupportedOperation
);
```

Where the `storage` is in fact the unlocker account. What is more the Airdrop program, does not contain such a redundant check in its `_charge_fees()` equivalent. It is recommended to remove the check from the `_charge_fees()` function.

**Impact:** Redundant code hinders readability and increases deployment costs.

**Recommendation:** It is recommended to optimize the redundant code.

**Status:** Fixed

**Update from TokenTable:** Redundant code for checking `fee_collector` removed in [78051afb53579a4e6558519000d6c35f510a5533](https://github.com/EthSign/tokentable-unlocker-solana/pull/8/commits/78051afb53579a4e6558519000d6c35f510a5533), validating fees removed in [8c443f729b4eefd491832bcac71d996c317f8252](https://github.com/EthSign/tokentable-unlocker-solana/pull/8/commits/8c443f729b4eefd491832bcac71d996c317f8252),
