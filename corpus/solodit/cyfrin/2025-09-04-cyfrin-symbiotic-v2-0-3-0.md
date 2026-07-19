---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-04-cyfrin-symbiotic-v2-0-3-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-09-04T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-04-cyfrin-symbiotic-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-04-cyfrin-symbiotic-v2-0
title: '`PersistentSet` library storage access'
vuln_class: []
---

# `PersistentSet` library storage access

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-04-cyfrin-symbiotic-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-04-cyfrin-symbiotic-v2.0.md)_

---

**Description:** Multiple expensive storage reads (SLOAD ~2100 gas each) for the same `set._statuses[value]` occur in several functions: `_add`, `_remove`, `_containsAt`, and `_contains`. Each repeated access to the same storage slot wastes gas.

**Recommended Mitigation:** Cache storage pointers to avoid repeated SLOADs in all affected functions:

```solidity
function _add(Set storage set, uint48 key, bytes32 value) private returns (bool) {
    unchecked {
        Status storage status = set._statuses[value]; // Cache once
        if (status.isAdded) {
            if (status.isRemoved.latest() == 0) {
                return false;
            }
            status.isRemoved.push(key, 0);
        } else {
            set._elements.push(value);
            status.isAdded = true;
            status.addedAt = key;
        }
        set._length += 1;
        return true;
    }
}

function _containsAt(Set storage set, uint48 key, bytes32 value, bytes memory hint) private view returns (bool) {
    Status storage status = set._statuses[value]; // Cache once
    return status.isAdded && key >= status.addedAt
        && status.isRemoved.upperLookupRecent(key, hint) == 0;
}

function _contains(Set storage set, bytes32 value) private view returns (bool) {
    Status storage status = set._statuses[value]; // Cache once
    return status.isAdded && status.isRemoved.latest() == 0;
}
```

This saves ~2100-4200 gas per function call by eliminating redundant storage reads.

**Symbiotic:** Acknowledged. Unchanged to keep it compatible with OpenZeppelin code.

**Cyfrin:** Acknowledged.
