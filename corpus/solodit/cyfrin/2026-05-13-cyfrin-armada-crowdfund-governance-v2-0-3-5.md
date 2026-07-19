---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-3-5
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: 'Event correctness gaps: incomplete emissions, missing indexed params, and
  semantic mismatches'
vuln_class: []
---

# Event correctness gaps: incomplete emissions, missing indexed params, and semantic mismatches

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** Enumerated sub-items covering event semantics and indexing across the in-scope contracts.

1. **`ArmadaRedemption::redeem`** emits `Redeemed(redeemer, armAmount, tokens, ethAmount)` but not per-token payout amounts. Tokens with `share == 0` are silently skipped inside the loop, so the event asserts something the contract did not do. Change to `Redeemed(address indexed redeemer, uint256 armAmount, address[] tokens, uint256[] amounts, uint256 ethAmount)` or emit a per-token `TokenRedeemed(redeemer, token, share)` inside the loop.

2. **`ArmadaGovernor::ProposalCreated`** does not index `proposalType` despite a free topic slot. Dashboards filter governance proposals by type constantly. Mark `ProposalType indexed proposalType`.

3. **`ArmadaCrowdfund::Cancelled`** emits with no payload. Add `Cancelled(address indexed caller, uint256 timestamp)` for indexer attribution.

4. **`TreasurySteward::removeSteward`** emits `StewardRemoved(currentSteward)` before zeroing storage and without guarding against `currentSteward == address(0)`. Add `require(currentSteward != address(0))` at entry and move the `emit` to after the state write.

5. **`ArmadaToken::addToWhitelist, addAuthorizedDelegator`** set `mapping[account] = true` unconditionally and emit even on idempotent re-adds. Gate the emit on `!transferWhitelist[account]` / `!authorizedDelegator[account]` (or revert with a same-value error).

6. **`RevenueLock::_updateMaxObservedRevenue`** always writes `lastSyncTimestamp = block.timestamp` but emits `ObservedRevenueUpdated` only on the advance branch. Monitoring bots that subscribe to events cannot observe no-op syncs even though the contract did advance the sync timestamp and consume the elapsed-time budget. Emit a lightweight `Synced(timestamp, reported, maxObservedRevenue)` on every call, or document explicitly that monitors must poll storage.

7. **`ArmadaTreasuryGov::removeStewardBudgetToken`** wipes `_stewardSpendHistory[token]` as well as `stewardBudgets[token]` but only emits `StewardBudgetTokenRemoved(token)`. Off-chain analytics cannot detect the history wipe. Emit a companion `StewardSpendHistoryCleared(token, uint256 recordsCleared)`.

8. **`ArmadaWindDown::triggerWindDown, governanceTriggerWindDown`** both emit the same `WindDownTriggered(caller, timestamp)`. Add a boolean to distinguish governance-forced from revenue-triggered wind-down.

9. **`ArmadaCrowdfund::Finalized`** in both refund-mode paths emits zero for `allocatedArm` and `netProceeds`; the `cappedDemand < MIN_SALE` branch additionally emits `saleSize = 0`. Post-mortem dashboards cannot distinguish "aborted before sizing" from "sized at zero". Extend the event to include `cappedDemand` and `totalCommitted`.

10. **`ArmadaGovernor::setSecurityCouncil`** emits `SecurityCouncilUpdated` before the state write. `RevenueCounter::setFeeCollector` has the same pattern. Reorder so events follow state changes.

11. **`ArmadaCrowdfund::Committed, Invited`** do not index `hop` despite one indexed slot remaining and `AllocatedHop` already indexing hop. Mark `uint8 indexed hop`.

12. **`ArmadaCrowdfund::Allocated`** semantics with `delegate == address(0)` would be interpreted ambiguously by an indexer; the claim path always sets a delegatee (defaults to `msg.sender`), but the event's optional-delegatee slot should be documented.

**Impact:** Event correctness gaps hinder off-chain indexers and monitoring tools. No direct on-chain fund loss.

**Recommended Mitigation:** Apply the per-subitem mitigations enumerated above.

**Armada:** Fixed in commit [0f298df](https://github.com/ship-armada/armada-poc/commit/0f298dff07a08a02f2574440e603dd0f58d63dfc0).

**Cyfrin:** Verified with the following notes:
* 7 no longer applies as that history deletion was removed as part of another mitigation
* 1 and 12 have not been implemented (though 12 was just a documentation update)
