---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-29-cyfrin-securitize-full-investor-locks-v2-0-1-6
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-05-29T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-29-cyfrin-securitize-full-investor-locks-v2-0
title: '`ComplianceServiceRegulated::recordBurn` and `recordSeize` skip lockup cleanup;
  stale records over-lock later inbound'
vuln_class: []
---

# `ComplianceServiceRegulated::recordBurn` and `recordSeize` skip lockup cleanup; stale records over-lock later inbound

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md)_

---

**Description:** The compliance bookkeeping hooks have asymmetric cleanup behavior. `recordTransfer` and `recordIssuance` both invoke `cleanupInvestorIssuances` against the relevant investor(s) before processing: `recordTransfer` cleans both the sender and the receiver leg, `recordIssuance` cleans the receiver. `recordBurn` and `recordSeize` decrement counters and adjust per-region bookkeeping but never call `cleanupInvestorIssuances`. The result is that an investor whose balance is fully burned or seized retains every `issuancesValues[_id][i]`, `issuancesTimestamps[_id][i]`, and `issuancesCounters[_id]` entry in storage, even though they currently hold zero tokens.

When that same investor later receives a fresh inbound transfer or issuance, the receiver-leg cleanup at the start of the inbound hook prunes only entries whose timestamps have aged past `lockTime`. Entries that are still inside the lock window survive. The freshly-credited balance is now evaluated against `getComplianceTransferableTokens`, which sums every still-active issuance value into `totalLockedTokens`. If the stale pre-burn issuance value matches or exceeds the new inbound balance, `transferable = balanceOfInvestor - min(totalLockedTokens, balanceOfInvestor) = 0`. The investor is locked out of moving the new balance until the stale timestamps age out.

**Files:**

- `contracts/compliance/ComplianceServiceRegulated.sol` (`recordBurn`, `recordSeize`, lines 638-651; `cleanupInvestorIssuances`, lines 890-932)

**Impact:** An investor whose tokens are burned or seized and who later receives a fresh inbound transfer or issuance is over-locked relative to the actual lock semantics of their current balance. A US Reg-D investor whose entire holding is seized for compliance, who then later legitimately receives a fresh issuance, finds their fresh tokens lock-treated against the seized-tokens' original timestamps, effectively double-counting lockup obligations across two distinct token cohorts. The newly-received tokens cannot transfer until the older (and now meaningless) timestamps age out. The direction is over-restriction rather than under-restriction, so this is not a regulatory bypass, but it produces user-visible bricks of fresh inbound transfers and confused error-message diagnostics: `TOKENS_LOCKED` triggered by records that no longer correspond to any held balance. Self-recoverable by waiting; admin has no setter in scope that can directly prune the stale records short of a contract upgrade.

**Recommended Mitigation:** Invoke `cleanupInvestorIssuances(_id)` from both `recordBurn` and `recordSeize` after the burn/seize accounting completes. Symmetry with `recordTransfer` (which cleans both legs) and `recordIssuance` (which cleans the receiver) is the simplest contract to state and reason about. Alternatively, when the investor's balance hits zero on burn/seize, explicitly delete every `issuancesValues[_id][i]` and `issuancesTimestamps[_id][i]` and reset `issuancesCounters[_id] = 0`. A zero-balance investor has no need to retain any pending-lock history.


**Securitize:** Acknowledged.
