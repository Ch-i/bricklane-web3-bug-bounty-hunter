---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-17
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Fee Prepayment Locked Due to Asset Record Cleanup after `fees_deposit`
vuln_class: []
---

# Fee Prepayment Locked Due to Asset Record Cleanup after `fees_deposit`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** When a user deposits fee prepayment via `fees_deposit`, if the deposit reduces crncy_tokens to zero(right after or later afterwards), the asset record is cleared by `clean_and_check_token_records()`. Later, when the user attempts to withdraw via `fees_withdraw`, the `resolve()` call with `alloc=false` fails to find the asset record, preventing withdrawal of the prepaid fees even though the prepayment amount is still stored in `client_community_state`.

The issue occurs in the following sequence(below is an example):
- In `fees_deposit`: `client_state.sub_crncy_tokens(data.amount)` reduces the currency token balance

```rust
    client_community_state.data[crncy_index].fees_prepayment += data.amount;
    client_state.sub_crncy_tokens(data.amount)?;
```

- In `fees_deposit`: `client_state.clean_and_check_token_records()` is called, which clears asset records when `value == 0`:

```rust
    client_state.clean_and_check_token_records()?;
```

```rust
    pub fn clean_and_check_token_records(&mut self) -> DeriverseResult {
        for r in self.assets.iter_mut() {
            if r.asset_id != 0
                && (r.asset_id & 0xFF000000) != AssetType::SpotOrders as u32
                && (r.asset_id & 0xFF000000) != AssetType::Perp as u32
            {
                match r.value.cmp(&0) {
                    std::cmp::Ordering::Equal => r.asset_id = 0,
                    std::cmp::Ordering::Less => bail!(InsufficientFunds),
                    std::cmp::Ordering::Greater => {}
                }
            }
        }
        Ok(())
    }
```

- In `fees_withdraw`: `client_state.resolve(AssetType::Token, data.token_id, TokenType::Crncy, false)` is called with `alloc=false`

```rust
    client_community_state.update(&mut client_state, &mut community_state, None)?;
    client_state.resolve(AssetType::Token, data.token_id, TokenType::Crncy, false)?;
    let dec_factor = get_dec_factor(community_state.base_crncy[crncy_index].decs_count) as f64;
    let amount = (data.amount as f64 / dec_factor) as i64;
```

- In `find_or_alloc_asset`: When `alloc=false` and the asset record is not found, it returns `AssetNotFound error:`

```rust
        if asset_index == NULL_INDEX {
            realloc = true;
            if !alloc {
                bail!(AssetNotFound {
                    asset_type: asset,
                    id,
                });
            }
```

- The withdrawal fails, even though `fees_prepayment` is still stored in `client_community_state.data[crncy_index].fees_prepayment`

The root cause is that `fees_withdraw` requires `resolve()` to succeed to set the `crncy_tokens` pointer before calling `add_crncy_tokens()`. However, `resolve()` with `alloc=false` cannot recreate the asset record that was cleared after deposit.


**Impact:** Users who deposit fee prepayment that reduces their crncy_tokens to zero(or maybe afterwards) will be unable to withdraw their prepaid fees. They need to deposit again in order to create the `asset`. This requires manual addtional manual operation.

**Recommended Mitigation:** Change `fees_withdraw` to use `alloc=true` when resolving the currency token asset:

```rust
client_state.resolve(AssetType::Token, data.token_id, TokenType::Crncy, true)?;
```

**Deriverse:** Fixed in commit [6662b16](https://github.com/deriverse/protocol-v1/commit/6662b16894ab4462ea9002f355bfd9c9e60784d9).

**Cyfrin:** Verified.
