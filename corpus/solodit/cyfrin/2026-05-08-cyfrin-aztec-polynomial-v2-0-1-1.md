---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-08-cyfrin-aztec-polynomial-v2-0-1-1
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
title: '`set()`, `at()`, and `operator[]` (mutable) use debug-only bounds checks allowing
  silent heap corruption in release'
vuln_class: []
---

# `set()`, `at()`, and `operator[]` (mutable) use debug-only bounds checks allowing silent heap corruption in release

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-08-cyfrin-aztec-polynomial-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md)_

---

**Description:** `SharedShiftedVirtualZeroesArray` provides two classes of accessors. The read-only `get()` method has an explicit runtime bounds check in all builds, while the mutable `set()` and `operator[]` methods guard bounds with `BB_ASSERT_DEBUG`, a macro that compiles to a no-op in release builds (when `NDEBUG` is defined). `Polynomial::at()` delegates directly to `operator[]`, inheriting the same behavior.

The safe read path (`get()`):

```cpp
// shared_shifted_virtual_zeroes_array.hpp, lines 56-64
const T& get(size_t index, size_t virtual_padding = 0) const
{
    static const T zero{};
    BB_ASSERT_DEBUG(index < virtual_size_ + virtual_padding);  // debug-only hint
    if (index >= start_ && index < end_) {                     // ALWAYS runs -- safe
        return data()[index - start_];
    }
    return zero;  // out-of-range returns zero, no memory access
}
```

The unsafe write paths (`set()` and `operator[]`):

```cpp
// shared_shifted_virtual_zeroes_array.hpp, lines 38-43
void set(size_t index, const T& value)
{
    BB_ASSERT_DEBUG(index >= start_);   // compiled out in release
    BB_ASSERT_DEBUG(index < end_);      // compiled out in release
    data()[index - start_] = value;     // executes unconditionally in release
}

// shared_shifted_virtual_zeroes_array.hpp, lines 86-91
T& operator[](size_t index)
{
    BB_ASSERT_DEBUG(index >= start_);   // compiled out in release
    BB_ASSERT_DEBUG(index < end_);      // compiled out in release
    return data()[index - start_];      // executes unconditionally in release
}
```

`Polynomial::at()` delegates to `operator[]`:

```cpp
// polynomial.hpp, line 268
Fr& at(size_t index) { return coefficients_[index]; }
```

When `index < start_`, the expression `index - start_` wraps around because both are `size_t` (unsigned), producing a huge offset. `data()` returns a pointer to the beginning of the allocated buffer, so `data()[huge_offset]` dereferences an address far beyond the allocation, resulting in a wild pointer write. When `index >= end_` but the backing memory is smaller than `end_ - start_` elements, the access is a classic heap buffer overflow.

**Impact:** Silent heap corruption in release builds if any caller passes an out-of-range index to a mutable accessor. The `SharedShiftedVirtualZeroesArray` is only accessed through `Polynomial`, which is expected to maintain correct invariants.

This requires a caller bug or a corrupted polynomial range invariant. No current production call site was identified that intentionally writes out of range, but the release-build failure mode is memory corruption rather than a clean abort.

**Recommended Mitigation:** Promote the mutable-access bounds checks that protect memory safety to always-on `BB_ASSERT`, at least for `set()` and `operator[]`. If profiling shows this is too expensive for hot paths, document the invariant requirement directly on the mutable accessors and add narrow wrapper APIs for checked mutation at call sites where indices are not trivially derived from validated ranges.

**Aztec:**
Acknowledged.
