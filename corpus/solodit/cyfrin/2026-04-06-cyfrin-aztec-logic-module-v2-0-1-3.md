---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-06-cyfrin-aztec-logic-module-v2-0-1-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-04-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-06-cyfrin-aztec-logic-module-v2.0.md
tags:
- firm:cyfrin
- report:2026-04-06-cyfrin-aztec-logic-module-v2-0
title: Redundant Range Constraints Between ACIR and Logic Gate
vuln_class: []
---

# Redundant Range Constraints Between ACIR and Logic Gate

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-06-cyfrin-aztec-logic-module-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-06-cyfrin-aztec-logic-module-v2.0.md)_

---

**Description:** When a Noir circuit uses a bitwise operation like `a: u8 ^ b: u8`, the Noir compiler emits both range checks and the XOR opcode:

```
Opcode 0: BlackBoxFunc::RANGE(Witness[0], 8)   <- compiler-inserted range check on input a
Opcode 1: BlackBoxFunc::RANGE(Witness[1], 8)   <- compiler-inserted range check on input b
Opcode 2: BlackBoxFunc::XOR(Witness[0], Witness[1], num_bits=8, output=Witness[3])
```

Barretenberg processes these as separate constraints. The RANGE opcodes call `create_range_constraint(8)` on each input. Then inside `create_logic_constraint` ([`logic.cpp:101-102`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/stdlib/primitives/logic/logic.cpp#L101-L102)), when `chunk_size != 32`, the logic gate adds its own range constraints on the same inputs:

```cpp
if (chunk_size != 32) {
    a_chunk.create_range_constraint(chunk_size, "stdlib logic: bad range on final chunk of left operand");
    b_chunk.create_range_constraint(chunk_size, "stdlib logic: bad range on final chunk of right operand");
}
```

For `num_bits = 8`, the same `create_range_constraint(8)` is called twice on each input — once by the ACIR RANGE opcode and once inside the logic gate. These are redundant: the first range check already proves the input is in `[0, 255]`.

**Proof of Concept:** Verified with a u8 XOR Noir circuit ([`audit/my-report/poc/xor-circuit`](https://github.com/AztecProtocol/aztec-packages/tree/audit/qpzm/audit/my-report/poc/xor-circuit)):

```noir
fn main(a: u8, b: u8) -> pub u8 {
    a ^ b
}
```

Compiled ACIR opcodes (`python3 decode_acir.py target/xor_test.json`):

```
Function: main, Witnesses: 3, Opcodes: 4
  Opcode 0: {'BlackBoxFuncCall': {'RANGE': [{'Witness': 0}, 8]}}
  Opcode 1: {'BlackBoxFuncCall': {'RANGE': [{'Witness': 1}, 8]}}
  Opcode 2: {'BlackBoxFuncCall': {'XOR': [{'Witness': 0}, {'Witness': 1}, 8, 3]}}
  Opcode 3: {'AssertZero': [[], [[b'\x00...01', 2], [b'\x30...00', 3]], b'\x00...00']}
```

Barretenberg constraint trace showing the redundancy:

```
Opcode 0: RANGE(Witness[0], 8)
  → create_range_constraint(8)            ← first range check on a

Opcode 1: RANGE(Witness[1], 8)
  → create_range_constraint(8)            ← first range check on b

Opcode 2: XOR(Witness[0], Witness[1], 8, output=Witness[3])
  → create_logic_constraint(a, b, 8, true)
    → plookup UINT32_XOR (6 sub-lookups)
    → create_range_constraint(8) for a_chunk  ← redundant
    → create_range_constraint(8) for b_chunk  ← redundant
    → a.assert_equal(a_accumulator)
    → b.assert_equal(b_accumulator)
  → computed_result.assert_equal(acir_result)
```

End-to-end proof verified successfully with `a = 222 (0xDE), b = 173 (0xAD)`, output `115 (0x73)`.

**Impact:** Informational. No soundness risk. The extra range constraints cost gates unnecessarily. For `num_bits = 8`, each redundant `create_range_constraint(8)` adds gates to the circuit.

Note: if the [Oversized Plookup Table for Sub-32-bit Chunks](https://github.com/AztecProtocol/aztec-packages/issues/6) optimization is implemented (using `UINT8_XOR` for 8-bit chunks), the logic gate's internal range constraint would be eliminated entirely (implicit in the table), making this issue moot for `chunk_size <= 8`.

**Recommended Mitigation:** No immediate action required. This is an informational observation about redundant constraints in the current pipeline.

**Aztec:**
Acknowledged, there could be cases of redundant range constraints (on the noir side as well as barretenberg) but we prefer to have redundancy over missing a range constraint. This was a good find but we decided to not use the optimisation.


\clearpage
