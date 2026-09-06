---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-06-cyfrin-aztec-logic-module-v2-0-1-1
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
title: Oversized Plookup Table for Sub-32-bit Chunks
vuln_class: []
---

# Oversized Plookup Table for Sub-32-bit Chunks

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-06-cyfrin-aztec-logic-module-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-06-cyfrin-aztec-logic-module-v2.0.md)_

---

**Description:** In [`stdlib/primitives/logic/logic.cpp:111`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/stdlib/primitives/logic/logic.cpp#L111), the multi-table ID is always `UINT32_XOR` or `UINT32_AND` regardless of the actual `chunk_size`:

```cpp
const auto multi_table_id = is_xor_gate ? plookup::MultiTableId::UINT32_XOR : plookup::MultiTableId::UINT32_AND;
```

The `UINT32` multi-table decomposes each input into 6 sub-lookups (`[6, 6, 6, 6, 6, 2]` bits). When the last chunk has `chunk_size ≤ 8`, smaller tables already exist ([`types.hpp:105-112`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/stdlib_circuit_builders/plookup_tables/types.hpp#L105-L112)):

```cpp
UINT8_XOR,   // 2 sub-lookups: [6, 2]
UINT16_XOR,  // 3 sub-lookups: [6, 6, 4]
UINT32_XOR,  // 6 sub-lookups: [6, 6, 6, 6, 6, 2]
```

For example, when `num_bits = 1` (so `chunk_size = 1`), the code performs 6 sub-lookups where 5 look up `(0, 0, 0)` — valid but wasteful. Using `UINT8_XOR` would need only 2 sub-lookups for the same result.

Additionally, a `UINT8` table implicitly proves 8-bit range, so the explicit `create_range_constraint` at [line 127](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/stdlib/primitives/logic/logic.cpp#L127) could be skipped for `chunk_size ≤ 8`, saving further gates.

**Impact:** Informational. For 16-bit operations, using `UINT16` instead of `UINT32` would reduce total gates from 1376 to 10 per call by eliminating the explicit `create_range_constraint(16)`, improving proving cost.

Current production usage comparison:

| `num_bits` | Current table | Sub-lookups | Range constraint | Optimized table | Sub-lookups | Range constraint |
|-----------|--------------|-------------|-----------------|----------------|-------------|-----------------|
| 16 | UINT32 | 6 | `create_range_constraint(16)` | UINT16 | 3 | Not needed (implicit) |
| 32 | UINT32 | 6 | Not needed (implicit) | UINT32 | 6 | Not needed (implicit) |

The Noir rollup circuits currently use AND operations with `num_bits = 16` and `32`:

| Noir function | Circuit | `num_bits` | Op |
|--------------|---------|-----------|-----|
| `is_power_of_2` (`n & (n-1) == 0`) | Tx Merge Rollup, Block Root Rollup | 16 (u16) | AND |
| `is_power_of_2` (`n & (n-1) == 0`) | Tx Merge Rollup, Block Root Rollup | 32 (u32) | AND |
| `compute_subtree_sizes` (`num_leaves & subtree_size`) | Tx Base Rollup | 32 (u32) | AND |

For `num_bits = 32`, every chunk is exactly 32 bits — no wasted sub-lookups. For `num_bits = 16`, the savings are significant: using `UINT16_AND` instead of `UINT32_AND` eliminates the explicit `create_range_constraint(16)` (which the UINT16 table proves implicitly), saving 1372 gates per call.

Measured gate counts for a single 16-bit AND lookup:

| Approach | Gates | Total gates | Tables | Table rows |
|----------|-------|------------|--------|-----------|
| UINT32_AND + `create_range_constraint(16)` | 1375 | 1376 | 2 | 4112 (SLICE_6 + SLICE_2) |
| UINT16_AND (no range constraint needed) | 3 | 4 | 2 | 4352 (SLICE_6 + SLICE_4) |

The dominant cost in the current approach is `create_range_constraint(16)`, which decomposes into ~1369 arithmetic gates internally. The UINT16 table's 3 sub-lookups implicitly prove a 16-bit range, making that explicit constraint unnecessary.

Since production circuits use both `num_bits = 32` and `num_bits = 16`, the circuit would need both `UINT32_AND` and `UINT16_AND` tables. The combined table cost:

| Configuration | Total gates | Tables | Table rows |
|--------------|------------|--------|-----------|
| Current: UINT32_AND only | 1376 | 2 | 4112 (SLICE_6: 4096 + SLICE_2: 16) |
| Proposed: UINT32_AND + UINT16_AND | 10 | 3 | 4368 (SLICE_6: 4096 + SLICE_2: 16 + SLICE_4: 256) |

The additional cost is 256 table rows (one `SLICE_4` BasicTable), a one-time overhead to save 1372 gates per 16-bit logic call.

**Proof of Concept:**
```cpp
// Compare UINT32 vs UINT16 table for 16-bit lookups.
// UINT32 = 6 sub-lookups + explicit range constraint.
// UINT16 = 3 sub-lookups + implicit 16-bit range (no extra range constraint needed).
TYPED_TEST(LogicTest, CompareUint32VsUint16Table)
{
    STDLIB_TYPE_ALIASES
    using plookup_read = stdlib::plookup_read<Builder>;

    // Approach 1: Current code — UINT32_AND + range constraint
    {
        auto builder = Builder();
        field_ct a = witness_ct(&builder, uint256_t(0xABCD));
        field_ct b = witness_ct(&builder, uint256_t(0x1234));

        size_t gates_before = builder.num_gates();
        field_ct result = plookup_read::read_from_2_to_1_table(plookup::MultiTableId::UINT32_AND, a, b);
        a.create_range_constraint(16, "range");
        b.create_range_constraint(16, "range");
        size_t gates_after = builder.num_gates();

        EXPECT_EQ(uint256_t(result.get_value()), uint256_t(0xABCD & 0x1234));
        std::cout << "UINT32_AND + range_constraint(16): gates=" << (gates_after - gates_before)
                  << "  total_gates=" << builder.num_gates()
                  << "  tables=" << builder.get_num_lookup_tables()
                  << "  table_rows=" << builder.get_tables_size() << "\n";

        EXPECT_TRUE(CircuitChecker::check(builder));
    }

    // Approach 2: Both UINT32_AND + UINT16_AND in the same circuit (production scenario).
    {
        auto builder = Builder();
        field_ct a32 = witness_ct(&builder, uint256_t(0xDEADBEEF));
        field_ct b32 = witness_ct(&builder, uint256_t(0x12345678));
        field_ct a16 = witness_ct(&builder, uint256_t(0xABCD));
        field_ct b16 = witness_ct(&builder, uint256_t(0x1234));

        plookup_read::read_from_2_to_1_table(plookup::MultiTableId::UINT32_AND, a32, b32);
        plookup_read::read_from_2_to_1_table(plookup::MultiTableId::UINT16_AND, a16, b16);

        std::cout << "UINT32_AND + UINT16_AND combined:  "
                  << "total_gates=" << builder.num_gates()
                  << "  tables=" << builder.get_num_lookup_tables()
                  << "  table_rows=" << builder.get_tables_size() << "\n";

        EXPECT_TRUE(CircuitChecker::check(builder));
    }
}
```

Test output:
```
UINT32_AND + range_constraint(16): gates=1375  total_gates=1376  tables=2  table_rows=4112
UINT32_AND + UINT16_AND combined:  total_gates=10  tables=3  table_rows=4368
```

**Recommended Mitigation:** Consider selecting the smallest available multi-table that fits `chunk_size` (e.g., `UINT8` for `chunk_size ≤ 8`, `UINT16` for `chunk_size ≤ 16`).

Current production usage:

- `num_bits = 16` ([`math.nr:is_power_of_2`](https://github.com/AztecProtocol/aztec-packages/blob/main/noir-projects/noir-protocol-circuits/crates/types/src/utils/math.nr), u16): Switching to `UINT16_AND` would save 1372 gates per call by eliminating the explicit `create_range_constraint(16)`.
- `num_bits = 32` ([`math.nr:is_power_of_2_u32`](https://github.com/AztecProtocol/aztec-packages/blob/main/noir-projects/noir-protocol-circuits/crates/types/src/utils/math.nr), [`unbalanced_merkle_tree.nr:compute_subtree_sizes`](https://github.com/AztecProtocol/aztec-packages/blob/main/noir-projects/noir-protocol-circuits/crates/types/src/merkle_tree/unbalanced_merkle_tree.nr), u32): No change needed — `UINT32_AND` is already the optimal table.

**Aztec:**
Acknowledged, The code always uses `UINT32_XOR`/`UINT32_AND` plookup tables even when the last chunk is smaller than 32 bits. Smaller tables (UINT8, UINT16) exist and would use fewer sub-lookups. However, this is a minor optimization that would change the circuit structure, which we want to avoid at this point. The existing explicit range constraint on the last chunk ensures correctness regardless of table size.
