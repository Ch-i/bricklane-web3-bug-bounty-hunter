---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-30-cyfrin-accountable-pr75-v2-0-3-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-06-30T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-30-cyfrin-accountable-pr75-v2-0
title: '`DepositGateway::_passEpoch` re-derives the `epochs[epochId]` storage pointer
  the callers already hold'
vuln_class: []
---

# `DepositGateway::_passEpoch` re-derives the `epochs[epochId]` storage pointer the callers already hold

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-30-cyfrin-accountable-pr75-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md)_

---

**Description:** `DepositGateway::onNavUpdate` and `forcePassEpoch` already hold (or compute) the `epochs[epochId]` storage slot, then call `_passEpoch(epochId, ...)`, which re-hashes `keccak256(epochId . slot)` to re-derive the same `Epoch storage` pointer. With the optimizer off, the pointer derivation and the `status` read are not deduped across the call boundary. Passing the already-derived `Epoch storage` pointer (or caching it) avoids one mapping-slot re-derivation plus the extra cold/warm SLOAD per close. This is a low-frequency path (NAV publish / recovery), so the savings are modest, but the dedup is guaranteed under optimizer-off.

```solidity
DepositGateway.sol
139:        if (epochs[epochId].status != EpochStatus.Open) return; // unexpected - no-op, never revert
141:        uint256 nav = _passEpoch(epochId, IMinimalStrategy(strategy));

153:        if (strategy_.lastNavMeasuredAt() <= epochs[epochId].openNavMeasuredAt) {
157:        uint256 nav = _passEpoch(epochId, strategy_);

269:    function _passEpoch(uint256 epochId, IMinimalStrategy strategy_) private returns (uint256 navMeasuredAt) {
270:        Epoch storage epoch = epochs[epochId];
```

**Recommended Mitigation:** Change `_passEpoch` to take an `Epoch storage epoch` parameter (the `epochId` is otherwise needed only for the lookup), and have each caller pass the pointer it already read. For example, in `onNavUpdate` cache `Epoch storage epoch = epochs[epochId];` once, gate on `epoch.status`, and call `_passEpoch(epoch, ...)`.

**Accountable:** Fixed in commit [`aea937c`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/aea937ccb0d39600236526c1dbcfe78fadbb3865)

**Cyfrin:** Verified.
