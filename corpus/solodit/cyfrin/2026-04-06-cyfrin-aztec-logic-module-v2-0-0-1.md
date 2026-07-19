---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-06-cyfrin-aztec-logic-module-v2-0-0-1
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
title: Non-constant logic operations discard `OriginTag` provenance and bypass debug
  tag checks
vuln_class: []
---

# Non-constant logic operations discard `OriginTag` provenance and bypass debug tag checks

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-06-cyfrin-aztec-logic-module-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-06-cyfrin-aztec-logic-module-v2.0.md)_

---

**Description:** The non-constant path in `stdlib/primitives/logic/logic.cpp` rebuilds both operands from fresh chunk witnesses:

```cpp
field_pt a_chunk = witness_pt(ctx, left_chunk);
field_pt b_chunk = witness_pt(ctx, right_chunk);
```

Those derived witnesses default to free-witness provenance via the field/witness construction path reflected in `stdlib/primitives/field/field.cpp`.
```cpp
template <typename Builder>
field_t<Builder> field_t<Builder>::from_witness_index(Builder* ctx, const uint32_t witness_index)
{
    field_t<Builder> result(ctx);
    result.witness_index = witness_index;
    // Since this is now a witness (not a constant), set the free witness tag
    // The caller should set the appropriate tag if this element has a known provenance
    result.set_free_witness_tag();
    return result;
}
```

The logic result is then derived entirely from those fresh witnesses, and the final `assert_equal` calls only bind values; they do not restore the original provenance and temporarily suppress origin-tag checking for witness-to-witness equality in `stdlib/primitives/field/field.cpp:940-980`. As a result, the `OriginTag` guard in `transcript/origin_tag.cpp` is never evaluated for the original non-constant inputs.
```cpp
// A free witness element should not interact with an element that has an origin
if (tag_a.is_free_witness()) {
    if (!tag_b.is_free_witness() && !tag_b.is_empty()) {
        throw_or_abort("A free witness element should not interact with an element that has an origin");
    } else {
        // If both are free witnesses or one of them is empty, just use tag_a
        *this = tag_a;
        return;
    }
}
if (tag_b.is_free_witness()) {
    if (!tag_a.is_free_witness() && !tag_a.is_empty()) {
        throw_or_abort("A free witness element should not interact with an element that has an origin");
    } else {
        // If both are free witnesses or one of them is empty, just use tag_b
        *this = tag_b;
        return;
    }
}
```

**Impact:** In debug builds, the logic gadget can combine transcript-derived values with free witnesses, or values from different transcript sources, without triggering the `OriginTag` security checks that ordinary field arithmetic would enforce. This does not change proof soundness in release builds, where origin-tag checks are compiled out, but it weakens the active debug-time defense intended to catch unsafe Fiat-Shamir interactions.

**Recommended Mitigation:** Preserve provenance in the witness path exactly as other stdlib gadgets do. At minimum, compute `OriginTag(a.get_origin_tag(), b.get_origin_tag())` once in `create_logic_constraint` before chunking and assign the merged tag to the returned value. Preferably also tag derived chunk/result witnesses consistently so intermediate gadget outputs do not revert to free-witness provenance. When converting constants to fixed witnesses in the mixed path, explicitly preserve the original constant tag instead of accepting the default free-witness tag.

**Aztec:**
Fixed in [0f3ca1c](https://github.com/AztecProtocol/aztec-packages/commit/0f3ca1c6a84ef6ed14d4b29564ffcf4d37645619).

**Cyfrin:** Verified.
