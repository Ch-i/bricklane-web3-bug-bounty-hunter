---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-23-cyfrin-securitize-solana-vault-v2-0-3-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-05-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-23-cyfrin-securitize-solana-vault-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-23-cyfrin-securitize-solana-vault-v2-0
title: Invalid Zero Rate Not Rejected During Deposit
vuln_class: []
---

# Invalid Zero Rate Not Rejected During Deposit

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-23-cyfrin-securitize-solana-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-23-cyfrin-securitize-solana-vault-v2.0.md)_

---

**Description:** When despoiting assets, and convert the shares to be minted to the despositer we are not checking the validity of rate value (weather it is greater zero or not)

> bc-solana-vault-sc/programs/sc-vault/src/utils/conversions.rs#convert_to_shares
```rust
pub fn convert_to_shares( ... ) -> Result<u64> {
    let liq_token_decimals_factor = 10u64.pow(decimals.into());
    let total_shares_after_deposit = math::mul_div(
>>      rate,
        total_assets + assets,
        liq_token_decimals_factor,
        rounding,
    )?;

    if total_shares_after_deposit >= total_supply {
        Ok(total_shares_after_deposit - total_supply)
    } else {
        Ok(0)
    }
}
```

This is not the case when redeeming where we check that the rate value is greater than zero

> bc-solana-vault-sc/programs/sc-vault/src/utils/conversions.rs#convert_to_assets
```rust
pub fn convert_to_assets( ... ) -> Result<u64> {
    if total_supply == 0 {
        return Ok(0);
    }
>>  require_gt!(rate, 0, ScVaultError::InvalidRate);
    let liq_token_decimals_factor = 10u64.pow(decimals.into());
    Ok(u64::min(
        math::mul_div(shares, liq_token_decimals_factor, rate, rounding)?,
        math::mul_div(shares, total_assets, total_supply, rounding)?,
    ))
}
```

This will make `total_shares_after_deposit` ends being `0`, results in minting `0` shares to the depositer (operator).

**Impact:**
- In case of incorrect return value from RedStone, the operator will take `0` shares

**Recommended Mitigation:** Check that `rate` is greater than `0`
```diff
pub fn deposit_handler<'info>( ... ) -> Result<()> {
    ...
    // Get rate from nav provider.
    let rate = get_rate!(ctx.remaining_accounts, ctx.accounts.nav_provider_program);
+   require_gt!(rate, 0, ScVaultError::InvalidRate);
    ...
    let shares = conversions::convert_to_shares( ... )?;

    ...
}

```

**Securitize:** Fixed in [2764f90](https://github.com/securitize-io/bc-solana-vault-sc/commit/2764f902d8cf3cfcf202eab1c78d16c48c7ef150).

**Cyfrin:** Verified
