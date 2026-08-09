---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-25-cyfrin-predict-cre-integration-v2-1-1-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-04-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-25-cyfrin-predict-cre-integration-v2-1
title: '`enableRoundConfig` skips `_validateInterval` check allowing re-activation
  for invalidated intervals'
vuln_class: []
---

# `enableRoundConfig` skips `_validateInterval` check allowing re-activation for invalidated intervals

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-25-cyfrin-predict-cre-integration-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md)_

---

**Description:** Both `initialize()` (`ChainlinkUpDownAdapter.sol:70`) and `extend()` (`ChainlinkUpDownAdapter.sol:86`) call
  `_validateInterval(interval)` before operating which enforces the `isIntervalValid allowlist. enableRoundConfig()`
  (`ChainlinkUpDownAdapter.sol:155`) does not. An admin can therefore call `enableRoundConfig` for an interval that was explicitly invalidated via `updateIsIntervalValid(interval, false)` bypassing the interval governance policy.

Once re-enabled, the series runs normally: the CRE delivers reports, `_closeRound` resolves markets and rolls forward indefinitely (rolling creation in `_closeRound` also does not check `isIntervalValid` consistent with M-4 design. The disallowed interval remains operationally active with no further admin action required to sustain it.

Example:
```typescript
  // Setup — interval valid, series running normally
  updateIsIntervalValid(300, true)
  initialize(FEED_A, 300, T0, price, 3)   // creates rounds at T0, T0+300, T0+600

  // Policy change — deprecate 5-min interval
  disableRoundConfig(FEED_A, 300)          // stops rolling creation
  // CRE winds down: closes rounds at T0, T0+300, T0+600

  updateIsIntervalValid(300, false)        // interval now policy-disallowed

  // Verify gates work for lesser roles:
  extend(FEED_A, 300, 3)                   // REVERTS: InvalidInterval ✓
  initialize(FEED_B, 300, T1, price, 3)   // REVERTS: InvalidInterval ✓

  // But admin can still bypass:
  enableRoundConfig(FEED_A, 300, T1, price, 3)  // SUCCEEDS — no _validateInterval call
  // FEED_A/300 series now live again on a disallowed interval
  // _closeRound rolling creation sustains it indefinitely
```

**Impact:** `DEFAULT_ADMIN_ROLE` can silently re-activate a market series for a disallowed interval without first re-enabling the interval. In a multi-admin setup, Admin `A` may invalidate an interval as a policy decision ("this interval is deprecated"), while Admin `B` calls `enableRoundConfig` without realizing the interval is disallowed.

So the check that should surface the conflict is absent. The active series then continues indefinitely on a policy-disallowed interval `via _closeRound` rolling creation.

**Proof of Concept:**
```typescript

  1. Admin: `updateIsIntervalValid(300, true)`
  2. Initializer: `initialize(FEED, 300, T0, price, 3)`
  3. Admin: `disableRoundConfig(FEED, 300`)
  4. CRE closes all 3 pre-created rounds (wind-down complete)
  5. Admin: `updateIsIntervalValid(300, false)`  // interval now invalid
  6. Extender: `extend(FEED, 300, 3)`            → REVERTS with InvalidInterval ✓
  7. Initializer: `initialize(FEED2, 300, ...)`  → REVERTS with InvalidInterval ✓

  8. Admin: `enableRoundConfig(FEED, 300, newTs, price, 3)` → SUCCEEDS ✗ (no interval check)
// Series now live on disallowed interval; rolling creation sustains indefinitely
```
Note: `_validateRoundConfigInitialized` (L342) does not prevent this, it only checks that both timestamps are non-zero, which they are (set during the original `initialize()` call and unchanged by `disableRoundConfig)`.

**Recommended Mitigation:** Add `_validateInterval(interval)` at the top of `enableRoundConfig`, consistent with `initialize()` (L70) and extend() (L86):

```solidity
  function enableRoundConfig(
      bytes32 feedId,
      uint32 interval,
      uint32 newCurrentRoundStartTimestamp,
      int192 startPrice,
      uint256 roundCount
  ) external onlyRole(DEFAULT_ADMIN_ROLE) {
      _validateInterval(interval);  // ADD THIS
      RoundConfig storage roundConfig = _getCurrentRoundConfig(feedId, interval);
      // ...
  }
```

**Predict.fun:** Fixed in commit [0065ac](https://github.com/PredictDotFun/prediction-market/pull/71/changes/0065ac46211c299a1c89ec5d811ed29b42e3fcc1).

**Cyfrin:** Verified.

\clearpage
