---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-29-cyfrin-securitize-solana-redemption-v2-0-3-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-08-29T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-29-cyfrin-securitize-solana-redemption-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-29-cyfrin-securitize-solana-redemption-v2-0
title: Missing Liquidity Vault Balance Validation
vuln_class: []
---

# Missing Liquidity Vault Balance Validation

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-29-cyfrin-securitize-solana-redemption-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-29-cyfrin-securitize-solana-redemption-v2.0.md)_

---

**Description:** In `withdraw_liquidity_handler`, liquidity tokens are transferred from `liquidity_token_vault` to the withdrawer’s associated token account. While the instruction checks that the withdrawal amount is greater than zero and that the system is not paused, it does not validate whether the vault actually holds at least `amount` tokens before attempting the transfer.
This omission may allow withdrawal attempts that exceed the available vault balance, leading to failed transactions or unintended program behavior depending on the token program implementation.

**Impact:** If the vault contains fewer tokens than requested, the transfer may fail at runtime, causing unnecessary transaction failures.

**Recommended Mitigation:** Add a balance check to ensure that `liquidity_token_vault.amount >= amount` before executing the transfer.

```diff
+ let liquidity_vault = &ctx.accounts.liquidity_token_vault;
+    require_gte!(
+      liquidity_vault.amount,
+      amount,
+    SecuritizeOffRampError::InsufficientLiquidity
+);
```


**Securitize:** Fixed in [3163cd9](https://github.com/securitize-io/bc-solana-redemption-sc/commit/3163cd9a818e0d83222d9cc74edbd6a4e4fa2d1c).

**Cyfrin:** Verified.

\clearpage
