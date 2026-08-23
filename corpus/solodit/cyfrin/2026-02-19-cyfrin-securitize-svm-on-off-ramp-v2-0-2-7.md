---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0-2-7
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-02-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0
title: Allowance Liquidity Provider Uses `delegated_amount` Without Capping by Actual
  Balance
vuln_class: []
---

# Allowance Liquidity Provider Uses `delegated_amount` Without Capping by Actual Balance

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md)_

---

**Description:** For `AllowanceLiquidityProvider`, `available_liquidity` returns the source token account’s `delegated_amount` only.

```rust
        let source_token_account =
            TokenAccount::try_deserialize(&mut &source_token_account_info.data.borrow()[..])?;

        require_keys_eq!(
            source_token_account.delegate.unwrap_or_default(),
            expected_delegate.key(),
            SecuritizeOffRampError::InvalidLiquidityProviderConfiguration
        );

        Ok(source_token_account.delegated_amount)
```

 In SPL Token, `delegated_amount` is not reduced when tokens are transferred out of the account after approval via `self-transfer`. Thus the reported “available liquidity” can exceed the account’s current balance. This leads to inflated liquidity visibility and redemptions that can fail at transfer time when the LP’s balance is lower than the reported allowance.

```rust
                if !self_transfer {
                    source_account.delegated_amount = source_account
                        .delegated_amount
                        .checked_sub(amount)
                        .ok_or(TokenError::Overflow)?;
                    if source_account.delegated_amount == 0 {
                        source_account.delegate = COption::None;
                    }
                }
```

In addition, `calculate_effective_liquidity_amount` returns the requested amount unchanged and does not consider the real token balance or available liquidity.


**Impact:**
- **Incorrect liquidity reporting**: Off-ramp and integrators may show “available liquidity” equal to `delegated_amount` even when the LP’s balance is lower, e.g. after the LP transferred tokens elsewhere.
- **Failed redemptions**: Users or operators may initiate redemptions for amounts that then fail at transfer because the source account has insufficient balance. This causes failed transactions and poor UX (and can be seen as a form of DoS for those redemption attempts).

**Recommended Mitigation:** Cap `available_liquidity` by current balance, return something like `Ok(source_token_account.delegated_amount.saturating_min(source_token_account.amount))`.

**Securitize:** Fixed in [cdd059f](https://github.com/securitize-io/bc-solana-on-off-ramp-sc/commit/cdd059f8d883c827f0e6ae14dcfe9067a32d082f).

**Cyfrin:** Verified.
