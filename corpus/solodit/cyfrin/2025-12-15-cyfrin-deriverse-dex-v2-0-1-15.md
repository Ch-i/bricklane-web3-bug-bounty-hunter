---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-15
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Operator precedence Issue during points program expiration validation in `change_points_program_expiration`
vuln_class: []
---

# Operator precedence Issue during points program expiration validation in `change_points_program_expiration`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** In `change_points_program_expiration`, the validation for `new_expiration_time` uses `!data.new_expiration_time < root_state.points_program_expiration` instead of `!(data.new_expiration_time < root_state.points_program_expiration)`, causes unintended behavior.

```rust
if !data.new_expiration_time < root_state.points_program_expiration {
    bail!(InvalidNewExpirationTime {
        program_name: "Points Program".to_string(),
        new_time: data.new_expiration_time,
        old_time: root_state.points_program_expiration
    });
}
```
This occurs because the bitwise NOT operator has higher precedence than the less-than comparison operator(`<`). This causes the expression to be evaluated as:
```rust
(!data.new_expiration_time) < root_state.points_program_expiration
```
Instead of the intended:
```rust
!(data.new_expiration_time < root_state.points_program_expiration)
```

**Impact:** Using the `change_points_program_expiration` function, we cannot decrease the points program expiration because applying `!` to a `u32` performs a bitwise NOT operation. This produces a value close to `u32::MAX`, which is almost always greater than any reasonable expiration time when attempting to reduce `points_program_expiration`.

**Recommended Mitigation:** Use `!(data.new_expiration_time < root_state.points_program_expiration)` during validation, here's the fix:
```rust
    if !(data.new_expiration_time < root_state.points_program_expiration){
        bail!(InvalidNewExpirationTime {
            program_name: "Points Program".to_string(),
            new_time: data.new_expiration_time,
            old_time: root_state.points_program_expiration
        });
    }
```

**Deriverse:** Fixed in commit [eae149](https://github.com/deriverse/protocol-v1/commit/eae1494725cf3ebdc5800fa39bb80b6c90c62478).

**Cyfrin:** Verified.
