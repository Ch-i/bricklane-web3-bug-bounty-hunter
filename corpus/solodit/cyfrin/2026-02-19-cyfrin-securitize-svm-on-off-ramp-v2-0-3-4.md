---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0-3-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-02-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0
title: Insufficient checks on liquidity amount wastes compute unnecessary
vuln_class: []
---

# Insufficient checks on liquidity amount wastes compute unnecessary

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md)_

---

**Description:** In both `[redeem_ds_token_handler]` and `[redeem_spl_token_handler]`, after computing `[liquidity_amount]` from the NAV rate and asset amount, the code proceeds directly into `[redemption_manager::redeem()]` without first verifying that the liquidity provider's `[source_token_account]` holds sufficient funds (or has sufficient delegated allowance) to fulfill the redemption.

```rust
let liquidity_amount = utils::token_calculator::calculate_liquidity_amount(
    asset_amount,
    rate,
    ctx.accounts.asset_mint.decimals,
    ctx.accounts.liquidity_mint.decimals,
)?;

require_gt!(liquidity_amount, 0, SecuritizeOffRampError::ZeroAmount);

// No check that the liquidity provider can actually fulfill `liquidity_amount`

let (fee_amount, user_supplied_amount) = redemption_manager::redeem(RedemptionParams {
    // ...
})?;
```
In the two-step redemption flow `[execute_two_step_redemption.rs]`, this means the redeemer's asset tokens are first transferred to the`[asset_vault]`, and then the subsequent `[supply_to]` call from the liquidity provider fails due to insufficient balance or delegation. While Solana's transaction atomicity ensures the entire transaction reverts (no funds are lost), the failure occurs deep inside the CPI chain rather than being caught early with a clear error. Which costs the operator or investor unnecessary extra computes

**Impact:** The late failure wastes compute units, produces SPL Token transfer errors instead of a clear InsufficientLiquidity error, and degrades user experience. For operator-mediated SPL token redemptions, repeated late failures can cause signature expiration, forcing the redeemer through the off-chain signing flow again.

**Recommended Mitigation:** Add an early liquidity sufficiency check immediately after computing [liquidity_amount], before calling [redemption_manager::redeem()]. The [liquidity_provider_accounts] (which include the [source_token_account]) are already available at this point:
```rust
let liquidity_amount = utils::token_calculator::calculate_liquidity_amount(
    asset_amount,
    rate,
    ctx.accounts.asset_mint.decimals,
    ctx.accounts.liquidity_mint.decimals,
)?;

require_gt!(liquidity_amount, 0, SecuritizeOffRampError::ZeroAmount);

// Add early liquidity check
let available = off_ramp_state
    .liquidity_provider
    .available_liquidity(off_ramp_state, liquidity_provider_accounts)?;
require_gte!(
    available,
    liquidity_amount,
    SecuritizeOffRampError::InsufficientLiquidity
);

let (fee_amount, user_supplied_amount) = redemption_manager::redeem(RedemptionParams {
    // ...existing code...
})?;
```
**Securitize:** Acknowledged.
