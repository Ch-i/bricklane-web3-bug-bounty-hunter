---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-08-cyfrin-aztec-polynomial-v2-0-0-1
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
title: '`compute_efficient_interpolation` silently produces wrong output on duplicate
  evaluation points'
vuln_class: []
---

# `compute_efficient_interpolation` silently produces wrong output on duplicate evaluation points

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-08-cyfrin-aztec-polynomial-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md)_

---

**Description:** In [`polynomial_arithmetic.cpp:249`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/polynomial_arithmetic.cpp#L249), `compute_efficient_interpolation` performs Lagrange interpolation from evaluation points and values. When two evaluation points are equal, the Lagrange denominator

$$d_i = \prod_{j \neq i} (x_i - x_j)$$

becomes 0 for the duplicated indices. [`batch_invert`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/polynomial_arithmetic.cpp#L305) skips zero entries, leaving $d_i^{-1} = 0$. The contributions from the duplicated points are silently zeroed out, producing an incorrect interpolation with no error or assertion.

```cpp
// Line 296-301: compute denominators
for (size_t j = 0; j < n; ++j) {
    if (j == i) continue;
    roots_and_denominators[n + i] *= (evaluation_points[i] - evaluation_points[j]);
    // If evaluation_points[i] == evaluation_points[j], this multiplies by 0
    // → d_i = 0 → batch_invert skips → contribution silently zeroed
}

// Line 305: batch invert all denominators (zeros are skipped)
Fr::batch_invert(roots_and_denominators.data(), 2 * n);
```

[`batch_invert`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/ecc/fields/field_impl.hpp#L418) skips zeros by design — when an element is zero, it is excluded from the running product and its result slot is left as 0:

```cpp
// field_impl.hpp:430
if (coeffs[i].is_zero()) {
    skipped[i] = true;     // zero excluded from accumulator
}
```

Other callers (e.g., [barycentric evaluation](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/barycentric.hpp#L151)) legitimately rely on this skip-zero behavior. The fix belongs in `compute_efficient_interpolation` — add a distinct-points assertion before calling `batch_invert`.

**Impact:** Low. Duplicate points make Lagrange interpolation mathematically undefined — this is a precondition violation, not a protocol flaw. All production callers use fixed subgroup domains (`{1, g, ..., g^(n-1)}`), which are distinct by construction. There is no current path for an external actor to supply duplicate points. The assert is a defensive check against future misuse.

**Proof of Concept:** Added [`AuditPoC_P07_InterpolationDuplicatePoints`](https://github.com/AztecProtocol/aztec-packages/blob/audit/qpzm/barretenberg/cpp/src/barretenberg/polynomials/polynomial_arithmetic.test.cpp#L420) to `polynomial_arithmetic.test.cpp`:

```cpp
TYPED_TEST(PolynomialTests, AuditPoC_P07_InterpolationDuplicatePoints)
{
    using FF = TypeParam;

    // Create a known polynomial: f(x) = 3x^2 + 2x + 1
    constexpr size_t n = 3;
    std::array<FF, n> poly = { FF(1), FF(2), FF(3) };

    // Case 1: Distinct points — should interpolate correctly
    {
        std::array<FF, n> x = { FF(1), FF(2), FF(3) };
        std::array<FF, n> src;
        for (size_t i = 0; i < n; i++) {
            src[i] = polynomial_arithmetic::evaluate(poly.data(), x[i], n);
        }
        std::array<FF, n> dest;
        std::copy(src.begin(), src.end(), dest.begin());

        polynomial_arithmetic::compute_efficient_interpolation(dest.data(), dest.data(), x.data(), n);

        bool correct = true;
        for (size_t i = 0; i < n; i++) {
            if (dest[i] != poly[i]) {
                correct = false;
                break;
            }
        }
        std::cout << "P-07 Case 1 (distinct points): interpolation correct = " << correct << std::endl;
        EXPECT_TRUE(correct);
    }

    // Case 2: Duplicate points — should fail but silently produces wrong result
    {
        std::array<FF, n> x = { FF(1), FF(2), FF(2) };  // duplicate!
        std::array<FF, n> src;
        for (size_t i = 0; i < n; i++) {
            src[i] = polynomial_arithmetic::evaluate(poly.data(), x[i], n);
        }
        std::array<FF, n> dest;
        std::copy(src.begin(), src.end(), dest.begin());

        // This should ideally throw or assert, but it silently produces wrong output
        polynomial_arithmetic::compute_efficient_interpolation(dest.data(), dest.data(), x.data(), n);

        bool correct = true;
        for (size_t i = 0; i < n; i++) {
            if (dest[i] != poly[i]) {
                correct = false;
                break;
            }
        }
        std::cout << "P-07 Case 2 (duplicate points): interpolation correct = " << correct << std::endl;
        if (!correct) {
            std::cout << "P-07 CONFIRMED: duplicate points produce wrong interpolation with no error" << std::endl;
        }
        // We expect this to be WRONG — the interpolation is ill-defined for duplicate points
        // The test documents the silent failure behavior
    }
}
```

```bash
cd barretenberg/cpp/build && ninja polynomials_tests
./bin/polynomials_tests --gtest_filter="*AuditPoC_P07*"
```

**Recommended Mitigation:** Add a distinct-points assertion at the start of `compute_efficient_interpolation`.
```cpp
for (size_t i = 0; i < n; ++i)
    for (size_t j = i + 1; j < n; ++j)
        BB_ASSERT(evaluation_points[i] != evaluation_points[j]);
```

O(n²) but not in the hot path — the only production caller is the [`Polynomial` interpolation constructor](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/polynomial.cpp#L123), called once during polynomial construction

**Aztec:**
Fixed in [12f6f61](https://github.com/AztecProtocol/aztec-packages/commit/12f6f61e4ff50bef70b293febec306ae4725f4a0).

**Cyfrin:** Verified.
