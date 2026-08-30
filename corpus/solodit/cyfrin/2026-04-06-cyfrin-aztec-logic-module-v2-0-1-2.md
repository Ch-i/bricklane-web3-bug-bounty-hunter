---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-06-cyfrin-aztec-logic-module-v2-0-1-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-04-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-06-cyfrin-aztec-logic-module-v2.0.md
tags:
- firm:cyfrin
- report:2026-04-06-cyfrin-aztec-logic-module-v2-0
title: Operator Precedence Bug in DSL Logic Constraint Test Input
vuln_class: []
---

# Operator Precedence Bug in DSL Logic Constraint Test Input

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-06-cyfrin-aztec-logic-module-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-06-cyfrin-aztec-logic-module-v2.0.md)_

---

**Description:** In [`dsl/acir_format/logic_constraint.test.cpp:76-77`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/dsl/acir_format/logic_constraint.test.cpp#L76-L77), the test creates input values with a misleading comment:

```cpp
bb::fr lhs = FF(static_cast<uint256_t>(1) << num_bits - 1); // All bits from 0 to num_bits-1 are set
bb::fr rhs = FF(static_cast<uint256_t>(1) << num_bits - 1); // All bits from 0 to num_bits-1 are set
```

Due to C++ operator precedence, `-` binds tighter than `<<`, so `1 << num_bits - 1` evaluates as `1 << (num_bits - 1)`. This produces a single-bit value (only bit `num_bits-1` set), not an all-bits-set value.

The comment says "All bits from 0 to num_bits-1 are set", which would require `(1 << num_bits) - 1`.

| num_bits | Comment intent: `(1 << num_bits) - 1` | Actual: `1 << (num_bits - 1)` |
|----------|--------------------------------------|-------------------------------|
| 1 | `0b1` = 1 | `0b1` = 1 (same by coincidence) |
| 16 | `0b1111111111111111` = 65535 | `0b1000000000000000` = 32768 |
| 128 | `0xFFFF...FFFF` (128 bits) | `0x8000...0000` (1 bit set) |
| 252 | `0xFFF...FFF` (252 bits) | `0x800...000` (1 bit set) |

Since `lhs == rhs` in both cases, XOR always produces 0 and AND always produces `lhs`. This means the test only exercises:
- A single-bit input pattern (sparse), not an all-bits-set pattern (dense)
- XOR result always 0, AND result always equals input

The intended all-bits-set pattern would test the maximum value in range, which is a more interesting boundary case for the range constraints.

**Impact:** Informational. The test still exercises a valid input and passes. However, the test coverage is weaker than intended: the all-bits-set boundary case (maximum value within num_bits range) is not tested.

**Proof of Concept:** All 128 DSL logic constraint tests pass with the current (misleading) values:

```
$ ./bin/dsl_tests --gtest_filter="*LogicConstraint*"
[==========] 128 tests from 64 test suites ran. (1776 ms total)
[  PASSED  ] 128 tests.
```

Test matrix: 4 constancy modes (None, Input1, Input2, Both) × 4 num_bits (1, 16, 128, 252) × 2 operations (AND, XOR) × 2 builders (Ultra, Mega) × 2 test types (VK, Tampering) = 128 tests.

**Recommended Mitigation:** Fix the expression to match the comment — test the all-bits-set value:

```cpp
bb::fr lhs = FF((static_cast<uint256_t>(1) << num_bits) - 1); // All bits from 0 to num_bits-1 are set
bb::fr rhs = FF((static_cast<uint256_t>(1) << num_bits) - 1); // All bits from 0 to num_bits-1 are set
```

**Aztec:**
Fixed in [2a597fb](https://github.com/AztecProtocol/aztec-packages/commit/2a597fb73b75f71ef7ddfd579eee8f749996dd67).

**Cyfrin:** Verified.
