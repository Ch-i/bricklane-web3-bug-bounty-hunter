---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-03-cyfrin-linea-burn-v2-2-1-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-11-03T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-03-cyfrin-linea-burn-v2.2.md
tags:
- firm:cyfrin
- report:2025-11-03-cyfrin-linea-burn-v2-2
title: Inconsistent deadline check in `V3DexSwap.swap `
vuln_class: []
---

# Inconsistent deadline check in `V3DexSwap.swap `

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-03-cyfrin-linea-burn-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-03-cyfrin-linea-burn-v2.2.md)_

---

**Description:** The swap() function in V3DexSwap implements the require check in the snippet below which ensures block.timestamp is strictly less than the `_deadline`.

```solidity
require(_deadline > block.timestamp, DeadlineInThePast());
```

However, the [Ramses V3 Swap Router](https://lineascan.build/address/0x8BE024b5c546B5d45CbB23163e1a4dca8fA5052A#code) allows swaps to occur even when the block.timestamp is equal to the deadline.

```solidity
modifier checkDeadline(uint256 deadline) {
        if (_blockTimestamp() > deadline) revert Old();
        _;
    }
```

**Impact:** Due to this inconsistency, if `_deadline` is passed as block.timestamp to the `V3DexSwap.swap ` function, the call would revert even though it's a valid value accepted by the router.

**Proof of Concept:** **Recommended Mitigation:**

**Linea:** Fixed at commit [e531e7](https://github.com/Consensys/linea-monorepo/pull/1620/commits/be1cbce5ad0410d004e09d0f559522e4eee22daa)

**Cyfrin:** Verified.
