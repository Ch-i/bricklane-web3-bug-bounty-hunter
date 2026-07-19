---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-04-cyfrin-symbiotic-v2-0-3-1
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
title: Cache storage reads in `upperLookupRecentCheckpoint`
vuln_class: []
---

# Cache storage reads in `upperLookupRecentCheckpoint`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-04-cyfrin-symbiotic-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-04-cyfrin-symbiotic-v2.0.md)_

---

**Description:** Functions like `upperLookupRecentCheckpoint` in `Checkpoints` perform multiple expensive storage reads for `self._trace._checkpoints.length` and repeated `_unsafeAccess` calls.

**Recommended Mitigation:** Cache the checkpoints array reference and length:

```solidity
function upperLookupRecentCheckpoint(
    Trace208 storage self,
    uint48 key
) internal view returns (bool, uint48, uint208, uint32) {
    OZCheckpoints.Checkpoint208[] storage checkpoints = self._trace._checkpoints; // Cache
    uint256 len = checkpoints.length; // Cache length

    uint256 low = 0;
    uint256 high = len;

    if (len > 5) {
        uint256 mid = len - Math.sqrt(len);
        if (key < _unsafeAccess(checkpoints, mid)._key) { // Use cached reference
            high = mid;
        } else {
            low = mid + 1;
        }
    }

    uint256 pos = _upperBinaryLookup(checkpoints, key, low, high);
    // ... rest of function
}
```

**Symbiotic:** Acknowledged.

**Cyfrin:** Acknowledged.
