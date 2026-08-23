---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-18
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
title: Decimal Mismatch in Fee Prepayment Accounting Causes Incorrect Balance Tracking
vuln_class: []
---

# Decimal Mismatch in Fee Prepayment Accounting Causes Incorrect Balance Tracking

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** There is a critical decimal mismatch between how fee prepayment is stored and withdrawn. In `fees_deposit`, the `fees_prepayment` field stores the raw `data.amount` value (in token's native decimal units), but in `fees_withdraw`, it subtracts `data.amount / dec_factor` (in human-readable units).

This causes severe accounting errors where the stored prepayment balance becomes incorrect after withdrawals, and also leads to incorrect off-chain event logging.

The issue occurs due to inconsistent unit handling:

In `fee_deposit`:
```rust
let prepayment = data.amount as f64 / dec_factor;
...
client_community_state.data[crncy_index].fees_prepayment += data.amount;  // Stores raw value
...
client_state.sub_crncy_tokens(data.amount)?;
```

However, in `fee_withdraw`:

```rust
let amount = (data.amount as f64 / dec_factor) as i64;  // Divides by dec_factor
client_community_state.data[crncy_index].fees_prepayment -= amount;  // Subtracts divided value
```

Example with 6 decimals (dec_factor = 1,000,000):
- User deposits 1 token: `fees_prepayment += 1,000,000 (stored as 1,000,000)`
- User withdraws 1 token: `amount = 1,000,000 / 1,000,000 = 1, fees_prepayment -= 1`
- Result: `fees_prepayment = 999,999` instead of `0`

Additional Issues:
- Event logging mismatch: The log events record `data.amount` (raw value), but the actual withdrawal amount is `data.amount / dec_factor`, causing incorrect off-chain accounting
```rust
    solana_program::log::sol_log_data(&[bytemuck::bytes_of::<FeesWithdrawReport>(
        &FeesWithdrawReport {
            tag: log_type::FEES_WITHDRAW,
            client_id: client_state.id,
            token_id: data.token_id,
            amount: data.amount,
            time: clock.unix_timestamp as u32,
            ..FeesWithdrawReport::zeroed()
        },
    )]);
```

**Workaround: The current implementation has a workaround to multiply the original `data.amount` by `dec_factor`, but this must be validated against `SPOT_MAX_AMOUNT` limits.**

**Impact:**
- Off-chain accounting errors: Event logs show incorrect amounts, causing off-chain systems to track wrong values.
- Original Withdrawal Don't Work: Original `fees_withdraw` doesn't work correctly unless a workaround is being applied.

**Recommended Mitigation:** Use `data.amount`consistently:

```rust
   client_community_state.data[crncy_index].fees_prepayment -= data.amount;  // Use raw value
   ...
   client_state.add_crncy_tokens(data.amount)?;  // Use raw value
```

**Deriverse:** Fixed in commit [1dcab9d](https://github.com/deriverse/protocol-v1/commit/1dcab9df3dc962b79c7a6458da810c36d3397f3e).

**Cyfrin:** Verified.
