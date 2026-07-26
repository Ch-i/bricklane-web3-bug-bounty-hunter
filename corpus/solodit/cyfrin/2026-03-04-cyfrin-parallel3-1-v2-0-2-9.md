---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-parallel3-1-v2-0-2-9
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-03-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-04-cyfrin-parallel3-1-v2-0
title: '`BridgeableTokenP::getMaxDebitableAmount` doesn''t account for isolate mode,
  returning inflated values'
vuln_class: []
---

# `BridgeableTokenP::getMaxDebitableAmount` doesn't account for isolate mode, returning inflated values

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-parallel3.1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md)_

---

**Description:** When isolate mode is on, `BridgeableTokenP::_debit` enforces that `creditDebitBalance` stays `>= 0` after debiting:

```solidity
if (isIsolateMode) {
    if (creditDebitBalance < 0) revert ErrorsLib.IsolateModeLimitReach();
}
```

This effectively caps the max debit at the current `creditDebitBalance`. But `BridgeableTokenP::getMaxDebitableAmount` doesn't factor this in — it only considers the global and daily limits:

```solidity
function getMaxDebitableAmount() external view returns (uint256) {
    if (isIsolateMode && creditDebitBalance < 0) return 0;
    if (creditDebitBalance <= globalDebitLimit) return 0;
    uint256 globalMax = MathLib.abs(globalDebitLimit - creditDebitBalance);
    ...
    return MathLib.min(globalMax, dailyMax);
}
```

So the view can report, say, 500 as the max debitable when in practice only 50 can go through before isolate mode reverts.

There's also a minor off-by-one in the early return: the guard checks `creditDebitBalance < 0` instead of `<= 0`. When the balance is exactly 0, the function doesn't bail out early and returns a non-zero value, even though any debit at that point would revert.

**Impact:** Any user or integrating contract that relies on this view to build transactions will show an incorrect max. Transactions built on top of this will revert, wasting gas.

**Proof of Concept:** Assume `isIsolateMode = true`, `creditDebitBalance = 50`, `globalDebitLimit = -1000`, `dailyDebitLimit = 500`, no daily usage yet.

1. A user calls `getMaxDebitableAmount()` — it computes `globalMax = 1050`, `dailyMax = 500`, returns `500`
2. User submits a debit of 51 tokens trusting the view output
3. Inside `_debit`, balance goes to `50 - 51 = -1`
4. Isolate mode check catches it and reverts with `IsolateModeLimitReach`

The real cap here is 50, not 500.

**Recommended Mitigation:** Two changes: fix the `< 0` guard to `<= 0`, and cap the result by `creditDebitBalance` when in isolate mode:

```solidity
function getMaxDebitableAmount() external view returns (uint256) {
    if (isIsolateMode && creditDebitBalance <= 0) return 0;
    if (creditDebitBalance <= globalDebitLimit) return 0;
    uint256 globalMax = MathLib.abs(globalDebitLimit - creditDebitBalance);
    uint256 currentDebitAmount = dailyDebitAmount[_getCurrentDay()];
    uint256 dailyMax = dailyDebitLimit > currentDebitAmount
        ? dailyDebitLimit - currentDebitAmount
        : 0;
    uint256 result = MathLib.min(globalMax, dailyMax);
    if (isIsolateMode) return MathLib.min(result, uint256(creditDebitBalance));
    return result;
}
```

**Parallel:** Fixed in commit [6735f32](https://github.com/parallel-protocol/parrallel-tokens/commit/6735f32b21b888f53ca8ef08c96a5bfab498f2dd).

**Cyfrin:** Verified. Remediated by implementing the recommended mitigation, `BridgeableTokenP::getMaxDebitableAmount` now correctly caps the limits when `isolateMode` is enabled.


\clearpage
