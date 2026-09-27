---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-11-17-the-vault-liquid-unstaker-v2-4-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-11-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-11-17-The-Vault-Liquid-Unstaker-V2.md
tags:
- firm:codespect
- report:2025-11-17-the-vault-liquid-unstaker-v2
title: '[I-01] Incosistent flash loan validation'
vuln_class: []
---

# [I-01] Incosistent flash loan validation

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-11-17-The-Vault-Liquid-Unstaker-V2.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-11-17-The-Vault-Liquid-Unstaker-V2.md)_

---

**Files:** [`flash_borrow.rs`](https://github.com/SolanaVault/liquid-unstaker/blob/2dd71f5e3d9017504783c67bc1b903ecaa169a54/programs/liquid-unstaker/src/instructions/flash_borrow.rs#L157)

**Description:**

The `borrow(...)` instructions contains the `verify_flash_repay_instruction_exists(...)` function which validates the `repay(...)` instruction which must be present within the same transaction. One of the validations ensures that the instruction argument of the repayment account is enough to repay the whole loan including fees:

```rust
require!(
    repay_amount >= minimum_repayment,
    LiquidUnstakerErrorCode::FlashLoanRepaymentAmountInsufficient
);
```

A similar validation is present within the repay instruction:

```rust
require!(
    repay_amount == expected_repayment,
    LiquidUnstakerErrorCode::FlashLoanRepaymentAmountInsufficient
);
```

Yet, with a `==` instead of `>=`, which is inconsistent. The borrow validation is less strict than repay, hence it could pass, but the repay would fail.

**Impact:** No security impact. The code would revert later than expected.

**Recommendation:** Implement stricter amount validation on the borrow side with `==`.

**Status:** Fixed

**Update from The Vault:** [ef7a1e4670d835d98592d2feb4142cb94595e5e9](https://github.com/SolanaVault/liquid-unstaker/commit/ef7a1e4670d835d98592d2feb4142cb94595e5e9).
