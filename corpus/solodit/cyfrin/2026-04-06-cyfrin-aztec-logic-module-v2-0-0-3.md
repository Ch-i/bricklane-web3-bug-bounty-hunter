---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-06-cyfrin-aztec-logic-module-v2-0-0-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-04-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-06-cyfrin-aztec-logic-module-v2.0.md
tags:
- firm:cyfrin
- report:2026-04-06-cyfrin-aztec-logic-module-v2-0
title: Constant-only logic constraints spuriously fail in write-VK mode
vuln_class: []
---

# Constant-only logic constraints spuriously fail in write-VK mode

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-06-cyfrin-aztec-logic-module-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-06-cyfrin-aztec-logic-module-v2.0.md)_

---

**Description:** When generating a Verification Key without real witnesses, `create_circuit(...)` zero-fills all witness slots (`dsl/acir_format/acir_format.cpp:203`).
```cpp
const bool is_write_vk_mode = witness.empty();

if (!is_write_vk_mode) {
    BB_ASSERT_EQ(witness.size(),
                 constraints.max_witness_index + 1,
                 "ACIR witness size (" << witness.size() << ") does not match max witness index + 1 ("
                                       << (constraints.max_witness_index + 1) << ").");
} else {
    witness.resize(constraints.max_witness_index + 1, 0);
}
```

For a constant-only logic constraint (e.g., `5 AND 3 = 1`), the stdlib fast path computes the correct result as a constant `field_ct(1)`. But `create_logic_gate` (`dsl/acir_format/logic_constraint.cpp:26-27`) then asserts this constant equals the result witness — which holds the dummy value `0`:

```cpp
field_ct acir_result = field_ct::from_witness_index(&builder, result);  // witness value = 0 (dummy)
computed_result.assert_equal(acir_result);                               // constant 1 != witness 0
```

Since `computed_result` is constant and `acir_result` is a witness, `field_t::assert_equal` (`field.cpp:948-951`) calls `assert_equal_constant()` (`ultra_circuit_builder.hpp:416-420`), which compares the witness value against the constant and calls `builder.failure(msg)` when they don't match.

The ACIR arithmetic constraint handler avoids this by checking `!builder.is_write_vk_mode()` before calling `failure()` (`arithmetic_constraints.cpp:43`). The logic constraint path has no such guard.

**Impact:** VK generation is broken for any circuit containing a constant-only AND/XOR whose result is non-zero. The builder is marked as failed even though the circuit structure is valid and the VK would be correct. Downstream tooling that checks `builder.failed()` will reject the VK or abort the pipeline. This affects availability of VK generation, not proof soundness.

**Recommended Mitigation:** Guard the value-based check in `create_logic_gate` against write-VK mode, matching the arithmetic constraint pattern.

**Aztec:**
Fixed in [a4837fe](https://github.com/AztecProtocol/aztec-packages/commit/a4837fef0294826c391125686cce671199d055f6).

**Cyfrin:** Verified.

\clearpage
