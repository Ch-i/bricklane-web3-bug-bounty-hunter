---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-02-cyfrin-stakelink-vesting-v2-0-1-0
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
title: Zero‑Duration vesting edge case
vuln_class: []
---

# Zero‑Duration vesting edge case

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-02-cyfrin-stakelink-vesting-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-02-cyfrin-stakelink-vesting-v2.0.md)_

---

**Description:** When `duration == 0`, calling `vestedAmount(start)` falls through the `else if (_timestamp > start + duration)` check (because `start > start` is false) into the linear‑vest branch, executing

```solidity
(totalAllocation * (start - start)) / duration
```

This creates a brief one‑second revert window at exactly `start`. Since any later timestamp (`> start`) correctly returns full allocation.

Consider changing the comparison to `>=`:
```diff
- else if (_timestamp > start + duration) {
+ else if (_timestamp >= start + duration) {
    return totalAllocation;
}
```

so that `start + duration` (even when zero) immediately yields the “fully vested” branch.

**Stake.Link:** Fixed in commit [`e458512`](https://github.com/stakedotlink/contracts/commit/e4585124c05137848196d4ca759c3e9d28b963e1)

**Cyfrin:** Verified. Comparison is not `>=`.
