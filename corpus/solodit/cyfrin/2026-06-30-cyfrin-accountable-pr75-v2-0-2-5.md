---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-30-cyfrin-accountable-pr75-v2-0-2-5
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-06-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-30-cyfrin-accountable-pr75-v2-0
title: 'Missing or incomplete events: absent emissions, missing indexed params and
  missing event fields'
vuln_class: []
---

# Missing or incomplete events: absent emissions, missing indexed params and missing event fields

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-30-cyfrin-accountable-pr75-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md)_

---

**Description:** PR75's event surface has four observability gaps. None is read by on-chain logic and none affects fund safety, but each breaks off-chain reconstruction by indexers, keeper dashboards, or fee-monitoring. The individual gaps:

1. **`DepositGateway::settle, refund`** emit `EpochSettled` with a stale aggregate `totalAssets`. `epoch.totalAssets` is only ever increased in `requestDeposit` and decreased in `cancelDeposit`; neither `settle` nor `refund` decrements it. So when an epoch is finalized after a mix of settlements and refunds, `EpochSettled(epochId, epoch.totalAssets)` reports the gross at-pass subscribed total, including the portion that was refunded rather than minted into vault shares. Off-chain TVL trackers and analytics that sum `EpochSettled::totalAssets` over-count assets that actually entered the vault by the total of all refunded requests in each epoch, and the discrepancy grows exactly with the operationally-expected refund triggers (de-whitelisting, capacity exceeded, raised minimum deposit).

 Source: `src/modules/DepositGateway.sol:190` (emit), `src/modules/DepositGateway.sol:175-184, 207-219` (the settle/refund finalize paths that omit the decrement).

 Recommended: track a running settled-assets accumulator on the `Epoch` and emit that in `EpochSettled` so the event is self-consistent with its name; alternatively rename the field to make explicit it is the gross subscribed total fixed at pass time so indexers do not treat it as assets-deposited-into-vault.

2. **`DepositGateway::refund`** finalizes an epoch to `Settled` without emitting `EpochSettled`. When the last pending request of a passed epoch is refunded rather than settled, `refund` sets `epoch.status = EpochStatus.Settled` and `epoch.settledAt` once `pendingCount` reaches 0, but emits only the per-request `DepositRefunded` - no `EpochSettled`. The `IDepositGateway` NatSpec documents `EpochSettled` as emitted when every request in an epoch is settled or refunded, so the refund-finalized case is an in-scope emit condition that is missing. Any off-chain epoch-lifecycle state machine that tracks finalization by listening for `EpochSettled` permanently misses the transition and shows the epoch stuck in `Passed`, even though on-chain state reads `Settled`.

 Source: `src/modules/DepositGateway.sol:212-215`.

 Recommended: inside the `if (epoch.pendingCount == 0)` block in `refund`, emit `EpochSettled(req.epochId, epoch.totalAssets)` consistent with the settle path, or factor the finalize-and-emit into a shared internal helper called from both `settle` and `refund`.

3. **`AccountableYield::reinitialize`** overwrites the fee high-water mark `peakSharePrice` with no event. `reinitialize` (the one-shot, manager/security-admin-gated migration hook) recomputes and overwrites `peakSharePrice`, which directly governs future performance-fee charges - a material accounting change that can re-enable or suppress fees on the next accrual. No event is emitted, while comparable setters (`setNavGracePeriod`, `setDepositGateway`) all emit dedicated events. A post-migration fee anomaly therefore cannot be correlated to the HWM reset off-chain.

 Source: `src/strategies/AccountableYield.sol:84-88`.

 Recommended: emit an event on reinitialization capturing the old and new `peakSharePrice` so fee-monitoring has a signal the high-water mark was reset.

4. **`DepositGateway::settle`** emits `RequestSettled` with `user` left un-indexed, while the sibling lifecycle events `DepositRequested, DepositCancelled, DepositRefunded` all index `user`. A frontend or indexer wanting all settlements for a given address cannot do a topic filter on the terminal settlement event and must scan and decode every event, an asymmetry inconsistent with the rest of the event family.

 Source: `src/modules/DepositGateway.sol:180` (emit; event declared in `IDepositGateway`).

 Recommended: mark `user` as `indexed` in the `RequestSettled` event declaration.

**Recommended Mitigation:** Apply the per-component fixes above: track and emit the actually-settled asset total (or rename the `EpochSettled` field), emit `EpochSettled` on the refund-finalized branch, emit an old/new `peakSharePrice` event in `reinitialize`, and add `indexed` to `user` in `RequestSettled`.

**Accountable:** Fixed in commit [`aea937c`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/aea937ccb0d39600236526c1dbcfe78fadbb3865)

**Cyfrin:** Verified.
