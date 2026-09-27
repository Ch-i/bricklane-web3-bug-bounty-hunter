---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-03-26-tokentable-solana-unlocker-v2-2-0
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
title: '[I-01] Miscalculated PresetAccount size'
vuln_class: []
---

# [I-01] Miscalculated PresetAccount size

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-03-26-TokenTable-Solana-Unlocker-V2.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-03-26-TokenTable-Solana-Unlocker-V2.md)_

---

**Files:** [`preset.rs`](https://github.com/EthSign/tokentable-unlocker-solana/blob/7516b8c86cb305f9d9eb3ac77e7fcd7c6b60cc2f/programs/unlocker-v2-solana/src/models/preset.rs#L22)

**Description:**

When creating a `PresetAccount`, the size of the `PresetAccount` is initialized based on the `Preset` struct passed in, using the `calculate_size()` function.

```rust
#[account(
  //...
  space = 8 + _preset.clone().calculate_size()
)]
pub preset: Account<'info, PresetAccount>,
```

The calculation seems to be implemented incorrectly, as the total size of non-vector items should be `linear_end_timestamp_relative + next_actual_id + stream + preset_id = 25` instead of 32.

```rust
pub fn calculate_size(self) -> usize {
  let mut size = 0;
  // @audit incorrect size
  size += 32; // Takes care of all non-vector items
  size += 4 + 8 * self.linear_start_timestamps_relative.len();
  size += 4 + 8 * self.linear_bips.len();
  size += 4 + 8 * self.num_of_unlocks_for_each_linear.len();
  size += 4 + self.project_id.len();

  size
}
```

**Impact:** This would result in unnecessary rent wastage.

**Recommendation:** Calculate account space using the correct size.

**Status:** Fixed

**Update from TokenTable:** Updated base size to 25 in [85e56b4993b46006e5cb36e08df56f49ac4a535e](https://github.com/EthSign/tokentable-unlocker-solana/tree/85e56b4993b46006e5cb36e08df56f49ac4a535e).
