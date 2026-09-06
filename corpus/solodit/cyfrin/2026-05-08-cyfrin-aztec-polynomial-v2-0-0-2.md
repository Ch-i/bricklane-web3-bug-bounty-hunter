---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-08-cyfrin-aztec-polynomial-v2-0-0-2
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
title: '`evaluate_mle` crashes (SIGSEGV) on single-coefficient polynomial'
vuln_class: []
---

# `evaluate_mle` crashes (SIGSEGV) on single-coefficient polynomial

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-08-cyfrin-aztec-polynomial-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md)_

---

**Description:** In [`polynomial.hpp:399`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/polynomial.hpp#L399), `_evaluate_mle` unconditionally accesses `evaluation_points[0]` without checking if the span is empty:

```cpp
Fr_ _evaluate_mle(std::span<const Fr_> evaluation_points,
                  const SharedShiftedVirtualZeroesArray<Fr_>& coefficients,
                  bool shift)
{
    if (coefficients.size() == 0) {
        return Fr_(0);
    }
    const size_t n = evaluation_points.size();                        // n = 0
    const size_t dim = numeric::get_msb(coefficients.end_ - 1) + 1;  // dim = get_msb(0) + 1 = 1
    // ...
    size_t n_l = 1 << (dim - 1);                                     // n_l = 1
    // ...
    Fr_ u_l = evaluation_points[0];   // OOB: span is empty!
```

For a `Polynomial(1)` (single coefficient, virtual_size=1), calling `evaluate_mle({})` with an empty evaluation point vector causes:
1. `n = 0` (no evaluation points)
2. `dim = get_msb(0) + 1 = 1` (from `coefficients.end_ = 1`)
3. `n_l = 1 << 0 = 1` (one iteration expected)
4. `evaluation_points[0]` -- out-of-bounds read on empty span, **SIGSEGV**

A single-coefficient polynomial represents a constant (a 0-variable multilinear polynomial). Evaluating it at an empty point set should return the constant value.

**Impact:** Low. `evaluate_mle` is a public API on `Polynomial` that crashes (SIGSEGV) on valid input — a single-coefficient polynomial with an empty evaluation point vector. In practice, sumcheck and other MLE consumers always work with polynomials of size ≥ 2, so `evaluation_points` is never empty. But the function has no guard, and a caller constructing a single-element polynomial would hit undefined behavior with no indication of the cause.

**Proof of Concept:** Integrated test [`AuditPoC_P27_EvaluateMleSingleCoefficientCrash`](https://github.com/AztecProtocol/aztec-packages/blob/audit/qpzm/barretenberg/cpp/src/barretenberg/polynomials/polynomial_arithmetic.test.cpp#L511) in `polynomial_arithmetic.test.cpp`:

```cpp
TYPED_TEST(PolynomialTests, AuditPoC_P27_EvaluateMleSingleCoefficientCrash)
{
    using FF = TypeParam;

    Polynomial<FF> poly(1);
    poly.at(0) = FF(42);

    // 0-variable MLE: empty evaluation points, should return the constant 42
    std::vector<FF> u; // empty
    // This crashes with SIGSEGV — _evaluate_mle accesses evaluation_points[0] on empty span
    FF result = poly.evaluate_mle(u);
    EXPECT_EQ(result, FF(42));
}
```

```bash
cd barretenberg/cpp/build && ninja polynomials_tests
./bin/polynomials_tests --gtest_filter="*AuditPoC_P27*"
```

```
[  DEATH  ] Exit code 139 (SIGSEGV)
```

Crashes with SIGSEGV — `_evaluate_mle` accesses `evaluation_points[0]` on an empty span.

**Recommended Mitigation:** Add after [`polynomial.hpp:411`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/polynomial.hpp#L411):

```diff
  const size_t n = evaluation_points.size();
+ if (n == 0) {
+     return coefficients.size() > 0 ? coefficients.get(0) : Fr_(0);
+ }
  const size_t dim = numeric::get_msb(coefficients.end_ - 1) + 1;
```

**Aztec:**
Fixed in [780139e](https://github.com/AztecProtocol/aztec-packages/commit/780139e06d813e38d0f8a92a05c5ec99faeb46cf).

**Cyfrin:** Verified.
