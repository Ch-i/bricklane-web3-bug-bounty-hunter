---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-23-cyfrin-securitize-solana-vault-v2-0-2-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-05-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-23-cyfrin-securitize-solana-vault-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-23-cyfrin-securitize-solana-vault-v2-0
title: Unsafe Addition in `convert_to_shares` Causes View Function Inaccuracy
vuln_class: []
---

# Unsafe Addition in `convert_to_shares` Causes View Function Inaccuracy

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-23-cyfrin-securitize-solana-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-23-cyfrin-securitize-solana-vault-v2.0.md)_

---

**Description:** When providing `assets` parameter there is no check if the addition of `total_assets` with `asset` will result in a number greater than `u64::MAX` or not.

```rust
pub fn convert_to_shares(
    assets: u64,
    rate: u64,
    decimals: u8,
    total_assets: u64,
    total_supply: u64,
    rounding: Rounding,
) -> Result<u64> {
    let liq_token_decimals_factor = 10u64.pow(decimals.into());
    let total_shares_after_deposit = math::mul_div(
        rate,
>>      total_assets + assets,
        liq_token_decimals_factor,
        rounding,
    )?;
    ...
}
```

When calling `convert_to_assets_handler`, the asset is provided as input. it is like a `view` function to check the corresponding shares the operator will take for this amount. and this `assets` are added to `total_assets`.

So if he provided `assets` with value that makes `total_assets + assets` goes greater than `U64::MAX` this will result in overflow, leading to incorrect shares returned value for that amount.

This only affects the `view` function and `convert_to_assets_handler` as `deposit_handler` transfers the assets from the depositer (operator) before it, and since supply is `u64` it will not reach the max.


**Impact:** Incorrect return values when calling `convert_to_assets_handler` with large asset amount

**Recommended Mitigation:** Use safe additions in `convert_to_shares`, so that the function revert with overflow if the user provided large asset amount.

**Securitize:** Fixed in [9189e4c](https://github.com/securitize-io/bc-solana-vault-sc/commit/9189e4c3b46956861db1e2efe6cc49b5c0111ca9).

**Cyfrin:** Verified
