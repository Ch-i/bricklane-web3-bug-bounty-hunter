---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-08-cyfrin-aztec-polynomial-v2-0-0-6
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
title: '`EvaluationDomain` copy constructor off-by-one for size=2 domains'
vuln_class: []
---

# `EvaluationDomain` copy constructor off-by-one for size=2 domains

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-08-cyfrin-aztec-polynomial-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md)_

---

**Description:** In [`evaluation_domain.cpp:112`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/evaluation_domain.cpp#L112), the copy constructor allocates `round_roots` using the formula `log2_size - 1`:

```cpp
round_roots.resize(log2_size - 1);               // for log2_size=1: resize(0)
inverse_round_roots.resize(log2_size - 1);
round_roots[0] = &roots[0];                      // OOB write when resize(0)!
inverse_round_roots[0] = &roots.get()[size];
for (size_t i = 1; i < log2_size - 1; ++i) {
    round_roots[i] = round_roots[i - 1] + (1UL << i);
    inverse_round_roots[i] = inverse_round_roots[i - 1] + (1UL << i);
}
```

For a size-2 domain ($\log_2(2) = 1$), this resizes to 0 elements, then writes to `round_roots[0]` — an out-of-bounds write on an empty vector (undefined behavior).

The original [`compute_lookup_table_single`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/evaluation_domain.cpp#L43) correctly uses `emplace_back` which always adds at least 1 entry unconditionally, then grows dynamically. But the [copy constructor](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/evaluation_domain.cpp#L90) pre-allocates with the formula `log2_size - 1`, which underestimates by 1 when `log2_size = 1`:

- `log2_size = 1`: original creates 1 entry, copy constructor creates 0 entries (bug)
- `log2_size = 2`: both create 1 entry
- `log2_size = 3`: both create 2 entries

**Impact:** Low. Copying an `EvaluationDomain<Fr>` of size 2 after `compute_lookup_table()` has been called causes undefined behavior. In practice, FFT domains are typically larger (2^10+), but size-2 domains are valid and could appear.

**Proof of Concept:** Integrated test [`AuditPoC_P22_EvalDomainCopyCtorOffByOne`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/polynomial_arithmetic.test.cpp#L599) in `polynomial_arithmetic.test.cpp`:

```cpp
TYPED_TEST(PolynomialTests, AuditPoC_P22_EvalDomainCopyCtorOffByOne)
{
    using FF = TypeParam;

    auto domain = EvaluationDomain<FF>(2);
    domain.compute_lookup_table();

    // Copy the domain — triggers the off-by-one bug:
    // round_roots.resize(log2_size - 1) = resize(0), then writes round_roots[0]
    // This is UB (out-of-bounds write on empty vector)
    auto copied = EvaluationDomain<FF>(domain);
}
```

```bash
cd barretenberg/cpp/build && ninja polynomials_tests
./bin/polynomials_tests --gtest_filter="*AuditPoC_P22*"
```

```
[==========] Running 2 tests from 2 test suites.
[ RUN      ] PolynomialTests/0.AuditPoC_P22_EvalDomainCopyCtorOffByOne
[1]    48511 segmentation fault  ./bin/polynomials_tests --gtest_filter="*AuditPoC_P22*"
```

The test crashes with a segfault, confirming the OOB write on the empty `round_roots` vector.

The formula `log2_size - 1` should be `log2_size` (or `std::max(1UL, log2_size - 1)`) to handle the size=2 case correctly.

**Recommended Mitigation:** In [`evaluation_domain.cpp:112-113`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/evaluation_domain.cpp#L112):

```diff
-        round_roots.resize(log2_size - 1);
-        inverse_round_roots.resize(log2_size - 1);
+        round_roots.resize(std::max(size_t(1), log2_size - 1));
+        inverse_round_roots.resize(std::max(size_t(1), log2_size - 1));
```

**Aztec:**
Fixed in [6cd21a0](https://github.com/AztecProtocol/aztec-packages/commit/6cd21a083ab5620d0ed9800a72f973417f5042b1).

**Cyfrin:** Verified.
