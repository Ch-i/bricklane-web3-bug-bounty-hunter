---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-30-cyfrin-accountable-pr75-v2-0-3-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-06-30T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-30-cyfrin-accountable-pr75-v2-0
title: '`DepositGateway::_passEpoch` re-reads strategy NAV every caller already fetched'
vuln_class: []
---

# `DepositGateway::_passEpoch` re-reads strategy NAV every caller already fetched

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-30-cyfrin-accountable-pr75-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md)_

---

**Description:** `DepositGateway::_passEpoch` calls `strategy_.lastNavMeasuredAt()` again even though every caller has just read it: `onNavUpdate` (via the status path), `forcePassEpoch` at line 153, and `_openEpochIfNeeded` at lines 249/263 all read `lastNavMeasuredAt` immediately before invoking `_passEpoch`, with no intervening write. The re-read inside `_passEpoch` issues a redundant cross-contract STATICCALL on the epoch-close path.

```solidity
DepositGateway.sol
153:        if (strategy_.lastNavMeasuredAt() <= epochs[epochId].openNavMeasuredAt) {
157:        uint256 nav = _passEpoch(epochId, strategy_);
249:            if (strategy_.lastNavMeasuredAt() <= epochs[epochId].openNavMeasuredAt) {
263:        epoch.openNavMeasuredAt = strategy_.lastNavMeasuredAt();
271:        navMeasuredAt = strategy_.lastNavMeasuredAt();
```

**Recommended Mitigation:** Change `_passEpoch(uint256 epochId, IMinimalStrategy strategy_)` to accept the NAV value the caller already holds (e.g. `_passEpoch(uint256 epochId, uint256 navMeasuredAt)`), removing the redundant `lastNavMeasuredAt` STATICCALL.

**Accountable:** Fixed in commit [`aea937c`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/aea937ccb0d39600236526c1dbcfe78fadbb3865)

**Cyfrin:** Verified.
