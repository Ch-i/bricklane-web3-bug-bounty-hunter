---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-04-cyfrin-symbiotic-v2-0-3-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-09-04T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-04-cyfrin-symbiotic-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-04-cyfrin-symbiotic-v2-0
title: Loop can use unchecked arithmetic and cache array length
vuln_class: []
---

# Loop can use unchecked arithmetic and cache array length

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-04-cyfrin-symbiotic-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-04-cyfrin-symbiotic-v2.0.md)_

---

**Description:** The `Network::scheduleBatch()` function has multiple loops that can be optimized with unchecked arithmetic and cached array lengths.

**Recommended Mitigation:**
```solidity
function scheduleBatch(/*...*/) public virtual override onlyRole(PROPOSER_ROLE) {
    uint256 targetsLength = targets.length;
    if (targetsLength != values.length || targetsLength != payloads.length) {
        revert TimelockInvalidOperationLength(targetsLength, payloads.length, values.length);
    }

    unchecked {
        for (uint256 i; i < targetsLength; ++i) {
            uint256 minDelay = getMinDelay(targets[i], payloads[i]);
            if (delay < minDelay) {
                revert TimelockInsufficientDelay(delay, minDelay);
            }
        }
    }

    bytes32 id = hashOperationBatch(targets, values, payloads, predecessor, salt);
    _scheduleOverriden(id, delay);

    unchecked {
        for (uint256 i; i < targetsLength; ++i) {
            emit CallScheduled(id, i, targets[i], values[i], payloads[i], predecessor, delay);
        }
    }
    // ...
}
```

**Symbiotic:** Acknowledged.

**Cyfrin:** Acknowledged.

\clearpage
