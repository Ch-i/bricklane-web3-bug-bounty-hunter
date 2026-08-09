---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-08-cyfrin-aztec-polynomial-v2-0-0-7
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-05-08T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-08-cyfrin-aztec-polynomial-v2-0
title: '`UnivariateCoefficientBasis` `operator==` compares unused `coefficients[2]`
  for `domain_end=2`'
vuln_class: []
---

# `UnivariateCoefficientBasis` `operator==` compares unused `coefficients[2]` for `domain_end=2`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-08-cyfrin-aztec-polynomial-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md)_

---

**Description:** In [`univariate_coefficient_basis.hpp:87`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/univariate_coefficient_basis.hpp#L87), `operator==` is defaulted:

```cpp
bool operator==(const UnivariateCoefficientBasis& other) const = default;
```

The compiler-generated `= default` compares **all** members, including all 3 elements of `std::array<Fr, 3> coefficients` — even `coefficients[2]`.

For `(domain_end=2, has_a0_plus_a1=false)` objects, `coefficients[2]` is semantically unused (neither an x² coefficient nor a valid Karatsuba precomputation). However, it may contain different values depending on the construction path, causing `operator==` to return `false` for two objects that represent the same polynomial.

Construction paths that leave `coefficients[2]` with different values:

1. [Cross-`has_a0_plus_a1` constructor (line 59)](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/univariate_coefficient_basis.hpp#L59): Copies `[0]` and `[1]` from a `(2, true)` source, does NOT set `[2]` — it is left uninitialized:

```cpp
UnivariateCoefficientBasis(const UnivariateCoefficientBasis<Fr, domain_end, true>& other)
    requires(!has_a0_plus_a1)
{
    coefficients[0] = other.coefficients[0];
    coefficients[1] = other.coefficients[1];
    // coefficients[2] NOT set for domain_end=2 → uninitialized
    if constexpr (domain_end == 3) {
        coefficients[2] = other.coefficients[2];
    }
}
```

2. [Default constructor (line 57)](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/univariate_coefficient_basis.hpp#L57) (`= default`): Leaves the entire array uninitialized for trivial types.

3. Arithmetic operators ([`operator+`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/univariate_coefficient_basis.hpp#L153), [`operator-`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/univariate_coefficient_basis.hpp#L169), etc.): Copy `*this` into `res` (copying whatever `[2]` held), then modify only `[0]` and `[1]`.

During sumcheck, `UnivariateCoefficientBasis<Fr, 2, true>` objects are naturally constructed from Lagrange-basis polynomials with `[2] = a0 + a1` precomputed for Karatsuba. After arithmetic, results become `(2, false)`. Two objects representing the same polynomial can end up with different `[2]` values depending on the construction path:

- **Path A** — [cross-constructor](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/univariate_coefficient_basis.hpp#L59) `(2, true)` → `(2, false)`: copies `[0]` and `[1]`, leaves `[2]` uninitialized
- **Path B** — cross-constructor then [`operator+`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/univariate_coefficient_basis.hpp#L156): `res(*this)` copies all 3 elements including `[2]`, then only updates `[0]` and `[1]`

Both produce the same polynomial, but `[2]` differs → `operator==` returns false.

**Impact:** Low. `operator==` produces false negatives — two objects representing the same polynomial compare as not equal. The `operator==` is currently not called in production code, but `UnivariateCoefficientBasis` is core sumcheck machinery, and equality comparison is a natural operation to add.

The `(2, true)` case is not affected (`coefficients[2] = a₀ + a₁` is deterministic). The `(3, false)` case is also fine (`[2]` is the actual x² coefficient).

**Proof of Concept:** [`AuditPoC_P35_EqualityComparesUnusedCoefficient`](https://github.com/AztecProtocol/aztec-packages/blob/audit/qpzm/barretenberg/cpp/src/barretenberg/polynomials/univariate_coefficient_basis.test.cpp#L56) — builds two `(2, false)` objects with identical `[0]` and `[1]` but different `[2]`, then shows `operator==` returns false:

```cpp
TYPED_TEST(UnivariateCoefficientBasisTest, AuditPoC_P35_EqualityComparesUnusedCoefficient)
{
    // Start from a (2, true) object — as naturally constructed from Univariate (Lagrange basis)
    // P(X) = 5 + 3X, so a0=5, a1=3, a0+a1=8
    UnivariateCoefficientBasis<fr, 2, true> src;
    src.coefficients[0] = fr(5);
    src.coefficients[1] = fr(3);
    src.coefficients[2] = fr(8); // a0 + a1 (Karatsuba precomputation)

    // Path A: cross-constructor (2, true) → (2, false)
    // copies [0] and [1], but does NOT set [2] → uninitialized
    UnivariateCoefficientBasis<fr, 2, false> a(src);

    // Path B: cross-constructor then arithmetic (operator+ copies [2] from *this)
    UnivariateCoefficientBasis<fr, 2, false> b(src);
    UnivariateCoefficientBasis<fr, 2, false> zero;
    zero.coefficients[0] = fr(0);
    zero.coefficients[1] = fr(0);
    b = b + zero; // operator+ copies b's [2] into result via res(*this)

    // Both represent P(X) = 5 + 3X, but [2] may differ
    // BUG: operator== (= default) compares unused [2]
    EXPECT_NE(a, b);
}
```

```bash
cd barretenberg/cpp/build && ninja polynomials_tests
./bin/polynomials_tests --gtest_filter="*P35*"
```

**Recommended Mitigation:** In [`univariate_coefficient_basis.hpp:87`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/univariate_coefficient_basis.hpp#L87), replace `= default` with a custom `operator==` that only compares semantically meaningful coefficients:

```diff
-    bool operator==(const UnivariateCoefficientBasis& other) const = default;
+    bool operator==(const UnivariateCoefficientBasis& other) const
+    {
+        bool eq = (coefficients[0] == other.coefficients[0]) &&
+                  (coefficients[1] == other.coefficients[1]);
+        if constexpr (domain_end == 3 || has_a0_plus_a1) {
+            eq = eq && (coefficients[2] == other.coefficients[2]);
+        }
+        return eq;
+    }
```

**Aztec:**
Fixed in [80131f6](https://github.com/AztecProtocol/aztec-packages/commit/80131f6906d0c5e0ac9f55f2d40a00757899c7c4).

**Cyfrin:** Verified
