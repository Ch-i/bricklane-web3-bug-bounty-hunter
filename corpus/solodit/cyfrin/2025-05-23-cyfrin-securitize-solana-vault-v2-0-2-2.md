---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-23-cyfrin-securitize-solana-vault-v2-0-2-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-05-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-23-cyfrin-securitize-solana-vault-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-23-cyfrin-securitize-solana-vault-v2-0
title: Strict Comparison in Slippage Check Incorrectly Blocks Valid Redemptions
vuln_class: []
---

# Strict Comparison in Slippage Check Incorrectly Blocks Valid Redemptions

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-23-cyfrin-securitize-solana-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-23-cyfrin-securitize-solana-vault-v2.0.md)_

---

**Description:** When checking minimum outcome from the liquidate, we are implementing the check to enforce the returned assets to be more than the minimum amount we put.

> bc-solana-vault-sc/programs/sc-vault/src/instructions/liquidator/liquidate.rs#liquidate_handler
```rust
    if let Some(min_output_amount) = min_output_amount {
>>      require_gt!(
            assets,
            min_output_amount,
            ScVaultError::InsufficientOutputAmount
        );
    }
```

This check is incorrect as if the `assets` equals `min_output_amount`. the tx will revert, but in reaility it should success as the user accepts this value is the minimum value he accepts, but it will be treated as less than desired by the user and revert the tx.

**Impact:** Reverting liquidations that are supposed to pass.

**Recommended Mitigation:** Consider adjusting the check to use `require_gt`.

**Securitize:** Fixed in [de507ba](https://github.com/securitize-io/bc-solana-vault-sc/commit/de507ba56f0181c411902cb23493b7a59b8de777).

**Cyfrin:** Verified
