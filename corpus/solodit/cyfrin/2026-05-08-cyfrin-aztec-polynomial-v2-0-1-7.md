---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-08-cyfrin-aztec-polynomial-v2-0-1-7
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-05-08T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-08-cyfrin-aztec-polynomial-v2-0
title: scalar `operator*=` unnecessarily restricted by `requires(!has_a0_plus_a1)`
vuln_class: []
---

# scalar `operator*=` unnecessarily restricted by `requires(!has_a0_plus_a1)`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-08-cyfrin-aztec-polynomial-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md)_

---

**Description:** In [`univariate_coefficient_basis.hpp:232`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/univariate_coefficient_basis.hpp#L232), `operator*=(const Fr& scalar)` has a `requires(!has_a0_plus_a1)` constraint that prevents it from being called on `(domain_end=2, has_a0_plus_a1=true)` objects:

```cpp
UnivariateCoefficientBasis<Fr, domain_end, false>& operator*=(const Fr& scalar)
    requires(!has_a0_plus_a1)   // ← unnecessarily restrictive
{
    coefficients[0] *= scalar;
    coefficients[1] *= scalar;
    if constexpr (domain_end == 3) {
        coefficients[2] *= scalar;
    }
    return *this;
}
```

Unlike `operator+=` and `operator-=` with scalars — where the constraint IS necessary because adding/subtracting a scalar changes `a₀` without changing `a₁`, invalidating the precomputed `a₀ + a₁` — scalar multiplication scales all coefficients uniformly:

```
Before: a₀, a₁, (a₀ + a₁)
After:  s·a₀, s·a₁, s·(a₀ + a₁) = s·a₀ + s·a₁  ← still valid!
```

Comparison of scalar operators:

| Operator | `requires(!has_a0_plus_a1)` justified? | Reason |
|----------|----------------------------------------|--------|
| [`operator+=(scalar)`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/univariate_coefficient_basis.hpp#L219) | **Yes** | `a₀` changes, `a₁` doesn't → `a₀+a₁` invalidated |
| [`operator-=(scalar)`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/univariate_coefficient_basis.hpp#L226) | **Yes** | Same as above |
| [`operator*=(scalar)`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/univariate_coefficient_basis.hpp#L232) | **No** | All terms scale by `s` → `s·(a₀+a₁)` still valid |

The same issue applies to the non-in-place [`operator*(const Fr& scalar)`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/univariate_coefficient_basis.hpp#L257) which returns `has_a0_plus_a1=false` and does not scale `coefficients[2]`.

**Impact:** Informational. This is a conservative design choice that simplifies the type system. The performance impact is the same as [issue-22](https://github.com/AztecProtocol/aztec-packages/issues/22): downstream `operator*` falls into a more expensive Karatsuba branch when the precomputation has been discarded.

**Proof of Concept:** Measured benchmark:

Integrated benchmark [`AuditPoC.P34_KaratsubaTTvsFFBranch`](https://github.com/AztecProtocol/aztec-packages/blob/audit/qpzm/barretenberg/cpp/src/barretenberg/polynomials/univariate_coefficient_basis.test.cpp#L65) in `polynomials/univariate_coefficient_basis.test.cpp`. The test directly compares the cost of the (T,T) Karatsuba branch (which P-34 unlocks downstream) against the (F,F) branch (which the current code is forced into after a scalar `*=` strips the precomputation):

```cpp
TEST(AuditPoC, P34_KaratsubaTTvsFFBranch)
{
    constexpr size_t N = 200000;
    std::vector<UnivariateCoefficientBasis<fr, 2, true>>  lhs_T(N), rhs_T(N);
    std::vector<UnivariateCoefficientBasis<fr, 2, false>> lhs_F(N), rhs_F(N);
    // ... fill both representations with the same random (a0, a1) / (b0, b1)
    //     — the (2, true) copies additionally set coefficients[2] = a0 + a1.

    // (T, T) — the cheap branch P-34 would unlock by removing the `requires` gate.
    auto t0 = high_resolution_clock::now();
    for (size_t i = 0; i < N; ++i) {
        auto r = lhs_T[i] * rhs_T[i];     // (T, T) Karatsuba branch
    }
    auto t1 = high_resolution_clock::now();

    // (F, F) — what the current code is forced into once a scalar `*=` strips the flag.
    for (size_t i = 0; i < N; ++i) {
        auto r = lhs_F[i] * rhs_F[i];     // (F, F) Karatsuba branch
    }
    auto t2 = high_resolution_clock::now();
}
```

```
P-34 N=200000:  (T,T) Karatsuba = 25.6 ns/op   (F,F) Karatsuba = 29.7 ns/op   (F,F) overhead = 13.7%
```

Per-multiplication cost difference: ~4 ns (one extra field addition). The 13.7% overhead is the upper bound on what the P-34 fix would save for any multiplication chain that currently goes through (F,F) because of an intervening scalar `*=`.

**Recommended Mitigation:** Remove the `requires` constraint and preserve `has_a0_plus_a1`:

```diff
- UnivariateCoefficientBasis<Fr, domain_end, false>& operator*=(const Fr& scalar)
-     requires(!has_a0_plus_a1)
+ UnivariateCoefficientBasis& operator*=(const Fr& scalar)
  {
      coefficients[0] *= scalar;
      coefficients[1] *= scalar;
      if constexpr (domain_end == 3) {
          coefficients[2] *= scalar;
+     } else if constexpr (has_a0_plus_a1) {
+         coefficients[2] *= scalar;  // preserve a₀+a₁ precomputation
      }
      return *this;
  }
```

**Aztec:**
Acknowledged.

\clearpage
