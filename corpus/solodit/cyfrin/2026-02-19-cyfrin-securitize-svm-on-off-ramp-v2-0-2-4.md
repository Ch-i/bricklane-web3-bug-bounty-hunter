---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0-2-4
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-02-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0
title: Inadequate validations on `collector-token-account`.
vuln_class: []
---

# Inadequate validations on `collector-token-account`.

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md)_

---

**Description:** `collector_token_account` in `initialize` and `update_fee_manager_handler` instruction lacks proper validations. When updating the [FeeManager] via the [update_fee_manager] instruction, the protocol only validates the fee percentage (numerator) but does not validate the `collector_token_account` address

The [validate()] function in [mpbs_fee_manager.rs] only checks the fee numerator:
```rust
impl FeeManagerTrait for MbpsFeeManager {
    fn validate(&self) -> Result<()> {
        require!(
            self.numerator <= Self::MAX_FEE_NUMERATOR,
            SecuritizeOnRampError::MaxFeeExceeded
        );
        Ok(())
    }
}
```
During swap operations, the [fee_collector_ta] is validated against the stored address in [swap_ds_token.rs] and [swap_spl_token.rs]:
```rust
#[account(
    mut,
    address = on_ramp_state.fee_manager.fee_collector_token_account()
        @ crate::errors::SecuritizeOnRampError::InvalidFeeCollector,
    token::mint = liquidity_mint,
    token::token_program = liquidity_token_program,
)]
pub fee_collector_ta: Box<InterfaceAccount<'info, TokenAccount>>,
```
However, this validation only occurs at swap time. If an admin sets an invalid `collector_token_account` address (e.g., wrong mint, frozen account, closed account, or non-existent account), the constraint will fail and all swaps will be blocked until the admin fixes the configuration.

**Impact:** Temporarily denial of service for swaps

**Recommended Mitigation:** Add validation of the collector_token_account in the UpdateFeeManager instruction to ensure it:
- Exists and is a valid token account
- Has the correct mint ([liquidity_mint]
- Is not frozen

**Securitize:** Fixed in [be1ac28](https://github.com/securitize-io/bc-solana-on-off-ramp-sc/commit/be1ac28823ec2719d8ac9956780b7fa176da01a4).

**Cyfrin:** Verified.
