---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-08-cyfrin-aztec-polynomial-v2-0-1-5
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-05-08T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-08-cyfrin-aztec-polynomial-v2-0
title: '`UnivariateCoefficientBasis` loses Karatsuba precomputation after arithmetic'
vuln_class: []
---

# `UnivariateCoefficientBasis` loses Karatsuba precomputation after arithmetic

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-08-cyfrin-aztec-polynomial-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md)_

---

**Description:** In [`univariate_coefficient_basis.hpp`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/univariate_coefficient_basis.hpp), all arithmetic operators ([`operator+`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/univariate_coefficient_basis.hpp#L153), [`operator-`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/univariate_coefficient_basis.hpp#L169), [`operator+=`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/univariate_coefficient_basis.hpp#L90), [`operator-=`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/univariate_coefficient_basis.hpp#L105), scalar operations) return `UnivariateCoefficientBasis<Fr, domain_end, false>` — unconditionally resetting `has_a0_plus_a1` to `false`. This discards the precomputed `a0 + a1` value stored in `coefficients[2]`, even when the result could preserve it cheaply.

```cpp
// operator+ always returns has_a0_plus_a1 = false
template <size_t other_domain_end, bool other_has_a0_plus_a1>
UnivariateCoefficientBasis<Fr, domain_end, false> operator+(
    const UnivariateCoefficientBasis<Fr, other_domain_end, other_has_a0_plus_a1>& other) const
{
    UnivariateCoefficientBasis<Fr, domain_end, false> res(*this);
    res.coefficients[0] += other.coefficients[0];
    res.coefficients[1] += other.coefficients[1];
    // coefficients[2] NOT updated for domain_end=2
    // → precomputed (a0+a1) is lost even though (a0'+a1') = (a0+a1) + (b0+b1)
    return res;
}
```

The in-place operators have the same issue — they skip `coefficients[2]` when `domain_end=2`:

```cpp
// operator+= also returns has_a0_plus_a1 = false
UnivariateCoefficientBasis<Fr, domain_end, false>& operator+=(...)
{
    coefficients[0] += other.coefficients[0];
    coefficients[1] += other.coefficients[1];
    if constexpr (other_domain_end == 3 && domain_end == 3) {
        coefficients[2] += other.coefficients[2];
    }
    // coefficients[2] NOT updated for domain_end=2
    return *this;
}
```

When both operands are `(domain_end=2, has_a0_plus_a1=true)`, the precomputation is preservable for all four operators:

```
operator+/+=:
  this:  a0, a1, (a0+a1)
  other: b0, b1, (b0+b1)
  result: (a0+b0), (a1+b1), (a0+a1)+(b0+b1) = (a0+b0)+(a1+b1) ← correct!

operator-/-=:
  result: (a0-b0), (a1-b1), (a0+a1)-(b0+b1) = (a0-b0)+(a1-b1) ← correct!
```

But the return type is hardcoded to `false`, so downstream `operator*` cannot use the (T,T) Karatsuba branch and must recompute `a0+a1` from scratch.

**Impact:** Informational (performance). In Sumcheck's inner loop, `UnivariateCoefficientBasis` operations are executed per-gate, per-relation, per-round. The Karatsuba optimization saves 1 field addition per degree-1 multiplication by using the precomputed `a0+a1`.

For relation patterns like `(wire_a + wire_b) * wire_c`:

```
1. wire_a, wire_b, wire_c: converted from Lagrange → (2, true), a0+a1 free
2. wire_a + wire_b → (2, false), Karatsuba precomputation LOST
3. result * wire_c → hits (F,T) branch, recomputes a0+a1 (+1 addition)
```

If step 2 preserved `has_a0_plus_a1=true`, step 3 would use the cheaper (T,T) branch.

**Proof of Concept:** Measured benchmark:

Integrated benchmark [`AuditPoC.P33_AddThenMultiplyKaratsubaPath`](https://github.com/AztecProtocol/aztec-packages/blob/audit/qpzm/barretenberg/cpp/src/barretenberg/polynomials/univariate_coefficient_basis.test.cpp#L142) in `polynomials/univariate_coefficient_basis.test.cpp`. The test simulates the realistic Sumcheck pattern `(wire_a + wire_b) * wire_c` for 200k iterations:

- Current: `a + b` returns `(2, false)` (precomputation discarded), so `(a+b) * c` takes the (F,T) Karatsuba branch.
- Optimized: manually preserve `a0+a1` in the sum (what the recommended fix would do automatically), so `(a+b) * c` takes the (T,T) branch.

```cpp
TEST(AuditPoC, P33_AddThenMultiplyKaratsubaPath)
{
    constexpr size_t N = 200000;
    std::vector<UnivariateCoefficientBasis<fr, 2, true>> A(N), B(N), C(N);
    // ... fill each with random (a0, a1) and coefficients[2] = a0 + a1

    // Current: (A + B) returns (2, false), so * falls into the (F, T) branch.
    auto t0 = high_resolution_clock::now();
    for (size_t i = 0; i < N; ++i) {
        auto sum = A[i] + B[i];           // has_a0_plus_a1 = false
        auto out = sum * C[i];            // (F, T) Karatsuba branch
    }
    auto t1 = high_resolution_clock::now();

    // Optimized: reconstruct the sum as (2, true) with coefficients[2] preserved → (T, T).
    for (size_t i = 0; i < N; ++i) {
        UnivariateCoefficientBasis<fr, 2, true> sum;
        sum.coefficients[0] = A[i].coefficients[0] + B[i].coefficients[0];
        sum.coefficients[1] = A[i].coefficients[1] + B[i].coefficients[1];
        sum.coefficients[2] = A[i].coefficients[2] + B[i].coefficients[2];  // a0'+a1'
        auto out = sum * C[i];            // (T, T) Karatsuba branch
    }
    auto t2 = high_resolution_clock::now();
}
```

```
P-33 N=200000:  current ((F,T) chain) = 33.3 ns/op   optimized ((T,T) chain) = 30.2 ns/op   saved = 9.5%
```

Per-`(add + mul)` pattern saved: ~3 ns. The 9.5% is the realistic per-pattern speedup, not the upper bound — it includes the `+` operation cost as well.

**Recommended Mitigation:** Template the return type to preserve `has_a0_plus_a1=true` when both inputs are `(2, true)`:

```cpp
template <size_t other_domain_end, bool other_has_a0_plus_a1>
auto operator+(const UnivariateCoefficientBasis<Fr, other_domain_end, other_has_a0_plus_a1>& other) const
{
    constexpr bool preserve = (domain_end == 2 && other_domain_end == 2
                               && has_a0_plus_a1 && other_has_a0_plus_a1);
    UnivariateCoefficientBasis<Fr, domain_end, preserve> res;
    res.coefficients[0] = coefficients[0] + other.coefficients[0];
    res.coefficients[1] = coefficients[1] + other.coefficients[1];
    if constexpr (other_domain_end == 3 && domain_end == 3) {
        res.coefficients[2] = coefficients[2] + other.coefficients[2];
    } else if constexpr (preserve) {
        res.coefficients[2] = coefficients[2] + other.coefficients[2];
    }
    return res;
}
```

Similar changes needed for `operator-`, `operator+=`, `operator-=`. Profiling recommended before applying.

**Aztec:**
Acknowledged.
