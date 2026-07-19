---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-08-cyfrin-aztec-polynomial-v2-0-0-11
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-05-08T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-08-cyfrin-aztec-polynomial-v2-0
title: '`ProverEqPolynomial::construct` returns `[0]` instead of `[1]` for empty challenges'
vuln_class: []
---

# `ProverEqPolynomial::construct` returns `[0]` instead of `[1]` for empty challenges

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-08-cyfrin-aztec-polynomial-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md)_

---

**Description:** When `ProverEqPolynomial::construct()` is called with an empty challenges vector (`d=0`), the mathematically expected result is the constant polynomial `[1]` (the empty product equals 1). The function first computes the scaling factor:

```cpp
// eq_polynomial.hpp:56-70
static Polynomial<FF> construct(std::span<const FF> challenges, size_t log_num_monomials)
{
    FF scaling_factor = compute_scaling_factor(challenges);
    // For empty challenges: scaling_factor = 1 (empty product), non-zero

    if (scaling_factor.is_zero()) {
        return construct_eq_with_edge_cases(challenges, log_num_monomials);
        // This fallback handles d=0 correctly: loop doesn't execute, returns [1]
    }

    // Optimal path — delegates to GateSeparatorPolynomial (out of scope)
    return GateSeparatorPolynomial<FF>::compute_beta_products(
        transform_challenge(challenges), log_num_monomials, scaling_factor);
};
```

For empty challenges:
1. `compute_scaling_factor({})` returns `1` (the empty product of `(1 - r_i)` terms).
2. Since `1 != 0`, the optimal path is taken, calling `GateSeparatorPolynomial::compute_beta_products({}, 0, 1)`.
3. This out-of-scope function hits its `betas.empty()` early return, which creates a size-1 polynomial initialized to `0` and ignores the `scaling_factor = 1` argument.

The `compute_scaling_factor` and `transform_challenge` for empty input:

```cpp
// eq_polynomial.hpp:80-88
static FF compute_scaling_factor(std::span<const FF> challenge)
{
    FF out(1);
    const FF one(1);
    for (auto u_i : challenge) {   // empty loop — no iterations
        out *= (one - u_i);
    }
    return out;   // returns 1
}

// eq_polynomial.hpp:101-116
static std::vector<FF> transform_challenge(std::span<const FF> challenges)
{
    std::vector<FF> result;         // empty
    std::vector<FF> denominators;   // empty
    for (const auto& challenge : challenges) { ... }   // empty loop
    FF::batch_invert(denominators);  // no-op on empty vector
    // ...
    return result;   // empty vector
}
```

The fallback path (`construct_eq_with_edge_cases`) would handle `d=0` correctly — its loop doesn't execute and it returns `[1]`. But the optimal path is chosen because `scaling_factor = 1` is non-zero, and the downstream function discards the scaling factor.

**Impact:** Only affects `d=0`, which is a degenerate case. Sumcheck requires at least `d=1`, so this is not reachable in normal protocol execution. The bug is technically in `GateSeparatorPolynomial::compute_beta_products` (out of scope), but manifests through the `ProverEqPolynomial` public interface. It is an incorrect public helper result for the mathematically valid empty-product case.

**Proof of Concept:**
```cpp
TEST(LowFindings, ECA_10_ProverEqPolynomialEmptyChallengesReturnsZero)
{
    std::vector<FF> empty_challenges;
    auto result = bb::ProverEqPolynomial<FF>::construct(empty_challenges, /*log_num_monomials=*/0);

    ASSERT_EQ(result.size(), 1u);

    // Mathematically eq(X, r) with d=0 is the empty product, which equals 1.
    // BUG: GateSeparatorPolynomial::compute_beta_products({}, 0, scaling_factor=1)
    // hits its betas.empty() early return and produces Polynomial(1)=[0],
    // ignoring the scaling_factor. So the public helper returns [0] instead of [1].
    EXPECT_EQ(result.get(0), FF(0));
    // Expected after fix:
    //   EXPECT_EQ(result.get(0), FF(1));
}
```

**Recommended Mitigation:** Add a guard at the top of `construct`:

```cpp
static Polynomial<FF> construct(std::span<const FF> challenges, size_t log_num_monomials)
{
    if (challenges.empty()) {
        Polynomial<FF> result(1, 1);
        result.at(0) = FF(1);
        return result;
    }
    // ... rest unchanged
}
```

Alternatively, fix `GateSeparatorPolynomial::compute_beta_products` to respect the `scaling_factor` argument when `betas` is empty.

**Aztec:**
Fixed in [87513f8](https://github.com/AztecProtocol/aztec-packages/commit/87513f8bffb880276c560bea2d8c540a8fa94945).

**Cyfrin:** Verified.
