---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-14-cyfrin-goldilocks-v1-1-2-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-04-14T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md
tags:
- firm:cyfrin
- report:2024-04-14-cyfrin-goldilocks-v1-1
title: '`Goldilocked._lockedLocks()` should round up.'
vuln_class: []
---

# `Goldilocked._lockedLocks()` should round up.

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-14-cyfrin-goldilocks-v1.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md)_

---

**Description:** Users might borrow 1 more wei as it rounds down.
```solidity
  function _lockedLocks(address user) internal view returns (uint256) {
    return FixedPointMathLib.divWad(borrowedHoney[user], IGoldiswap(goldiswap).floorPrice());//@audit round up
  }
```
**Client:** Fixed in [PR #15](https://github.com/0xgeeb/goldilocks-core/pull/15)

**Cyfrin:** Verified.
