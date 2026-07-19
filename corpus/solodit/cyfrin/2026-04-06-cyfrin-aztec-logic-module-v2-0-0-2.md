---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-06-cyfrin-aztec-logic-module-v2-0-0-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-04-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-06-cyfrin-aztec-logic-module-v2.0.md
tags:
- firm:cyfrin
- report:2026-04-06-cyfrin-aztec-logic-module-v2-0
title: Missing Builder Context Validation in `create_logic_constraint`
vuln_class: []
---

# Missing Builder Context Validation in `create_logic_constraint`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-06-cyfrin-aztec-logic-module-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-06-cyfrin-aztec-logic-module-v2.0.md)_

---

**Description:** In [`stdlib/primitives/logic/logic.cpp:80`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/stdlib/primitives/logic/logic.cpp#L80), when both `a` and `b` are witnesses, the function extracts the builder context from only one operand without validating that both operands belong to the same builder:

```cpp
// Both a and b are witnesses at this point, so they have the same context.
Builder* ctx = a.get_context();
```

There is no check that `a.get_context() == b.get_context()`. If a developer passes operands from different builders, the function would:

1. Create `b_chunk` witnesses in `a`'s builder (`witness_pt(ctx, right_chunk)`)
2. Accumulate `b_accumulator` in `a`'s builder
3. Call `b.assert_equal(b_accumulator)` — comparing a witness in `b`'s builder with one in `a`'s builder — undefined behavior

Related Occurrence (Same Root Cause):

The same "pick one context and assume the other matches" pattern exists in the plookup read layer.

In [`stdlib/primitives/plookup/plookup.cpp:19`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/stdlib/primitives/plookup/plookup.cpp#L19), `plookup_read<Builder>::get_lookup_accumulators(...)` selects a `ctx` from either `key_a` or `key_b`:

```cpp
Builder* ctx = key_a.get_context() ? key_a.get_context() : key_b.get_context();
```

and then uses witness indices from both operands (for the variable path) without validating that both keys belong to the same builder. If `key_a` and `key_b` come from different builders, this can similarly lead to undefined behavior (e.g., passing a witness index allocated in one builder into `create_gates_from_plookup_accumulators` on another builder).

**Impact:** Low. This is a developer error (mixing builders), not a prover attack. The prover does not control which builder objects are used — this is determined at circuit construction time. If triggered, it would cause undefined behavior or assertion failures during circuit construction, not during verification.

**Proof of Concept:**
```cpp
// Missing builder context validation.
// When operands come from different builders, create_logic_constraint uses only a's context.
// b's chunks get created in the wrong builder, and b.assert_equal() compares across builders.
// This test documents the undefined behavior — it should ideally be caught by an assertion.
TYPED_TEST(LogicTest, CrossBuilderContextMismatch)
{
    STDLIB_TYPE_ALIASES

    auto builder_1 = Builder();
    auto builder_2 = Builder();

    field_ct a = witness_ct(&builder_1, uint256_t(42));
    field_ct b = witness_ct(&builder_2, uint256_t(17));

    // a.get_context() != b.get_context(), but no validation exists.
    // The function will use builder_1's context for everything,
    // then call b.assert_equal() which compares a witness in builder_2
    // with an accumulator in builder_1.
    EXPECT_NE(a.get_context(), b.get_context());

    // This call exhibits undefined behavior due to cross-builder operands.
    // Depending on implementation, it may:
    // - Silently produce a broken circuit
    // - Crash with an out-of-range witness index
    // - Trigger an assertion in debug builds
    // Any of these outcomes confirms the missing validation.
    EXPECT_ANY_THROW(stdlib::logic<Builder>::create_logic_constraint(a, b, 32, true));
}
```

Test result: The error is caught downstream by `assert_equal()` with: `"Pointers refer to different builder objects!"`.
An early validation in `create_logic_constraint` would provide a clearer error at the point of misuse.

**Recommended Mitigation:** Add context validation before the main loop. Since constant cases are already handled above ([lines 62-77](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/stdlib/primitives/logic/logic.cpp#L62-L77)), at this point both `a` and `b` are witnesses with non-null contexts:

Option 1 — explicit assertion:
```cpp
ASSERT(a.get_context() == b.get_context() && "logic constraint: operands belong to different builders");
Builder* ctx = a.get_context();
```

Option 2 — use existing `validate_context` utility from [`field.hpp`](https://github.com/AztecProtocol/aztec-packages/blob/main/barretenberg/cpp/src/barretenberg/stdlib/primitives/field/field.hpp):
```cpp
Builder* ctx = validate_context(a.get_context(), b.get_context());
```

Consider applying the same pattern in `plookup_read<Builder>::get_lookup_accumulators(...)` before using witness indices from both keys.

**Aztec:**
Fixed in [249bfdc](https://github.com/AztecProtocol/aztec-packages/commit/249bfdc76053f41455e048f182605a871f970cce).

**Cyfrin:** Verified.
