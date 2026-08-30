---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-02-cyfrin-stakelink-vesting-v2-0-2-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-08-02T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-02-cyfrin-stakelink-vesting-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-02-cyfrin-stakelink-vesting-v2-0
title: use fixed length array for `reSDLTokenIds`
vuln_class: []
---

# use fixed length array for `reSDLTokenIds`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-02-cyfrin-stakelink-vesting-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-02-cyfrin-stakelink-vesting-v2.0.md)_

---

**Description:** The contract currently declares

```solidity
uint256[] private reSDLTokenIds;
```

and in the constructor uses a `for`-loop with `.push(0)` to initialize it to length `MAX_LOCK_TIME + 1`. This incurs:

* A dynamic‐array length slot in storage
* A pointer slot for the array data
* Multiple storage writes (one per `.push`)

Since the array’s length is always exactly `MAX_LOCK_TIME + 1` (5), a static array:

```solidity
uint256[MAX_LOCK_TIME + 1] private reSDLTokenIds;
```

removes the dynamic‐array overhead and eliminates the initialization loop.

Consider replacing the dynamic array with a fixed-length array and remove the constructor loop:

```diff
-   // list of reSDL token ids for each lock time
-   uint256[] private reSDLTokenIds;

+   // list of reSDL token ids for each lock time (0–4 years)
+   uint256[MAX_LOCK_TIME + 1] private reSDLTokenIds;

    constructor(…) {
        ...
-       for (uint256 i = 0; i <= MAX_LOCK_TIME; ++i) {
-           reSDLTokenIds.push(0);
-       }
     }
```

This change collapses two storage slots (length + data pointer) into one and removes the costly initialization loop, reducing both deployment and per-read gas costs.

**Stake.Link:** Fixed in commit [`128c335`](https://github.com/stakedotlink/contracts/commit/128c33560d8f43057c5d10d822b4904d0762d0fd)

**Cyfrin:** Verified. `reSDLTokenIds` now static.

\clearpage
