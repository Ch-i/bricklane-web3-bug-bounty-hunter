---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-3-16
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Withdraw Instruction Trying to Create New Asset Records for Non-Existent Tokens
  Instead of Failing
vuln_class: []
---

# Withdraw Instruction Trying to Create New Asset Records for Non-Existent Tokens Instead of Failing

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The `withdraw` instruction uses `alloc=true` when resolving the token asset, which tries the creation of a new asset record with zero balance if the token doesn't exist, instead of immediately failing with an appropriate error. While the transaction eventually fails, this behavior wastes account space and violates the semantic expectation that withdrawals should only operate on existing assets.

In `withdraw.rs`, the resolve function is called with `alloc=true`:

```rust
client_state.resolve(AssetType::Token, data.token_id, TokenType::Asset, true)?;
```

When `find_or_alloc_asset `is called with `alloc=true` and the asset doesn't exist in `client_primary`, it:
- Creates a new asset record with asset_id set to the token ID
- Initializes the balance to 0
- Potentially reallocates the account if no free slot is available

Subsequently, `sub_asset_tokens(data.amount)` is called, which subtracts the withdrawal amount from 0, resulting in a negative balance. The check then fails with InsufficientFunds.

```rust
    client_state.sub_asset_tokens(data.amount)?;
    if client_state.asset_tokens()? < 0 {
        bail!(InsufficientFunds);
    }
```

This is semantically incorrect because:
- Withdrawals should only operate on existing assets with positive balances


Note:

In some cases, the `finalize_spot` will be called in `clean_generic`.
```rust
    if accounts.len() > 11 + extra_accounts {
        client_state.clean_generic(accounts_iter, accounts.len() - 11 - extra_accounts)?;
    }
```

But the asset record will be created anyway in `clean_generic`:

```rust
            self.resolve_instr(client_infos_acc, false)?;
```

So, we don't ever need to put `alloc=true`:
```rust
    if accounts.len() > 11 + extra_accounts {
        client_state.clean_generic(accounts_iter, accounts.len() - 11 - extra_accounts)?;
    }
    client_state.resolve(AssetType::Token, data.token_id, TokenType::Asset, true)?;
```

**Impact:** The instruction should fail immediately if the token doesn't exist, not create a record first.

**Recommended Mitigation:** Change the `alloce` to `false`
```rust
client_state.resolve(AssetType::Token, data.token_id, TokenType::Asset, false)?;
```

**Deriverse:** Fixed in commit [45ee168](https://github.com/deriverse/protocol-v1/commit/45ee1680acdf605aeb52796f7d5f29d169d1a7e5).

**Cyfrin:** Verified.
