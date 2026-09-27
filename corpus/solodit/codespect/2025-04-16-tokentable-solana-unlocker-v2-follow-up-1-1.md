---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-16-tokentable-solana-unlocker-v2-follow-up-1-1
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-04-16T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-16-TokenTable-Solana-Unlocker-V2-Follow-Up.md
tags:
- firm:codespect
- report:2025-04-16-tokentable-solana-unlocker-v2-follow-up
title: '[L-02] The _preset_is_empty function should not consider num_of_unlocks_for_each_linear'
vuln_class: []
---

# [L-02] The _preset_is_empty function should not consider num_of_unlocks_for_each_linear

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-16-TokenTable-Solana-Unlocker-V2-Follow-Up.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-16-TokenTable-Solana-Unlocker-V2-Follow-Up.md)_

---

**Files:** [create_actual.rs](https://github.com/EthSign/tokentable-unlocker-solana/tree/67a39faff7b848ae05c5e3ab45e36b60efcc622e/programs/unlocker-v2-solana/src/instructions/create_actual.rs#L62C14-L62C44)

**Description:**

When `preset.stream` is true, the length of `preset.num_of_unlocks_for_each_linear` is not strictly limited to save rent. Therefore, in a successfully created `preset` account, `preset.num_of_unlocks_for_each_linear` may be 0. As a result, when `_preset_is_empty` checks whether the `preset` account is initialized, it should not consider the `num_of_unlocks_for_each_linear` field.

```rust
#[allow(unused_parens)] // Allowing unused_parens to ignore Prettier formatting
fn _preset_is_empty(preset: anchor_lang::prelude::Account<'_, PresetAccount>) -> bool {
    return (
        preset.linear_bips.len() *
            preset.linear_start_timestamps_relative.len() *
            preset.num_of_unlocks_for_each_linear.len() *
            (preset.linear_end_timestamp_relative as usize) == 0
    );
}
```

**Impact:** An already initialized `preset` account may be mistakenly considered uninitialized, preventing the creation of its corresponding `actual` account.

**Recommendation:** In the `_preset_is_empty` function, the `num_of_unlocks_for_each_linear` field should not be considered when `preset.stream` is true.

**Status:** Fixed

**Update from TokenTable:** We now take `preset.stream` into account when determining if a preset is empty in [b98faf703c27399307598bcb21bf6f647fc143bf](https://github.com/EthSign/tokentable-unlocker-solana/pull/8/commits/b98faf703c27399307598bcb21bf6f647fc143bf).
