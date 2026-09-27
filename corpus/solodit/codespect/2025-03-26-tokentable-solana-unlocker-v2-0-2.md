---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-03-26-tokentable-solana-unlocker-v2-0-2
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-03-26T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-03-26-TokenTable-Solana-Unlocker-V2.md
tags:
- firm:codespect
- report:2025-03-26-tokentable-solana-unlocker-v2
title: '[M-03] Incorrect Preset input parameters validation'
vuln_class: []
---

# [M-03] Incorrect Preset input parameters validation

_Section severity (from Solodit section header): Medium_  
_Audit firm: CODESPECT_  
_Source report: [2025-03-26-TokenTable-Solana-Unlocker-V2.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-03-26-TokenTable-Solana-Unlocker-V2.md)_

---

**Files:** [`create_preset.rs`](https://github.com/EthSign/tokentable-unlocker-solana/blob/8dc0aa15e5cf78611a7bf7a5aa5ab1ca793ac108/programs/unlocker-v2-solana/src/instructions/create_preset.rs)

**Description:**

The `create_preset` instruction is called to create a `PresetAccount` account which holds the airdrop schedule information. The instruction caller provides a `Preset` struct which is used to populate values for the `PresetAccount`. The input `Preset` struct is validated using `_preset_has_valid_format()` function. The function ensures the following:

- `preset.linear_bips` vector sum of values is equal to `BIPS_PRECISION` const;
- All vectors must be of the same length;
- The `preset.linear_start_timestamps_relative` vector last element must be smaller than `preset.linear_end_timestamp_relative`;
- Each `preset.num_of_unlocks_for_each_linear` element value must be smaller than relative timestamp spacing;

The first three conditions from the above list are enclosed within the following conditional instruction:

```rust
if
  !(total == BIPS_PRECISION) &&
  preset.linear_bips.len() == preset.linear_start_timestamps_relative.len() &&
  preset.linear_start_timestamps_relative[preset.linear_start_timestamps_relative.len() - 1] <
    preset.linear_end_timestamp_relative &&
  preset.num_of_unlocks_for_each_linear.len() == preset.linear_start_timestamps_relative.len()
{
  return false;
}
```

We can see that the logical operator `!` is not applied correctly, and hence it is possible that all the remaining checks after BIPS verification can be bypassed.

**Impact:** A preset account could be created with incorrect values. Depending on which specific values are incorrect (several are possible), it may become impossible to claim from the affected Preset.

**Recommendation:** Fix the logical expression.

**Status:** Fixed

**Update from TokenTable:** Fixed the parenthesis location in [c5a96b7c73e0b37678436b4bce9adf9e3c8bf78f](https://github.com/EthSign/tokentable-unlocker-solana/tree/c5a96b7c73e0b37678436b4bce9adf9e3c8bf78f).
