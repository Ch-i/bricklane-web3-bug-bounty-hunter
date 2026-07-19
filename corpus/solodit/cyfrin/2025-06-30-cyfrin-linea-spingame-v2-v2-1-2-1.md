---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-30-cyfrin-linea-spingame-v2-v2-1-2-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-06-30T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-30-cyfrin-linea-spingame-v2-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-30-cyfrin-linea-spingame-v2-v2-1
title: Cache `prize.probability` before first use
vuln_class: []
---

# Cache `prize.probability` before first use

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-30-cyfrin-linea-spingame-v2-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-30-cyfrin-linea-spingame-v2-v2.1.md)_

---

**Description:** In `SpinGame::_fulfillRandomness()`, `prize.probability` is first read in an `if` statement, and then cached immediately afterward:

```solidity
if (prize.probability == 0) {
    continue;
}
uint64 prizeProbability = prize.probability;
```

This results in an unnecessary initial storage read before caching. Consider caching it above the `if`-statement.

**Linea:** Fixed in commit [`0290123`](https://github.com/Consensys/linea-hub/pull/557/commits/02901233dbe9a184b80bffb67bf5d489bc015a10)

**Cyfrin:** Verified. The caching of `prize.probability` is moved above the `if` and the cached value is used in the comparison.
