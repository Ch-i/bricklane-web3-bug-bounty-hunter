---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-23-cyfrin-securitize-solana-vault-v2-0-2-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-05-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-23-cyfrin-securitize-solana-vault-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-23-cyfrin-securitize-solana-vault-v2-0
title: Incorrect Splitting of `remaining_accounts` Causes Misrouting Between NAV and
  Redemption Accounts
vuln_class: []
---

# Incorrect Splitting of `remaining_accounts` Causes Misrouting Between NAV and Redemption Accounts

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-23-cyfrin-securitize-solana-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-23-cyfrin-securitize-solana-vault-v2.0.md)_

---

**Description:** When spliting accounts in `liquidate_handler`, we are assuming that `nav_provider_program` will take the MAX value. where we take  the minimum value from the `MAX_NAV_PROVIDER_ACCOUNTS (5)` and the remaining accounts.

> bc-solana-vault-sc/programs/sc-vault/src/instructions/liquidator/liquidate.rs#liquidate_handler
```rust
    let nav_provider_accounts_count = MAX_NAV_PROVIDER_ACCOUNTS.min(ctx.remaining_accounts.len());
    let (nav_provider_accounts, redemption_accounts) =
        ctx.remaining_accounts.split_at(nav_provider_accounts_count);
```

The problem is that in case of `redemption` is activated, it takes at least `4` accounts.

> bc-solana-vault-sc/programs/sc-vault/src/constants.rs
```rust
pub const MIN_REDEMPTION_ACCOUNTS: usize = 4;
```

So if the liquidator is firing in a vault state where it activate the `redemption` and the nav provider only accepts `1` account as rate. this will result in incorrect splitting, and redemption accounts will goes to nav_provider instead.


**Impact:**
- Reverting liquidate function, resulting in inapility to do the liquidation process

**Proof of Concept:**
- Vault state activate `Redemption`, with minimum accounts required (4)
- Vault state has `NAV Provider program` accepting only one account (minimum).
- The liquidator fired liquidate putting remaining accounts as following: first one is `nav_provider_state`, and the other `4` are for redemption. i.e total 5.
- `nav_provider_accounts_count` will be 5.min(5), i.e 5
- All `5` accounts will goes to `nav_provider_accounts` and no account will goes to `redemption_accounts`
- This will lead to revert the tx when checking `redemption_accounts` aganist minimum as they should be at least of 4 length

**Recommended Mitigation:** Provide the split index as input, so that for `nav_providers` that don't need all `5` accounts, you can make them take the accounts they need. and make redemption accounts with correct values

**Securitize:** Fixed in [ab400a8](https://github.com/securitize-io/bc-solana-vault-sc/commit/ab400a819c6e96a317a1aba151101a930c485995#diff-4f93a9d4b557fd37b8c1471b7327157fcb3c08921e5f2226c38d5981651300b0).

**Cyfrin:** Verified
