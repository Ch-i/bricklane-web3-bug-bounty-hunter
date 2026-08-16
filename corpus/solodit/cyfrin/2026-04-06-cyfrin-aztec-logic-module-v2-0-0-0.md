---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-06-cyfrin-aztec-logic-module-v2-0-0-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-04-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-06-cyfrin-aztec-logic-module-v2.0.md
tags:
- firm:cyfrin
- report:2026-04-06-cyfrin-aztec-logic-module-v2-0
title: Malformed ACIR logic constraints can throw or hard-abort instead of failing
  the circuit normally
vuln_class: []
---

# Malformed ACIR logic constraints can throw or hard-abort instead of failing the circuit normally

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-06-cyfrin-aztec-logic-module-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-06-cyfrin-aztec-logic-module-v2.0.md)_

---

**Description:** `create_logic_gate(...)` in `dsl/acir_format/logic_constraint.cpp` forwards `num_bits` and constant operands directly into `logic<Builder>::create_logic_constraint(...)`.
```cpp
template <typename Builder>
void create_logic_gate(Builder& builder,
                       const WitnessOrConstant<bb::fr> a,
                       const WitnessOrConstant<bb::fr> b,
                       const uint32_t result,
                       const size_t num_bits,
                       const bool is_xor_gate)
{
    using field_ct = bb::stdlib::field_t<Builder>;

    field_ct left = to_field_ct(a, builder);
    field_ct right = to_field_ct(b, builder);

    field_ct computed_result = bb::stdlib::logic<Builder>::create_logic_constraint(left, right, num_bits, is_xor_gate);
    field_ct acir_result = field_ct::from_witness_index(&builder, result);
    computed_result.assert_equal(acir_result);
}
```

The logic gadget enforces `0 < num_bits <= 252` and constant-operand bit bounds with `BB_ASSERT_*` in `stdlib/primitives/logic/logic.cpp`, rather than through a builder-failure path. Those assertions route through `common/assert.hpp`, `common/assert.cpp`, and `env/throw_or_abort_impl.cpp`, which means malformed logic constraints throw in exception-enabled builds and abort the process in `BB_NO_EXCEPTIONS` builds.

```cpp
// ensure the number of bits doesn't exceed field size and is not negative
BB_ASSERT_LTE(num_bits, grumpkin::MAX_NO_WRAP_INTEGER_BIT_LENGTH);
BB_ASSERT_GT(num_bits, 0U);

if (a.is_constant() && b.is_constant()) {
    uint256_t a_native = static_cast<uint256_t>(a.get_value());
    uint256_t b_native = static_cast<uint256_t>(b.get_value());
    BB_ASSERT_LTE(
        a_native.get_msb(), num_bits - 1, "field_t: Left operand in logic gate exceeds specified bit length");
    BB_ASSERT_LTE(
        b_native.get_msb(), num_bits - 1, "field_t: Right operand in logic gate exceeds specified bit length");

```

```cpp
// Native implementation of throw_or_abort
extern "C" void throw_or_abort_impl [[noreturn]] (const char* err)
{

#ifdef STACKTRACES
    // Use backward library to print stack trace
    backward::StackTrace trace;
    trace.load_here(32);
    backward::Printer{}.print(trace);
#endif
#ifndef BB_NO_EXCEPTIONS
    throw std::runtime_error(err);
#else
    abort_with_message(err);
#endif
}
```

**Impact:** Malformed or untrusted ACIR logic opcodes can terminate circuit construction at the host level instead of producing a normal unsatisfied-constraint result or explicit rejected-opcode error. This is an availability and robustness issue. The worst case is `BB_NO_EXCEPTIONS`, where the same path becomes a hard process abort.

**Recommended Mitigation:** Validate `LogicConstraint` inputs in the ACIR layer before calling the stdlib gadget. Downgrade malformed `num_bits` and constant-operand violations to builder failure or explicit rejected-opcode errors, rather than relying on host-level assertions in the logic gadget.

**Aztec:**
Acknowledged, It is true that `create_logic_constraint` uses `BB_ASSERT` (which aborts) rather than throwing an exception when `num_bits` is invalid. `BB_ASSERT` is the standard pattern throughout barretenberg for structural invariant checks. Additionally, the `num_bits` value originates from Noir's `IntegerBitSize` enum, which restricts values to {1, 8, 16, 32, 64, 128} at the compiler level, so invalid values cannot reach this code through normal operation.
