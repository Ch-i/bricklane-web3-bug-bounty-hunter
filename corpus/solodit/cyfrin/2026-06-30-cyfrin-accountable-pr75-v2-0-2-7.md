---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-30-cyfrin-accountable-pr75-v2-0-2-7
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-06-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-30-cyfrin-accountable-pr75-v2-0
title: '`DepositGateway::_passEpoch` passes an emptied epoch into `Passed` where it
  never finalizes to `Settled`'
vuln_class: []
---

# `DepositGateway::_passEpoch` passes an emptied epoch into `Passed` where it never finalizes to `Settled`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-30-cyfrin-accountable-pr75-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md)_

---

**Description:** `cancelDeposit` decrements `epoch.pendingCount` but does not change `epoch.status` or `currentOpenEpochId` (`src/modules/DepositGateway.sol:113-132`), so when every request in the open epoch is cancelled the epoch is left `Open` with `pendingCount == 0`. `_passEpoch` then closes such an epoch to `Passed` unconditionally - it never checks `pendingCount` (`src/modules/DepositGateway.sol:269-277`). The `pendingCount == 0` finalization that flips an epoch to `Settled` exists only inside `settle` (`src/modules/DepositGateway.sol:186`) and `refund` (`src/modules/DepositGateway.sol:212`), so an emptied epoch passed by `onNavUpdate` (or force-passed via `_openEpochIfNeeded` or `forcePassEpoch`) lands in `Passed` with no pending requests and no path that auto-finalizes it. It emits `EpochPassed` for an epoch holding no live deposits and never emits `EpochSettled`, lingering in `Passed` indefinitely unless someone calls `settle(epochId, new uint256[](0))`, whose post-loop `pendingCount == 0` check then flips it to `Settled`.

No funds or liveness are affected: the escrow was already returned on cancel, `unsettledEscrow` was decremented, and `currentOpenEpochId` is zeroed at pass so the next request opens a fresh epoch. The impact is observational. Off-chain epoch-lifecycle trackers that expect every `Passed` epoch to eventually emit `EpochSettled` see the empty epoch stuck in `Passed` forever, and settle-scanning keepers keep surfacing it as outstanding. It is reachable in normal operation: a sole subscriber who deposits then cancels (a cost-free action) before the NAV leaves the epoch empty when it passes.

**Files:**

- `DepositGateway::_passEpoch` (`src/modules/DepositGateway.sol`)
- `DepositGateway::cancelDeposit` (`src/modules/DepositGateway.sol`)

**Recommended Mitigation:** Finalize empty epochs at pass time. In `_passEpoch`, when `epoch.pendingCount == 0`, set `epoch.status = EpochStatus.Settled` and emit `EpochSettled` instead of leaving the epoch `Passed`, or skip passing an epoch that has no pending requests. Either keeps the epoch lifecycle observable off-chain and removes the lingering empty `Passed` state.

**Accountable:** Fixed in commit [`aea937c`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/aea937ccb0d39600236526c1dbcfe78fadbb3865)

**Cyfrin:** Verified.
