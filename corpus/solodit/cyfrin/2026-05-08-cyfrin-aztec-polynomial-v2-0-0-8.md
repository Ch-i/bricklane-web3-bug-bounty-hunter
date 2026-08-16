---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-08-cyfrin-aztec-polynomial-v2-0-0-8
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-05-08T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-08-cyfrin-aztec-polynomial-v2-0
title: Signed integer overflow in `_evaluate_mle` bit-shift expressions
vuln_class: []
---

# Signed integer overflow in `_evaluate_mle` bit-shift expressions

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-08-cyfrin-aztec-polynomial-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-08-cyfrin-aztec-polynomial-v2.0.md)_

---

**Description:** The `_evaluate_mle` function in `polynomial.hpp` uses the integer literal `1` (type `int`, 32-bit signed) as the left operand of the left-shift operator `<<` in three places:

```cpp
// polynomial.hpp:415
BB_ASSERT_EQ(coefficients.virtual_size(), static_cast<size_t>(1 << n));

// polynomial.hpp:421
size_t n_l = 1 << (dim - 1);

// polynomial.hpp:448
n_l = 1 << (dim - l - 1);
```

Per the C++ standard ([expr.shift]/1), shifting a signed integer by an amount greater than or equal to its bit-width, or shifting into the sign bit, is undefined behavior. When `n >= 31`, the expression `1 << n` overflows a 32-bit signed `int`. Concretely:

- `1 << 31` produces `INT_MIN` (-2147483648) in two's complement.
- `static_cast<size_t>(INT_MIN)` then sign-extends to `0xFFFFFFFF80000000` on a 64-bit system, which is NOT `2^31`.
- The assertion on line 415 spuriously fails, or worse, a conforming compiler is entitled to optimize away the entire check because the expression involves UB.

The same issue affects the buffer size computation on line 421 and the loop variable on line 448. If `dim >= 32`, these produce garbage values that control loop bounds and allocation sizes.

The codebase already uses the correct `1UL << d` pattern elsewhere, for instance in `eq_polynomial.hpp`:

```cpp
// eq_polynomial.hpp:145 — correct pattern
const size_t N = 1UL << d;
```

The three occurrences in `_evaluate_mle` are inconsistent with this established convention.

**Impact:** For circuits with 2^31 or more rows, MLE evaluation silently produces incorrect results or crashes. The current maximum circuit size is `CONST_SIZE_PROOF_LOG_N = 28`, so this is not reachable today. However, the trend in proving systems is toward larger circuits, and this is actual C++ undefined behavior — the compiler is not required to produce any particular result, and optimizations based on UB assumptions can silently break seemingly unrelated code.

**Recommended Mitigation:** Replace the signed `1` literal with `size_t(1)` in all three locations:

```cpp
// Line 415
BB_ASSERT_EQ(coefficients.virtual_size(), size_t(1) << n);

// Line 421
size_t n_l = size_t(1) << (dim - 1);

// Line 448
n_l = size_t(1) << (dim - l - 1);
```

**Aztec:**
Fixed in [87513f8](https://github.com/AztecProtocol/aztec-packages/commit/87513f8bffb880276c560bea2d8c540a8fa94945).

**Cyfrin:** Verified.
