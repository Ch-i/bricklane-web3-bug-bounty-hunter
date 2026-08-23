---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-08-cyfrin-aztec-polynomial-v2-0-0-14
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-05-08T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-08-cyfrin-aztec-polynomial-v2-0
title: '`ProverEqPolynomial::construct` fast path does not enforce `challenges.size()
  == log_num_monomials`'
vuln_class: []
---

# `ProverEqPolynomial::construct` fast path does not enforce `challenges.size() == log_num_monomials`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-08-cyfrin-aztec-polynomial-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md)_

---

**Description:** `ProverEqPolynomial::construct()` in `eq_polynomial.hpp` decides between an optimized path (via `GateSeparatorPolynomial::compute_beta_products`) and a fallback (`construct_eq_with_edge_cases`) based on a scaling factor. Only the fallback path asserts the fundamental dimensional precondition `challenges.size() == log_num_monomials` — the fast path has no such check:

```cpp
// eq_polynomial.hpp:56-70
static Polynomial<FF> construct(std::span<const FF> challenges, size_t log_num_monomials)
{
    FF scaling_factor = compute_scaling_factor(challenges);

    if (scaling_factor.is_zero()) {
        return construct_eq_with_edge_cases(challenges, log_num_monomials);
        // construct_eq_with_edge_cases does:
        //   BB_ASSERT_EQ(d, log_num_monomials, "expect log_num_monomials == r.size()");
    }

    // Fast path — no dimension assertion:
    return GateSeparatorPolynomial<FF>::compute_beta_products(
        transform_challenge(challenges), log_num_monomials, scaling_factor);
};
```

Two concrete symptoms follow:

1. **`log_num_monomials < challenges.size()`** — extra challenges are silently discarded. The returned eq-table is not `eq(X, r)` over the full challenge vector; it corresponds to a smaller-dimensional polynomial. For a weighting object over the Boolean hypercube, dropping a dimension changes the polynomial entirely.
2. **`log_num_monomials > challenges.size()` and no `r_i == 1`** — the fast path continues into `compute_beta_products`, where the inner loop walks `betas[current_element_idx]` past the end of the transformed-challenge vector. This is an out-of-bounds read in the consuming helper, reachable only via this public entry point.

The existing issue 16 (`ProverEqPolynomial::construct returns [0] instead of [1] for empty challenges`) is adjacent but strictly narrower — it addresses only the empty-challenge degenerate case, not the general-dimension mismatch on non-empty input.

**Impact:** Current production callers pass matched dimensions. A mismatched internal caller either silently computes the wrong eq-polynomial (soundness-relevant if the output feeds into a sumcheck-style relation) or reads out of bounds in the downstream `compute_beta_products`. The fallback path has the right assertion; the fast path should too.

**Recommended Mitigation:** Hoist the dimension check out of `construct_eq_with_edge_cases` and apply it on both paths:

```cpp
static Polynomial<FF> construct(std::span<const FF> challenges, size_t log_num_monomials)
{
    BB_ASSERT_EQ(challenges.size(), log_num_monomials,
                 "ProverEqPolynomial::construct: challenges.size() must equal log_num_monomials");
    FF scaling_factor = compute_scaling_factor(challenges);
    // ... rest unchanged
}
```

**Aztec:**
Fixed in [80131f6](https://github.com/AztecProtocol/aztec-packages/commit/80131f6906d0c5e0ac9f55f2d40a00757899c7c4) and [19c03f4](https://github.com/AztecProtocol/aztec-packages/commit/19c03f4739bac844350e91357b662b36725dc160).

**Cyfrin:** Verified.

\clearpage
