---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-02-cyfrin-stakelink-vesting-v2-0-1-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-08-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-02-cyfrin-stakelink-vesting-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-02-cyfrin-stakelink-vesting-v2-0
title: Lack of `_lockTime` validation in `constructor`
vuln_class: []
---

# Lack of `_lockTime` validation in `constructor`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-02-cyfrin-stakelink-vesting-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-02-cyfrin-stakelink-vesting-v2.0.md)_

---

**Description:** The constructor assigns `lockTime = _lockTime` without checking `_lockTime <= MAX_LOCK_TIME`. If an out‑of‑range value is provided, any subsequent call that indexes `reSDLTokenIds[lockTime]` (e.g. in `stakeReleasableTokens` or `withdrawRESDLPositions`) will revert with an array‑bounds error.

Consider adding an explicit check in the constructor to improve UX and fail fast:

```solidity
require(_lockTime <= MAX_LOCK_TIME, "Invalid lock time");
```


**Stake.Link:** Fixed in commit [`e458512`](https://github.com/stakedotlink/contracts/commit/e4585124c05137848196d4ca759c3e9d28b963e1)

**Cyfrin:** Verified. `_lockTime` now required to not be larger than `MAX_LOCK_TIME`.
