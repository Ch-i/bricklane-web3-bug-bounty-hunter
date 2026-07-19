---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-08-cyfrin-aztec-polynomial-v2-0-0-9
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
title: '`EvaluationDomain` move-assignment self-assignment permanently destroys lookup
  tables'
vuln_class: []
---

# `EvaluationDomain` move-assignment self-assignment permanently destroys lookup tables

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-08-cyfrin-aztec-polynomial-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md)_

---

**Description:** The `EvaluationDomain<Fr>::operator=(EvaluationDomain&&)` move-assignment operator in `evaluation_domain.cpp` lacks a self-assignment guard. When `domain = std::move(domain)` is executed, the function first destroys its own state and then attempts to read from `other` — which is the same object:

```cpp
// evaluation_domain.cpp:147-172
template <typename Fr> EvaluationDomain<Fr>& EvaluationDomain<Fr>::operator=(EvaluationDomain&& other)
{
    size = other.size;
    generator_size = other.generator_size;
    // ... scalar copies work fine since this == &other ...

    roots = nullptr;                     // (1) destroys this->roots, which IS other.roots
    round_roots.clear();                 // (2) destroys this->round_roots, which IS other.round_roots
    inverse_round_roots.clear();         // (3) destroys this->inverse_round_roots

    if (other.roots != nullptr) {        // (4) always FALSE — we just set it to nullptr at (1)
        roots = other.roots;             //     never reached
        round_roots = std::move(other.round_roots);
        inverse_round_roots = std::move(other.inverse_round_roots);
    }
    other.roots = nullptr;               // (5) redundant — already nullptr
    return *this;
}
```

The sequence is:
1. Line 162: `roots = nullptr` — since `this == &other`, this also nullifies `other.roots`. If this was the last `shared_ptr` reference, the root-of-unity array is deallocated.
2. Lines 163-164: `round_roots.clear(); inverse_round_roots.clear()` — destroys the pointer vectors for both `this` and `other`.
3. Line 165: `if (other.roots != nullptr)` — evaluates to `false` because step 1 already nullified it.
4. All precomputed FFT lookup table data is permanently lost. Any subsequent FFT/IFFT call will crash or produce garbage.

Both `Polynomial::operator=(const Polynomial&)` and `BackingMemory::operator=(BackingMemory&&)` in the same codebase correctly check for self-assignment:

```cpp
// polynomial.cpp:137-144 — correct pattern
template <typename Fr> Polynomial<Fr>& Polynomial<Fr>::operator=(const Polynomial<Fr>& other)
{
    if (this == &other) {
        return *this;
    }
    coefficients_ = _clone(other.coefficients_);
    return *this;
}

// backing_memory.hpp:78-89 — correct pattern
BackingMemory& operator=(BackingMemory&& other) noexcept
{
    if (this != &other) {
        raw_data = other.raw_data;
        // ...
    }
    return *this;
}
```

`EvaluationDomain` is the only move-assignment operator in the module that omits this guard.

**Impact:** Self-move-assignment can occur through generic algorithms (e.g., `container[i] = std::move(container[j])` where `i == j` at runtime), `std::swap` idioms with moved-from temporaries, or standard library operations on containers of `EvaluationDomain` objects. The result is permanent, irrecoverable loss of all precomputed FFT root tables, causing null pointer dereference or incorrect FFT results on subsequent use. Not currently reachable in normal proving flows, but the inconsistency with sibling operators suggests an oversight.

**Recommended Mitigation:** Add the same self-assignment guard used by `Polynomial` and `BackingMemory`:

```cpp
template <typename Fr>
EvaluationDomain<Fr>& EvaluationDomain<Fr>::operator=(EvaluationDomain&& other)
{
    if (this == &other) {
        return *this;
    }
    // ... rest unchanged
}
```

**Aztec:**
Fixed in [80131f6](https://github.com/AztecProtocol/aztec-packages/commit/80131f6906d0c5e0ac9f55f2d40a00757899c7c4).

**Cyfrin:** Verified.
