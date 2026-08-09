---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-2-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Casting from `u64` to `i64` causes genuine deposit requests to fail in `deposit`
  function
vuln_class: []
---

# Casting from `u64` to `i64` causes genuine deposit requests to fail in `deposit` function

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The `deposit` function in `deposit.rs` casts the amount value( the amount of tokens trader is willing to deposit) which is of type `u64` to `i64` when `deposit_all` is set to `true`. When token amounts exceed `i64::MAX` (9,223,372,036,854,775,807), the cast wraps around to negative values due to Rust's default overflow behavior in release builds. The amount is later cast back to u64 for SPL token transfers, however we have this check before casting it back up to `u64`
```rust
    if !(1..=SPOT_MAX_AMOUNT).contains(&amount) {
        bail!(InvalidQuantity {
            value: amount,
            min_value: 1,
            max_value: SPOT_MAX_AMOUNT,
        });
    }
```
here the goal is to put lower and upper bound on the amount between 1 & 36028797018963967, since we have casted the amount from `u64` to `i64`, if the amount was big, It might have turned to a negative number and this negative number does not lie in the desired range, so the transaction does not go through.

**Impact:** Genuine transactions especially for large token decimal mints may get reverted.

**Proof of Concept:**
```rust
fn main() {
    let a: i64;

    let b: u64 = 15_000_000_000_000_000_000;

    a = b as i64;  // Casting

    println!("a = {}", a);  //
}
Output: a = -3446744073709551616
```

**Recommended Mitigation:** Don't convert input amount to `i64` instead we can do this
```rust
const SPOT_MAX_AMOUNT_U64: u64 = SPOT_MAX_AMOUNT as u64;
```
**Deriverse:** Fixed in commit [801209](https://github.com/deriverse/protocol-v1/commit/801209dc5d425dd0a3177d4a41660e0e4ed91bda)

**Cyfrin:** Verified.
