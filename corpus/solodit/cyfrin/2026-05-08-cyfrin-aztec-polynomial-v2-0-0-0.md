---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-08-cyfrin-aztec-polynomial-v2-0-0-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-05-08T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-08-cyfrin-aztec-polynomial-v2-0
title: '`factor_roots` masks remainder — silent wrong result on violated precondition'
vuln_class: []
---

# `factor_roots` masks remainder — silent wrong result on violated precondition

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-08-cyfrin-aztec-polynomial-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md)_

---

**Description:** In [`polynomial_arithmetic.hpp:56`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/polynomial_arithmetic.hpp#L56), `factor_roots` performs synthetic division assuming $(X - r) \mid p(X)$. After the division loop, it unconditionally zeroes the final coefficient:

```cpp
polynomial[size - 1] = Fr::zero();  // unconditionally zeroes the leading coefficient slot
```
https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/polynomial_arithmetic.hpp#L107

The division loop (lines 99-105) computes quotient coefficients $b_0, \ldots, b_{n-2}$ in-place, storing the last value in `temp`. It never touches `polynomial[size-1]`, which still holds the original $a_{n-1}$. For exact division, $a_{n-1} = b_{n-2}$ (i.e., `polynomial[size-1] == temp`). When the precondition is violated, these differ — but line 107 unconditionally zeroes the slot without checking, silently producing a wrong quotient with no indication of error.

**Impact:** Low. Called 7 times in proof-critical path (all prover-side). All callers correctly satisfy the precondition — KZG subtracts the evaluation before quotienting, Shplonk/Gemini evaluations are computed from the polynomial itself, and Merge prover evaluations are derived directly. A failure requires a future trusted-caller bug (not external input), and the result would be verifier rejection, not a soundness break. The assert costs 1 field comparison and would make such a bug fail loudly instead of silently.

**All 7 call sites (prover only):**

1. [`kzg/kzg.hpp:56`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/commitment_schemes/kzg/kzg.hpp#L56) — KZG Prover
   - Root: `pair.challenge`
   - Precondition: `quotient.at(0) -= pair.evaluation`
2. [`shplonk/shplonk.hpp:77`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/commitment_schemes/shplonk/shplonk.hpp#L77) — Shplonk Prover
   - Root: `-claim.opening_pair.challenge`
   - Precondition: `tmp.at(0) -= gemini_fold_pos_evaluations[fold_idx]`
3. [`shplonk/shplonk.hpp:86`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/commitment_schemes/shplonk/shplonk.hpp#L86) — Shplonk Prover
   - Root: `claim.opening_pair.challenge`
   - Precondition: `tmp.at(0) -= claim.opening_pair.evaluation`
4. [`shplonk/shplonk.hpp:102`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/commitment_schemes/shplonk/shplonk.hpp#L102) — Shplonk Prover (Libra)
   - Root: `claim.opening_pair.challenge`
   - Precondition: `tmp.at(0) -= claim.opening_pair.evaluation`
5. [`shplonk/shplonk.hpp:114`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/commitment_schemes/shplonk/shplonk.hpp#L114) — Shplonk Prover (Sumcheck)
   - Root: `claim.opening_pair.challenge`
   - Precondition: `tmp.at(0) -= claim.opening_pair.evaluation`
6. [`goblin/merge_prover.cpp:84`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/goblin/merge_prover.cpp#L84) — Merge Prover
   - Root: `kappa`
   - Precondition: `shplonk_batched_quotient.at(0) -= challenge * eval` (in loop)
7. [`goblin/merge_prover.cpp:91`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/goblin/merge_prover.cpp#L91) — Merge Prover
   - Root: `kappa_inv`
   - Precondition: `reversed_batched_left_tables_copy.at(0) -= evals.back()`


**Proof of Concept:** [`AuditPoC_P17_FactorRootsMasksRemainder`](https://github.com/AztecProtocol/aztec-packages/blob/audit/qpzm/barretenberg/cpp/src/barretenberg/polynomials/polynomial_arithmetic.test.cpp#L375) — saves the original $a_{n-1}$ before calling `factor_roots`, then compares it with $b_{n-2}$ (`poly[n-2]` after the call). For exact division these match; for violated preconditions they differ, which is exactly what our proposed assert catches.

```cpp
TYPED_TEST(PolynomialTests, AuditPoC_P17_FactorRootsMasksRemainder)
{
    using FF = TypeParam;

    constexpr size_t n = 3;

    // Case 1: Exact division — p(X) = X^2 - 1 = (X-1)(X+1), root = 1
    {
        std::array<FF, n> poly = { -FF(1), FF(0), FF(1) }; // [-1, 0, 1]
        FF original_leading = poly[n - 1];                  // a_{n-1} = 1

        polynomial_arithmetic::factor_roots(std::span<FF>(poly), FF(1));

        // After division: poly[n-2] = b_{n-2} (last quotient coeff)
        // For exact division: a_{n-1} == b_{n-2}
        FF b_last = poly[n - 2];
        EXPECT_EQ(original_leading, b_last);
    }

    // Case 2: Non-exact division — p(X) = X^2 + 1, root = 1, p(1) = 2 ≠ 0
    {
        std::array<FF, n> poly = { FF(1), FF(0), FF(1) }; // [1, 0, 1]
        FF original_leading = poly[n - 1];                 // a_{n-1} = 1

        FF eval_at_root = polynomial_arithmetic::evaluate(poly.data(), FF(1), n);
        EXPECT_NE(eval_at_root, FF(0));

        polynomial_arithmetic::factor_roots(std::span<FF>(poly), FF(1));

        // After division: a_{n-1} ≠ b_{n-2} — proposed assert catches this
        FF b_last = poly[n - 2];
        EXPECT_NE(original_leading, b_last);
    }
}
```

```bash
cd barretenberg/cpp/build && ninja polynomials_tests
./bin/polynomials_tests --gtest_filter="*AuditPoC_P17*"
```

```
P-17 Case 1 (exact): a_{n-1}=..01, b_{n-2}=..01       → proposed assert PASSES
P-17 Case 2 (non-exact): a_{n-1}=..01, b_{n-2}=..p-1   → proposed assert CATCHES non-divisibility
```

**Recommended Mitigation:** Replace [`polynomial_arithmetic.hpp:107`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/polynomial_arithmetic.hpp#L107):

```diff
- polynomial[size - 1] = Fr::zero();
+ BB_ASSERT(polynomial[size - 1] == temp);  // verify a_{n-1} == b_{n-2} (exact divisibility)
+ polynomial[size - 1] = Fr::zero();
```

**Aztec:**
Fixed in [80131f6](https://github.com/AztecProtocol/aztec-packages/commit/80131f6906d0c5e0ac9f55f2d40a00757899c7c4).

**Cyfrin:** Verified.
