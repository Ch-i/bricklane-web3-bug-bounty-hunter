---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-03-26-tokentable-solana-unlocker-v2-2-2
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-03-26T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-03-26-TokenTable-Solana-Unlocker-V2.md
tags:
- firm:codespect
- report:2025-03-26-tokentable-solana-unlocker-v2
title: '[I-03] In some cases the num_of_unlocks_for_each_linear vector may waste rent'
vuln_class: []
---

# [I-03] In some cases the num_of_unlocks_for_each_linear vector may waste rent

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-03-26-TokenTable-Solana-Unlocker-V2.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-03-26-TokenTable-Solana-Unlocker-V2.md)_

---

**Original severity:** Best Practices

**Files:** [`create_preset.rs`](https://github.com/EthSign/tokentable-unlocker-solana/blob/7516b8c86cb305f9d9eb3ac77e7fcd7c6b60cc2f/programs/unlocker-v2-solana/src/instructions/create_preset.rs#L64)

**Description:**

When the `PresetAccount` enables the stream configuration, the `num_of_unlocks_for_each_linear` field becomes ineffective and can be set to an empty vector.

```rust
if preset.stream {
  num_of_unlocks_for_incomplete_linear = latest_incomplete_linear_duration;
} else {
  num_of_unlocks_for_incomplete_linear =
    preset.num_of_unlocks_for_each_linear[latest_incomplete_linear_index as usize];
}
```

However, during the `create_preset()` function, the `num_of_unlocks_for_each_linear` field must always be set to the same length as the `linear_start_timestamps_relative` vector, regardless of the situation.

```rust
if
  !(total == BIPS_PRECISION) &&
  preset.linear_bips.len() == preset.linear_start_timestamps_relative.len() &&
  preset.linear_start_timestamps_relative[preset.linear_start_timestamps_relative.len() - 1] <
    preset.linear_end_timestamp_relative &&
  preset.num_of_unlocks_for_each_linear.len() == preset.linear_start_timestamps_relative.len()
{
```

**Impact:** This will cause some rent waste for certain fields in the `PresetAccount` when the stream is enabled.

**Recommendation:** It is recommended that when the stream is enabled, the `num_of_unlocks_for_each_linear` field can be left empty. Additionally, the `_preset_is_empty()` function should be modified to remove the `num_of_unlocks_for_each_linear` field from it, based on the stream value.

**Status:** Fixed

**Update from TokenTable:** If `preset.stream` is set to true, we no longer enforce that `preset.num_of_unlocks_for_each_linear` has the same length as `preset.linear_start_timestamps_relative` in [cd8e53d03b91c20af3153fb8feb6cbf1988d7bea](https://github.com/EthSign/tokentable-unlocker-solana/tree/cd8e53d03b91c20af3153fb8feb6cbf1988d7bea).
