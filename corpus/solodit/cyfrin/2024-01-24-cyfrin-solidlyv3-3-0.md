---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-01-24-cyfrin-solidlyv3-3-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-01-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md
tags:
- firm:cyfrin
- report:2024-01-24-cyfrin-solidlyv3
title: Cache array length outside of loop
vuln_class: []
---

# Cache array length outside of loop

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-01-24-cyfrin-solidlyV3.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md)_

---

**Description:** Cache array length outside of loop:

```solidity
File: contracts/RewardsDistributor.sol
// @audit use `numLeaves` from L263 instead of `earners.length`
265:         for (uint256 i; i < earners.length; ) {
```

**Solidly:**
Fixed in commit [6481747](https://github.com/SolidlyV3/v3-rewards/commit/6481747737b98c8650a36f87b1aeace815505ba9).

**Cyfrin:**
Verified.
