---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-3-15
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Inefficient `free_index` Selection in Assets Array Causes Performance Degradation
vuln_class: []
---

# Inefficient `free_index` Selection in Assets Array Causes Performance Degradation

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The `find_or_alloc_asset` function in `client_primary` always selects the last vacant slot (`asset_id == 0`) instead of the first available slot when allocating new assets. This causes unnecessary `O(n)` iterations, space fragmentation, and potential compute budget exhaustion as the assets array grows.

In `client_primary`, the loop logic is:

```rust
for (i, a) in self.assets.iter().enumerate() {
    let current_id = a.asset_id;
    if current_id == asset_id {
        asset_index = i;
        break;
    } else if current_id == 0 {
        free_index = i;  // Always overwrites with the last vacant slot
    }
}
```

`free_index` is continuously overwritten whenever a vacant slot (`asset_id == 0`) is found, meaning it will always contain the index of the last vacant slot in the array, not the first.

Example scenario:
- Array state: `[asset1, 0, asset2, 0, asset3]`
- When searching for a non-existent `asset4`
- The loop traverses all 5 elements
- `free_index` is set to index `1` (first 0), then overwritten to index `3` (last 0)
- The first vacant slot at index `1` remains unused

**Impact:** Later in the search, every lookup could requires full O(n) traversal even when vacant slots exist early in the array

**Recommended Mitigation:** `free_index` could only be overwritten when it is `NULL_INDEX`, thus we are always returning and using the first vacant slot.

**Deriverse:** Fixed in commit [30e062e](https://github.com/deriverse/protocol-v1/commit/30e062e9f393bfdcf9a510cd2da71237d5db9d20).

**Cyfrin:** Verified.
