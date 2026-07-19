---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-30-cyfrin-accountable-pr75-v2-0-1-6
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
title: '`AccountableYield::acceptTerms` writes new penalty parameters before accruing,
  mispricing the proposal-to-acceptance window'
vuln_class: []
---

# `AccountableYield::acceptTerms` writes new penalty parameters before accruing, mispricing the proposal-to-acceptance window

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-30-cyfrin-accountable-pr75-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md)_

---

**Description:** The manager-side `updateTerms` correctly calls `_accruePenalties()` before storing the pending terms (line 123), settling the period up to the proposal at the old rate. The borrower-side `acceptTerms` does the opposite. In the ongoing-loan branch it writes the new `lateInterestPenalty` and `lateInterestGracePeriod` into `_loan` first (lines 161-162) and only then calls `_updateDelinquentStatus` (line 166), which fires `_accruePenalties` using the already-mutated values:

```solidity
_loan.lateInterestPenalty = terms.lateInterestPenalty;
_loan.lateInterestGracePeriod = terms.lateInterestGracePeriod; // new (extended) grace
...
_updateDelinquentStatus(); // -> _accruePenalties() reads the NEW grace period
```

`_accruePenalties` computes `graceEnd = delinquencyStart + _loan.lateInterestGracePeriod`. With the extended grace period, if `block.timestamp <= graceEnd` it returns early, accruing zero penalties for the whole window since the last accrual. Even a partial extension skips the segment between `_lastPenaltyTime` and the new `graceEnd`, because `penaltyStart = max(_lastPenaltyTime, graceEnd)`.

The same ordering also misprices in the opposite direction. If the accepted terms raise `lateInterestPenalty` and the window is already past grace (`block.timestamp > graceEnd`), `_accruePenalties` reads the new `lateInterestPenalty` (written at line 161 before the accrual fires) and charges the entire proposal-to-acceptance window at the new higher rate (`penaltyAmount = _totalAssets * newRate * penaltyTime`) rather than the rate that was actually in effect during that window.

**Impact:** Whichever way the terms move, the proposal-to-acceptance window is settled under the new parameters rather than the old ones: extending the grace period erases penalty income owed to depositors for that window, while raising the rate overcharges the borrower for it.

**Recommended Mitigation:** Settle penalties at the old terms before mutating them, mirroring the ordering already used in `updateTerms`:

```diff
+    // Settle penalties at the OLD terms before overwriting them (mirror updateTerms)
+    _accruePenalties();
+
     _loan.minRedeem = terms.minRedeem;
     _loan.minDeposit = terms.minDeposit;
     _loan.maxCapacity = terms.maxCapacity;
     _loan.interestInterval = terms.interestInterval;
     _loan.lateInterestPenalty = terms.lateInterestPenalty;
     _loan.lateInterestGracePeriod = terms.lateInterestGracePeriod;
```

**Accountable:** Fixed in commit [`c54cb88`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/c54cb88b1c6fb3c757eea876a74534d4725903b7)

**Cyfrin:** Verified. `acceptTerms` now accrues penalties against the existing parameters before writing the new ones, so the proposal-to-acceptance window is priced correctly.


\clearpage
