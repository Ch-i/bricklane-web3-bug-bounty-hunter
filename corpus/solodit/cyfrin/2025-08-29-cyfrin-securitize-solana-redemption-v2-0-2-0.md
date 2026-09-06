---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-29-cyfrin-securitize-solana-redemption-v2-0-2-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-08-29T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-29-cyfrin-securitize-solana-redemption-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-29-cyfrin-securitize-solana-redemption-v2-0
title: Silent truncation on u128 to u64 cast in liquidity token amount calculator
vuln_class: []
---

# Silent truncation on u128 to u64 cast in liquidity token amount calculator

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-29-cyfrin-securitize-solana-redemption-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-29-cyfrin-securitize-solana-redemption-v2.0.md)_

---

**Description:** The `utils::token_calculator::calculate_liquidity_token_amount` function computes the output in `u128` and returns it with a plain `as u64` cast:
```rust
let result = /* u128 math */;
Ok(result as u64)
```
If `result` fits in `u128` but exceeds `u64::MAX`, the cast truncates the high bits without error. The function then reports a much smaller number than intended. Both the quote path and `redeem` use this helper, so the truncation can silently underpay.

**Impact:** Silent underpayment and wrong accounting.


**Recommended Mitigation:** Replace the lossy cast with a checked conversion:
```rust
use core::convert::TryFrom;

let result_u64 = u64::try_from(result)
    .map_err(|_| SecuritizeOffRampError::Overflow)?;
Ok(result_u64)
```

**Securitize:** Fixed in [7172884](https://github.com/securitize-io/bc-solana-redemption-sc/commit/71728848f7ae01c3b686b343210bd6ae3143ab85).

**Cyfrin:** Verified.


\clearpage
