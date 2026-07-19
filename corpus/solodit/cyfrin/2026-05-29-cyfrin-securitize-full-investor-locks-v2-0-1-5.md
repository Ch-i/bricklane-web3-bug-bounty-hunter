---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-29-cyfrin-securitize-full-investor-locks-v2-0-1-5
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-05-29T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-29-cyfrin-securitize-full-investor-locks-v2-0
title: '`RegistryService::removeInvestor` does not clear downstream state; recycled
  investor IDs inherit stale lockups'
vuln_class: []
---

# `RegistryService::removeInvestor` does not clear downstream state; recycled investor IDs inherit stale lockups

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md)_

---

**Description:** `RegistryService::removeInvestor` is the only path that retires an investor record. After verifying `walletCount == 0`, it iterates the sixteen attribute slots, deletes them, and deletes `investors[_id]`. The function performs no cross-contract cleanup. Two distinct off-contract per-ID state surfaces remain populated for the same `_id`:

**Component 1: Stale issuance lock-up state in `ComplianceServiceRegulated`.** Each call to `recordIssuance` (line 623-636) and the new-investor incoming branch of `recordTransfer` invoke `createIssuanceInformation` (line 737-749), which writes `issuancesValues[_id][n] = shares`, `issuancesTimestamps[_id][n] = time`, and increments `issuancesCounters[_id]`. `cleanupInvestorIssuances` (line 890-932) only evicts entries whose timestamp has aged past the configured `lockTime`; entries that are still inside the lock-up window are preserved. When `removeInvestor` runs against an investor whose balance was just zeroed but whose most recent issuance is still within the US Reg-D / Rule 144 hold window, those records survive the delete. The investor record is gone from `RegistryService`, but the `issuancesCounters[_id]` mapping in `ComplianceServiceRegulated` still reports a non-zero count for that same string key.

**Component 2: Stale lock state in `InvestorLockManager`.** `InvestorLockManager` (out of scope) maintains per-investor state keyed by the same `_id` string at `contracts/data-stores/InvestorLockManagerDataStore.sol:24-29`: `investorsLocks[_id][lockId]`, `investorsLocksCounts[_id]`, `investorsLocked[_id]`, `investorsLiquidateOnly[_id]`, `investorsPartitionsLocks[_id][partition][lockId]`, and `investorsPartitionsLocksCounts[_id][partition]`. This state pre-existed BC-1779; the full-investor-lock changeset added a new in-scope consumer of it (the `isInvestorLocked` check at `doPreTransferCheckRegulated:214` and the `getTransferableTokens` partial-lock check at `:220`) alongside the pre-existing `isInvestorLiquidateOnly` consumer at `completeTransferCheck:259`. `RegistryService::removeInvestor` does not call into `InvestorLockManager` to clear any of this state. Whether `isInvestorLocked(_id)` and `isInvestorLiquidateOnly(_id)` continue to return their previous values after the registry delete depends entirely on `InvestorLockManager`'s internal semantics; the registry contract makes no guarantee in either direction.

A subsequent re-registration of the same `_id` via `registerInvestor` (line 37-43) succeeds because `newInvestor(_id)` only checks `!isInvestor(_id)`, which the prior `delete` satisfied. The new holder of that string identifier now inherits whatever residual state the two downstream contracts retain.

**Files:**

- `contracts/registry/RegistryService.sol` (`RegistryService::removeInvestor`)
- `contracts/compliance/ComplianceServiceRegulated.sol` (issuance lock-up state)
- `contracts/compliance/InvestorLockManager.sol` (per-investor lock state)

**Impact:** On a recycled investor-id, the new investor inherits the prior holder's residual state in both downstream contracts. From the issuance side: if the prior holder had Reg-D issuance records still inside the lockup window, `getComplianceTransferableTokens` for the new investor walks `issuancesValues[id][0..issuancesCounters[id] - 1]` and sums those still inside the lock window into the locked total; if that total exceeds the new holder's freshly-issued balance, `transferable = 0` and every transfer reverts with `TOKENS_LOCKED` until the stale timestamps age past `lockTime`. From the lock-manager side: if `investorsLocked[id]` or `investorsLiquidateOnly[id]` was set on the prior holder, the flags persist and every transfer reverts at the full-investor-lock check (`TOKENS_LOCKED`) or the liquidate-only gate (`INVESTOR_LIQUIDATE_ONLY`, code 90). No public setter in scope clears `issuancesCounters[id]` or the lock manager's per-id maps; recovery is wait-out (let the lockup records age out) or contract upgrade.

**Recommended Mitigation:** Add a per-component `onlyRegistry`-gated cleanup function on each affected contract and call it from `removeInvestor` after the `walletCount == 0` check passes and before the `delete investors[_id]` line:

- On `ComplianceServiceRegulated`, add `clearInvestorIssuances(string memory _id) external onlyRegistry` that loops `for (uint256 i = 0; i < issuancesCounters[_id]; i++) { delete issuancesValues[_id][i]; delete issuancesTimestamps[_id][i]; }` and then sets `issuancesCounters[_id] = 0`.
- On `InvestorLockManager`, add `clearInvestorLockState(string memory _id) external onlyRegistry` that deletes `investorsLocked[_id]`, `investorsLiquidateOnly[_id]`, every `investorsLocks[_id][i]` entry for `i` in `0..investorsLocksCounts[_id] - 1`, `investorsLocksCounts[_id]`, and the per-ID `investorsPartitionsLocks` / `investorsPartitionsLocksCounts` entries for every partition the investor held locks on. Partitions are not enumerable from the data store, so either pass the partition list as a parameter or restructure the storage to track per-id partition membership.

Alternatively, defend at the entry point: in `registerInvestor`, refuse the call when `issuancesCounters[_id] > 0` or when `InvestorLockManager` reports any residual state for `_id`. That preserves the silent-recycle as a no-op rather than a state-inheritance carry-over.


**Securitize:** Acknowledged.
