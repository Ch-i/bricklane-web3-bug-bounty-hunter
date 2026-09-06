---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-08-cyfrin-aztec-polynomial-v2-0-0-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-05-08T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-08-cyfrin-aztec-polynomial-v2-0
title: Interpolation constructor does not assert equal sizes of interpolation points
  and evaluations
vuln_class: []
---

# Interpolation constructor does not assert equal sizes of interpolation points and evaluations

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-08-cyfrin-aztec-polynomial-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md)_

---

**Description:** The interpolation constructor accepts two `std::span` arguments, `interpolation_points` and `evaluations`, and uses the size of `interpolation_points` to determine the polynomial size. It then passes both raw data pointers along with this size to `compute_efficient_interpolation`. There is no assertion or check that `evaluations.size()` is at least as large as `interpolation_points.size()`. If the evaluations span is shorter, the interpolation function reads past the end of the evaluations buffer.

```cpp
// polynomial.cpp, lines 115-125
template <typename Fr>
Polynomial<Fr>::Polynomial(std::span<const Fr> interpolation_points,
                           std::span<const Fr> evaluations,
                           size_t virtual_size)
    : Polynomial(interpolation_points.size(), virtual_size)
{
    BB_ASSERT_GT(coefficients_.size(), static_cast<size_t>(0));

    // evaluations.size() could be < interpolation_points.size() -- no check!
    polynomial_arithmetic::compute_efficient_interpolation(
        evaluations.data(), coefficients_.data(), interpolation_points.data(), coefficients_.size());
}
```

Inside `compute_efficient_interpolation`, the `n` parameter (set to `coefficients_.size()`, which equals `interpolation_points.size()`) is used to index into `src` (the evaluations data pointer) up to index `n-1`:

```cpp
// polynomial_arithmetic.cpp, lines 289-292
for (size_t i = 0; i < n; ++i) {
    roots_and_denominators[i] = -evaluation_points[i];
    temp_src[i] = src[i];     // reads evaluations[i] -- OOB if i >= evaluations.size()
    dest[i] = 0;
```

**Impact:** Out-of-bounds read on the evaluations buffer. The interpolation produces incorrect polynomial coefficients based on whatever data lies beyond the evaluations array.

Current call sites pass matched interpolation/evaluation spans. A mismatched internal call would produce incorrect local proof construction; there is no evidence this would make a verifier accept an invalid proof.

**Proof of Concept:**
```cpp
TEST(LowFindings, ECA_02_InterpolationConstructorMissingSizeCheck)
{
    // Backing buffer of 4 evaluations — but we only intend to pass the first 2.
    std::vector<FF> all_evaluations = { FF(10), FF(20), FF(30), FF(40) };
    std::vector<FF> points = { FF(1), FF(2), FF(3), FF(4) };

    // The "evaluations" span we hand to the constructor is shorter (size 2) than
    // the interpolation points span (size 4).
    std::span<const FF> short_evals(all_evaluations.data(), 2);

    // The constructor uses interpolation_points.size() (=4) as the loop bound
    // inside compute_efficient_interpolation, so it reads evaluations[0..3] from
    // the underlying buffer — past the end of the span we passed.
    auto poly = bb::Polynomial<FF>(points, short_evals, /*virtual_size=*/4);

    // The reconstructed polynomial reproduces ALL FOUR backing values, including
    // the two that lie BEYOND the supplied span. With a proper size assertion
    // those reads should never have happened.
    EXPECT_EQ(poly.evaluate(FF(1)), FF(10));
    EXPECT_EQ(poly.evaluate(FF(2)), FF(20));
    EXPECT_EQ(poly.evaluate(FF(3)), FF(30)); // <-- read PAST evaluations.size()
    EXPECT_EQ(poly.evaluate(FF(4)), FF(40)); // <-- read PAST evaluations.size()
}
```

**Recommended Mitigation:** Add a size assertion at the top of the constructor body:

```cpp
BB_ASSERT_EQ(interpolation_points.size(), evaluations.size());
```

**Aztec:**
Fixed in [80131f6](https://github.com/AztecProtocol/aztec-packages/commit/80131f6906d0c5e0ac9f55f2d40a00757899c7c4).

**Cyfrin:** Verified.
