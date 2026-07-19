---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-30-cyfrin-accountable-pr75-v2-0-1-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-06-30T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-30-cyfrin-accountable-pr75-v2-0
title: '`AccountableYield::updateLateStatus` is permissionless and lacks the `whenNotStale`
  and `whenNotPaused` guards'
vuln_class: []
---

# `AccountableYield::updateLateStatus` is permissionless and lacks the `whenNotStale` and `whenNotPaused` guards

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-30-cyfrin-accountable-pr75-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md)_

---

**Description:** `AccountableYield::updateLateStatus` (`src/strategies/AccountableYield.sol:497-500`) is permissionless and carries no `whenNotStale` or `whenNotPaused` guard. It calls `_updateDelinquentStatus`, which when the loan is already delinquent calls `_accruePenalties` (`src/strategies/AccountableYield.sol:712-735`), a wall-clock accumulator that charges penalty for every second elapsed since the last penalty timestamp. The borrower's only cure path, `repay` (`src/strategies/AccountableYield.sol:327`), is gated `whenNotStale whenNotPaused`. While the strategy is paused or its NAV is stale, the borrower cannot repay, but any third party can keep calling `updateLateStatus` to keep advancing the penalty accumulator over the same window.

**Files:**

- `AccountableYield::updateLateStatus` (`src/strategies/AccountableYield.sol`)
- `AccountableYield::_accruePenalties, repay` (`src/strategies/AccountableYield.sol`)

**Impact:** During a pause or stale-NAV window the borrower is locked out of repayment while penalties continue to compound against the position. The penalties accrued over that window are charged to a position the borrower had no opportunity to cure, and `accruedPenalties` is only reduced inside `repay`, so the borrower must absorb penalties that accrued precisely when repayment was impossible. The accrual is bounded by the duration of the stale/paused window and the configured penalty rate; the borrower cannot retroactively reverse penalties already booked over that window.

**Recommended Mitigation:** Gate the penalty-advancing path so the delinquency clock does not run while the borrower's cure path is blocked. Apply `whenNotStale` and `whenNotPaused` to `updateLateStatus` (consistent with `repay`), or suspend penalty accrual in `_accruePenalties` while the strategy is paused or NAV is stale, resuming the clock from the moment repayment becomes possible again.

**Accountable:** Fixed in commit [`aea937c`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/aea937ccb0d39600236526c1dbcfe78fadbb3865)

**Cyfrin:** Verified.
