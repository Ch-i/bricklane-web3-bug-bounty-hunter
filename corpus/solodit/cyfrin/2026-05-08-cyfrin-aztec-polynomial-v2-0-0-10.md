---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-08-cyfrin-aztec-polynomial-v2-0-0-10
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
title: '`Polynomial::random(size, start_index)` underflows when `start_index > size`'
vuln_class: []
---

# `Polynomial::random(size, start_index)` underflows when `start_index > size`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-08-cyfrin-aztec-polynomial-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md)_

---

**Description:** The two-argument `Polynomial::random` overload computes the allocation size as `size - start_index`. Both parameters are `size_t` (unsigned), so when `start_index > size`, the subtraction wraps to a near-`SIZE_MAX` value:

```cpp
// polynomial.hpp:274-289
static Polynomial random(size_t size, size_t start_index = 0)
{
    BB_BENCH_NAME("generate random polynomial");
    return random(size - start_index, size, start_index);
    //             ^^^^^^^^^^^^^^^^^^  wraps if start_index > size
}

static Polynomial random(size_t size, size_t virtual_size, size_t start_index)
{
    Polynomial p(size, virtual_size, start_index, DontZeroMemory::FLAG);
    parallel_for_heuristic(
        size,
        [&](size_t i) { p.coefficients_.data()[i] = Fr::random_element(); },
        thread_heuristics::ALWAYS_MULTITHREAD);
    return p;
}
```

The three-argument overload then calls `allocate_backing_memory`, which has its own assertion:

```cpp
BB_ASSERT_LTE(start_index + size, virtual_size);
```

But this assertion is also defeated by unsigned wraparound. For example, `random(4, 10)` computes `size - start_index = 4 - 10 = SIZE_MAX - 5`. Inside `allocate_backing_memory`, the check becomes `10 + (SIZE_MAX - 5) = SIZE_MAX + 5`, which wraps to `4`, and `4 <= 4` passes. The subsequent `BackingMemory::allocate(SIZE_MAX - 5)` attempts a roughly 2^64 byte allocation that fails with `std::bad_alloc`.

The naming is also misleading: in the two-argument form, the `size` parameter actually represents `virtual_size`, not the allocation size. A caller might reasonably write `Polynomial::random(4, /*start_index=*/1)` expecting 4 random elements starting at index 1, but actually gets 3 random elements with `virtual_size=4`.

**Impact:** OOM crash (not silent corruption). The function is used internally with correct arguments. The underflow is caught by the memory allocator throwing `std::bad_alloc`, so no exploitable memory corruption occurs. The issue is a fragile helper API that turns invalid arguments into an attempted huge allocation instead of rejecting them with a clear assertion at the boundary.

**Proof of Concept:**
```cpp
TEST(LowFindings, ECA_08_RandomTwoArgUnderflow)
{
    // random(size=4, start_index=10) computes random(4 - 10, 4, 10).
    //   - 4 - 10 underflows in size_t to SIZE_MAX - 5, requested as the alloc size.
    //   - allocate_backing_memory's internal BB_ASSERT_LTE(start + size, virtual)
    //     also wraps (10 + (SIZE_MAX-5) = SIZE_MAX+5 == 4 in size_t), so the
    //     check passes and does NOT catch the bug.
    //   - The allocator then tries to allocate ~2^64 bytes and throws std::bad_alloc.
    EXPECT_THROW(bb::Polynomial<FF>::random(/*size=*/4, /*start_index=*/10), std::bad_alloc);
}
```

**Recommended Mitigation:** Add a precondition check before the subtraction:

```cpp
static Polynomial random(size_t size, size_t start_index = 0)
{
    BB_ASSERT_GTE(size, start_index);
    return random(size - start_index, size, start_index);
}
```

**Aztec:**
Fixed in [6cd21a0](https://github.com/AztecProtocol/aztec-packages/commit/6cd21a083ab5620d0ed9800a72f973417f5042b1).

**Cyfrin:** Verified.
