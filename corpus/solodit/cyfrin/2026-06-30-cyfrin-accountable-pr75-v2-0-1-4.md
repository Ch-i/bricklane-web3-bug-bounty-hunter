---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-30-cyfrin-accountable-pr75-v2-0-1-4
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-06-30T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-30-cyfrin-accountable-pr75-v2-0
title: '`AccountableYield::_accruedFeeShares` degenerate fee-overflow early return
  advances the high-water mark without charging the fee'
vuln_class: []
---

# `AccountableYield::_accruedFeeShares` degenerate fee-overflow early return advances the high-water mark without charging the fee

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-30-cyfrin-accountable-pr75-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md)_

---

**Description:** `AccountableYield::_accruedFeeShares` (`src/strategies/AccountableYield.sol:558-603`) returns early with zero fee shares when `totalFeeAssets >= newTotalAssets`, but still returns the full `newTotalAssets`. Back in `_accrueFees` (`src/strategies/AccountableYield.sol:503-516`), the high-water-mark block then runs unconditionally: with `performanceFeeShares` and `managementFeeShares` both zero, `hwmSupply` equals the current `totalSupply`, so `postFeePrice = newTotalAssets.mulDiv(PRECISION, hwmSupply)` is the gross, un-feed share price. If that price exceeds `peakSharePrice`, the high-water mark is ratcheted up to the gross price even though no performance fee was charged on the underlying gain.

**Files:**

- `AccountableYield::_accruedFeeShares, _accrueFees` (`src/strategies/AccountableYield.sol`)

**Impact:** In the degenerate case where computed fees meet or exceed total assets, a genuine gain advances `peakSharePrice` to the gross post-gain price without that gain ever being taxed. Because the performance fee only applies to gains above the high-water mark, the un-taxed gain is permanently forgiven - a later, smaller gain measured against the inflated mark yields a reduced or zero performance fee. The protocol loses fee revenue it was otherwise entitled to; depositors are not harmed. The condition requires fees to compute to at least total assets, which is an extreme regime.

**Recommended Mitigation:** Advance the high-water mark only when fees were actually charged. Skip the `peakSharePrice` update when `_accruedFeeShares` took the degenerate early return (e.g. have it signal that no fee was charged), so the high-water mark is not ratcheted past a gain that escaped the performance fee. Ensure the normal path, where fees are minted, continues to advance the mark using the post-fee price.

**Accountable:** Fixed in commit [`aea937c`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/aea937ccb0d39600236526c1dbcfe78fadbb3865)

**Cyfrin:** Verified.
