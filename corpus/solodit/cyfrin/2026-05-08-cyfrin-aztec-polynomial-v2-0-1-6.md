---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-08-cyfrin-aztec-polynomial-v2-0-1-6
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-05-08T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-08-cyfrin-aztec-polynomial-v2-0
title: '`Polynomial::full()` performs unnecessary double-clone'
vuln_class: []
---

# `Polynomial::full()` performs unnecessary double-clone

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-08-cyfrin-aztec-polynomial-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md)_

---

**Description:** [`Polynomial::full()`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/polynomial.cpp#L242-L247) clones the polynomial's backing memory **twice**. The first clone is immediately discarded by the second:

```cpp
// polynomial.cpp:298
template <typename Fr> Polynomial<Fr> Polynomial<Fr>::full() const
{
    Polynomial result = *this;                                         // ← Clone 1 (wasted)
    result.coefficients_ = _clone(coefficients_, virtual_size() - end_index(), start_index());
                                                                       // ← Clone 2 (the kept one)
    return result;
}
```

`Polynomial` has only one data member: `coefficients_`. So:

1. Line 244 (`Polynomial result = *this;`) invokes the copy constructor, which delegates to [`Polynomial(const Polynomial& other, size_t target_size)`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/polynomial.cpp#L108-L113). That constructor calls `_clone(other.coefficients_, 0)` — a full deep copy of all `other.size()` backed elements (allocation + memcpy).

2. Line 246 (`result.coefficients_ = _clone(...)`) calls `_clone` again on the original `this->coefficients_` and assigns the result. This drops the `shared_ptr` to the line 244 allocation (refcount → 0 → `delete[]`) and installs a new allocation.

The line 244 clone's data is never used. Both the allocation and the memcpy that filled it are wasted.

**Impact:** Informational, but the IPA-prover impact is non-trivial.

`full()` is called only once per IPA prove ([`ipa.hpp:182`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/commitment_schemes/ipa/ipa.hpp#L182)) — but on a polynomial sized to the **circuit size**:

| Circuit size `N` | Wasted alloc + memcpy per IPA prove |
|------------------|-------------------------------------|
| 2^{16} (test bench)  | ~2 MB |
| 2^{20} (typical app circuit) | **~32 MB** |
| 2^{28} (`CONST_SIZE_PROOF_LOG_N` upper bound) | **~8 GB** |

For typical UltraHonk circuits, this is **~32 MB of extra alloc + memcpy + free on every IPA prove** — real memory-bandwidth and allocator pressure on a hot prover path. The fix is a one-line change with zero correctness risk.

The author of `full()` routed through `Polynomial result = *this` (itself going through `_clone` via the copy constructor) and then called `_clone` again directly. Each step looks correct in isolation; the duplication is only visible when both calls are traced together.

**Proof of Concept:** Integrated test [`AuditPoC_P48_FullDoubleClone`](https://github.com/AztecProtocol/aztec-packages/blob/audit/qpzm/barretenberg/cpp/src/barretenberg/polynomials/polynomial.test.cpp#L293) in `polynomials/polynomial.test.cpp`. It compares the time taken by `full()` against a baseline single-clone operation (the copy constructor) on the same-size polynomial:

```cpp
TEST(Polynomial, AuditPoC_P48_FullDoubleClone)
{
    using FF = bb::fr;
    using Polynomial = bb::Polynomial<FF>;

    const size_t SIZE = 1 << 16;  // 65536 elements (~2 MB of Fr data)
    auto poly = Polynomial::random(SIZE, SIZE, 0);

    const int ITERATIONS = 100;

    // Time full() — expected to do TWO clones
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < ITERATIONS; ++i) {
        auto result = poly.full();
        (void)result;
    }
    auto t1 = std::chrono::steady_clock::now();
    auto full_us = std::chrono::duration_cast<std::chrono::microseconds>(t1 - t0).count();

    // Time single-copy via copy constructor — does ONE clone
    auto t2 = std::chrono::steady_clock::now();
    for (int i = 0; i < ITERATIONS; ++i) {
        Polynomial result = poly;
        (void)result;
    }
    auto t3 = std::chrono::steady_clock::now();
    auto single_us = std::chrono::duration_cast<std::chrono::microseconds>(t3 - t2).count();

    const double ratio = static_cast<double>(full_us) / static_cast<double>(single_us);
    EXPECT_GT(ratio, 1.3) << "full() should be noticeably slower due to the extra _clone call";
}
```

Observed output on a release build (M-series Mac):

```
P-48: full()         took 7263 us over 100 iterations
P-48: single-copy    took 3001 us over 100 iterations
P-48: ratio = 2.42x (expected ~2x if double-copy is real)
P-48 CONFIRMED: full() does more work than a single copy — consistent with double-clone
```

A ratio of ~2x is empirical proof that `full()` performs two clones. The slight overshoot above 2.0 is consistent with the extra `new`/`delete` pair from the discarded allocation (allocator overhead beyond the pure memcpy cost).

```bash
cd barretenberg/cpp/build && ninja polynomials_tests
./bin/polynomials_tests --gtest_filter="*AuditPoC_P48*"
```

**Recommended Mitigation:** Skip the first clone by constructing `result` empty, then assigning the one clone we actually need:

```cpp
template <typename Fr> Polynomial<Fr> Polynomial<Fr>::full() const
{
    Polynomial result;   // default-constructed, empty (no allocation)
    result.coefficients_ = _clone(coefficients_, virtual_size() - end_index(), start_index());
    return result;
}
```

`Polynomial` has a default constructor (`= default`) that leaves `coefficients_` in a harmless empty `SharedShiftedVirtualZeroesArray` state (default-initialized members, no allocations). The assignment then installs the only clone we actually want.

This eliminates one `new Fr[size]` + one `memcpy(size * sizeof(Fr))` + one `delete[]` per `full()` call. For size-$2^{20}$ polynomials, that's ~32 MB of saved work.

**Aztec:**
Fixed in [27400b6](https://github.com/AztecProtocol/aztec-packages/commit/27400b680b30b6e3333ac34395b279b8c53bfce6).

**Cyfrin:** Verified.
