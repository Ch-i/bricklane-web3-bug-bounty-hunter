---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0-2-5
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
title: Investors can grief Operators
vuln_class: []
---

# Investors can grief Operators

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md)_

---

**Description:** In the `swap_spl_token` flow, the check for investor's token account's balance occurs at the end of the execution path inside `swap_process()`.
```rust
    // in `swap_logic.rs`
    // Transfer liquidity from investor
    require_gte!(
        params.investor_liquidity_ta.amount,
        params.liquidity_amount,
        SecuritizeOnRampError::InsufficientBalance
    );
```
after several computationally expensive operations have already been performed:
- Pause state check
- Token type validation
- Minimum subscription amount check
- Ed25519 signature verification (expensive - [validate_investor_signature])
- Remaining accounts validation
- Fee calculation
- AMM [execute_buy_base] CPI call (expensive)
- Asset amount calculation

Finally:  Inside `swap_process()` after checking for slippage &  calculating `liquidity_amount_excluding_fee`, it finally checks that Investor's token balance is greater than liquidity amount, an malicious investor can exploit this ordering of operations and expensive checks to grief operators( becuase operator is signer, he pays for transaction fees) and as the CU raises, the fee is raised too. These many checkes and cpis increase cu heavily. Operator bears this transaction fee cost.

**Impact:** This setup can be used by malicious investors to grief operators by making them pay large transaction fees and making the transaction fail on purpose.

**Recommended Mitigation:** Move the balance check to the beginning of `swap_spl_token_handler` before expensive operations:
```rust
pub fn swap_spl_token_handler<'info>(
    ctx: &Context<'_, '_, '_, 'info, SwapSplToken<'info>>,
    liquidity_amount: u64,
    min_out_amount: u64,
    deadline: i64,
    asset_provider_accounts_count: u8,
    nav_provider_params: &NavProviderParams,
) -> Result<()> {
    let on_ramp_state = &ctx.accounts.on_ramp_state;

    require!(!on_ramp_state.is_paused, SecuritizeOnRampError::Paused);

    // Early balance check - fail fast before expensive operations
    require_gte!(
        ctx.accounts.investor_liquidity_ta.amount,
        liquidity_amount,
        SecuritizeOnRampError::InsufficientBalance
    );

    require!(
        on_ramp_state.asset_token_type == crate::states::TokenType::SplToken,
        SecuritizeOnRampError::InvalidTokenType
    );

    // ...existing code...
```
Note: Also make sure the `investor_asset_ta` is not frozen upfront, otherwise a faulty investor can execute same griefing with his frozen token account(spl token account).

**Securitize:** Acknowledged.
