---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-03-26-tokentable-solana-unlocker-v2-0-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-03-26T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-03-26-TokenTable-Solana-Unlocker-V2.md
tags:
- firm:codespect
- report:2025-03-26-tokentable-solana-unlocker-v2
title: '[M-01] Arithmetic overflow in claim instruction'
vuln_class: []
---

# [M-01] Arithmetic overflow in claim instruction

_Section severity (from Solodit section header): Medium_  
_Audit firm: CODESPECT_  
_Source report: [2025-03-26-TokenTable-Solana-Unlocker-V2.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-03-26-TokenTable-Solana-Unlocker-V2.md)_

---

**Files:** [`claim.rs`](https://github.com/EthSign/tokentable-unlocker-solana/blob/7516b8c86cb305f9d9eb3ac77e7fcd7c6b60cc2f/programs/unlocker-v2-solana/src/instructions/claim.rs#L246)

**Description:**

The `claim` instruction uses the internal function `_simulate_amount_claimable()` to calculate the amount of claimable tokens based on given actual and preset accounts.

When calculating `updated_amount_claimed`, which represents the new amount of claimed tokens, it multiplies two values, which are both 9 decimals big:

```rust
updated_amount_claimed =
  (updated_amount_claimed * actual.total_amount) / BIPS_PRECISION / TOKEN_PRECISION;
```

Provided that the `total_amount` is big enough, the calculation may overflow as it needs to fit into the `u64` variable size before division.

**Impact:** Under certain big enough values representing token amounts, claims will fail.

**Recommendation:** Make the calculations on at least `u128` variable sizes.

**Status:** Fixed

**Update from TokenTable:** Switched to `u128` for calculations in [d7357087b3a46d0c6eed3c240239d35d2f7ddc15](https://github.com/EthSign/tokentable-unlocker-solana/tree/d7357087b3a46d0c6eed3c240239d35d2f7ddc15).
