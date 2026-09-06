---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-06-cyfrin-aztec-logic-module-v2-0-1-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-04-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-06-cyfrin-aztec-logic-module-v2.0.md
tags:
- firm:cyfrin
- report:2026-04-06-cyfrin-aztec-logic-module-v2-0
title: Witness indices in the ACIR logic bridge are only bounds-checked in debug builds
vuln_class: []
---

# Witness indices in the ACIR logic bridge are only bounds-checked in debug builds

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-06-cyfrin-aztec-logic-module-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-06-cyfrin-aztec-logic-module-v2.0.md)_

---

**Description:** `create_logic_gate` passes three witness indices to the builder without any bounds validation:

```cpp
// dsl/acir_format/logic_constraint.cpp:22-27
field_ct left = to_field_ct(a, builder);
field_ct right = to_field_ct(b, builder);

field_ct computed_result = bb::stdlib::logic<Builder>::create_logic_constraint(left, right, num_bits, is_xor_gate);
field_ct acir_result = field_ct::from_witness_index(&builder, result);
computed_result.assert_equal(acir_result);
```

For non-constants, `to_field_ct` stores the index without checking it:

```cpp
// dsl/acir_format/witness_constant.hpp:44-45
return field_ct::from_witness_index(&builder, input.index);
```

When the index is later dereferenced (e.g., `get_value()` during chunking, or `assert_equal` during normalization), it reaches `get_variable()`:

```cpp
// stdlib_circuit_builders/circuit_builder_base.hpp:159-163
inline FF get_variable(const uint32_t index) const
{
    BB_ASSERT_DEBUG(real_variable_index.size() > index);      // compiled out in release
    BB_ASSERT_DEBUG(variables.size() > real_variable_index[index]); // compiled out in release
    return variables[real_variable_index[index]];             // raw OOB if index is bad
}
```

`BB_ASSERT_DEBUG` compiles to nothing under `NDEBUG` (release builds). The normal ACIR parser computes `max_witness_index` from opcodes, so well-formed parsed ACIR stays within bounds. But `create_circuit` sizes the witness array to `max_witness_index + 1` without re-checking every individual index embedded in constraints. A manually constructed or post-parse mutated `AcirFormat` with an index exceeding that bound will silently read out of bounds in release builds.

Not a proof-soundness issue for well-formed parsed ACIR. Malformed in-memory `AcirFormat` structs (direct C++ callers, post-parse mutations, or a parser bug in `max_witness_index` tracking) can trigger out-of-bounds reads in release builds, leading to crashes or garbage witness values.

**Recommended Mitigation:** Validate witness indices against the builder's variable bounds in `to_field_ct` / `from_witness_index` regardless of `NDEBUG`, or promote the debug assertions in `get_variable()` to unconditional checks.

**Aztec:**
Acknowledged, as it will be fixed later. The witness index bounds checks in `get_variable()` use `BB_ASSERT_DEBUG`, which is compiled out in release builds. This is known and it affects every circuit component that calls `get_variable()`, not just the logic gadget. We are discussing this the noir team if it can be exploited in any meaningful way. Regardless, we will enable these asserts in release mode soon after ensuring no significant hit in performance because of the asserts.
