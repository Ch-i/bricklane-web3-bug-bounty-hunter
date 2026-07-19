---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-08-cyfrin-aztec-polynomial-v2-0-1-0
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
title: '`SharedShiftedVirtualZeroesArray` invariant enforcement gap'
vuln_class: []
---

# `SharedShiftedVirtualZeroesArray` invariant enforcement gap

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-08-cyfrin-aztec-polynomial-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md)_

---

**Description:** In [`shared_shifted_virtual_zeroes_array.hpp`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/shared_shifted_virtual_zeroes_array.hpp), the struct requires the invariant `start_ <= end_ <= virtual_size_`, but this is never validated:

1. No constructor checks the invariant — aggregate initialization allows any values
2. `Polynomial::shrink_end_index` checks the upper bound but not the lower:

```cpp
// polynomial.cpp:236
void Polynomial<Fr>::shrink_end_index(const size_t new_end_index)
{
    BB_ASSERT_LTE(new_end_index, end_index());   // checks: new <= current end
    coefficients_.end_ = new_end_index;            // NO check: new >= start_
}
```

If `new_end_index < start_`, then `size()` (= `end_ - start_`) underflows to `SIZE_MAX` because both are `size_t` (unsigned). This corrupts all size-dependent operations.

**Impact:** Informational. All current callers use `shrink_end_index` correctly. If misused, the `SIZE_MAX` underflow would crash immediately (not silently produce wrong results). The assert is a code hygiene suggestion.

**Proof of Concept:** [`AuditPoC_P15_ShrinkEndIndexUnderflow`](https://github.com/AztecProtocol/aztec-packages/blob/audit/qpzm/barretenberg/cpp/src/barretenberg/polynomials/polynomial_arithmetic.test.cpp#L485) — creates a polynomial with `start_index=2`, then calls `shrink_end_index(1)`. The current check passes (`1 <= 10`) but `end_ < start_` causes `size()` to underflow. With our fix, the assert would catch it.

```cpp
TEST(AuditPoC, P15_ShrinkEndIndexUnderflow)
{
    using FF = bb::fr;

    // Create a polynomial with start_index=2: coefficients at indices [2..9], virtual_size=16
    auto poly = Polynomial<FF>(8, 16, /*start_index=*/2);
    EXPECT_EQ(poly.start_index(), 2UL);
    EXPECT_EQ(poly.end_index(), 10UL);
    EXPECT_EQ(poly.size(), 8UL);

    // shrink_end_index(1): passes current check (1 <= 10) but violates start_ <= end_
    poly.shrink_end_index(1);

    // end_ = 1, start_ = 2 → size() = 1 - 2 = SIZE_MAX (unsigned underflow)
    EXPECT_EQ(poly.end_index(), 1UL);
    EXPECT_EQ(poly.size(), SIZE_MAX);

    // With fix: BB_ASSERT_GTE(new_end_index, start_index()) would catch 1 < 2
}
```

```bash
cd barretenberg/cpp/build && ninja polynomials_tests
./bin/polynomials_tests --gtest_filter="*P15*"
```

```
P-15: start=2 end=1 size=18446744073709551615
P-15 CONFIRMED: size() underflows to SIZE_MAX
```

**Recommended Mitigation:** Add lower bound check at [`polynomial.cpp:238`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/polynomials/polynomial.cpp#L238):

```diff
  BB_ASSERT_LTE(new_end_index, end_index());
+ BB_ASSERT_GTE(new_end_index, start_index());
  coefficients_.end_ = new_end_index;
```

**Aztec:**
Fixed in [80131f6](https://github.com/AztecProtocol/aztec-packages/commit/80131f6906d0c5e0ac9f55f2d40a00757899c7c4).

**Cyfrin:** Verified.
