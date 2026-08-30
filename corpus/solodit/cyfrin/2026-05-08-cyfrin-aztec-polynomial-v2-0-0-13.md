---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-08-cyfrin-aztec-polynomial-v2-0-0-13
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-05-08T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-08-cyfrin-aztec-polynomial-v2-0
title: '`Polynomial` defaulted move leaves inconsistent state'
vuln_class: []
---

# `Polynomial` defaulted move leaves inconsistent state

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-08-cyfrin-aztec-polynomial-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md)_

---

**Description:** [`Polynomial`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/polynomial.hpp#L96) uses both a defaulted move constructor and move assignment:

```cpp
Polynomial(Polynomial&& other) noexcept = default;                    // line 96
Polynomial& operator=(Polynomial&& other) noexcept = default;         // line 134
```

Both share the same issue.

`Polynomial` has one member, `coefficients_` of type `SharedShiftedVirtualZeroesArray<Fr>`. That struct also has no custom move, so the compiler-generated move performs:

- **`start_`, `end_`, `virtual_size_`** (`size_t` scalars) — trivially copied, **source unchanged**
- **`backing_memory_`** (contains `shared_ptr<Fr[]>`, `raw_data`, optional `file_backed`) — moved via `BackingMemory`'s move, which correctly nulls source's pointer fields

The result: after move, the source polynomial has `size() > 0` (scalars unchanged), but `data() == nullptr` (backing memory moved out).

A moved-from `Polynomial` looks valid to most accessors:
- `size()` returns the old non-zero value
- `virtual_size()` returns the old value
- `start_index()` / `end_index()` return old values
- `is_empty()` returns `false`

But any attempt to access backed memory (`at()`, `data()[i]`, `operator+=`, etc.) **dereferences nullptr** → segfault or UB.

**Impact:** Low. C++ move semantics say moved-from objects should not be used without reassignment. Careful callers avoid this entirely. The danger is that:

1. A caller accidentally uses a moved-from polynomial (common bug class in C++)
2. The polynomial looks valid via scalar queries (size, virtual_size)
3. The crash happens only on data access, with a misleading null-pointer error

**Proof of Concept:** Integrated death test [`AuditPoC_P50_MovedFromPolynomialCausesSegfault`](https://github.com/AztecProtocol/aztec-packages/blob/d630e5bd77/barretenberg/cpp/src/barretenberg/polynomials/polynomial.test.cpp#L262) in `polynomials/polynomial.test.cpp`. A caller trusts the scalar fields (`size() > 0`) and writes via `src.at(start_index)`, which dereferences the null `data()` pointer and segfaults — demonstrating that the inconsistent moved-from state (`size() > 0` but `data() == nullptr`) is a real crash path, not just a latent state violation.

```cpp
TEST(PolynomialDeathTest, AuditPoC_P50_MovedFromPolynomialCausesSegfault)
{
    using FF = bb::fr;
    using Polynomial = bb::Polynomial<FF>;

    auto use_moved_from = [] {
        auto src = Polynomial::random(10, 16, 2);
        Polynomial moved{ std::move(src) };

        // After move: src.size() == 10 (looks valid), but src.data() == nullptr.
        src.at(2) = FF(5); // dereferences nullptr
    };

    EXPECT_DEATH(use_moved_from(), ".*");
}
```

```bash
cd barretenberg/cpp/build && ninja polynomials_tests
./bin/polynomials_tests --gtest_filter="*AuditPoC_P50*"
```

Observed output:
```
[ RUN      ] PolynomialDeathTest.AuditPoC_P50_MovedFromPolynomialCausesSegfault
[       OK ] PolynomialDeathTest.AuditPoC_P50_MovedFromPolynomialCausesSegfault (9 ms)
```

`EXPECT_DEATH` forks a subprocess, runs the write, and confirms the subprocess terminates abnormally (SIGSEGV).

**Recommended Mitigation:** Fix at the [`SharedShiftedVirtualZeroesArray`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/shared_shifted_virtual_zeroes_array.hpp#L29) layer — replace the implicit defaulted move with an explicit one that zeros the scalar fields. This addresses the root cause and propagates up to every wrapper (not just `Polynomial`):

```cpp
SharedShiftedVirtualZeroesArray(SharedShiftedVirtualZeroesArray&& other) noexcept
    : start_(std::exchange(other.start_, 0))
    , end_(std::exchange(other.end_, 0))
    , virtual_size_(std::exchange(other.virtual_size_, 0))
    , backing_memory_(std::move(other.backing_memory_))
{}

SharedShiftedVirtualZeroesArray& operator=(SharedShiftedVirtualZeroesArray&& other) noexcept {
    if (this != &other) {
        start_         = std::exchange(other.start_, 0);
        end_           = std::exchange(other.end_, 0);
        virtual_size_  = std::exchange(other.virtual_size_, 0);
        backing_memory_ = std::move(other.backing_memory_);
    }
    return *this;
}
```

With this fix, the moved-from `Polynomial` has `size() == 0` and `is_empty() == true` — matching the default-constructed empty state. The invariant `size > 0 → data() != nullptr` is restored.

**Aztec:**
Fixed in [6043f43](https://github.com/AztecProtocol/aztec-packages/commit/cf988ed6f4801af41adab1e98d7d0ff771adb227).

**Cyfrin:** Verified.
