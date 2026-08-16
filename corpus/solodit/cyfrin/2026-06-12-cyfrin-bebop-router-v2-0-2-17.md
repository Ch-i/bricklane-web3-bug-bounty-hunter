---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-12-cyfrin-bebop-router-v2-0-2-17
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-06-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-12-cyfrin-bebop-router-v2-0
title: '`BebopPmmSwap` event emit reverts on aggregate orders with a dust last refundable
  maker'
vuln_class: []
---

# `BebopPmmSwap` event emit reverts on aggregate orders with a dust last refundable maker

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-12-cyfrin-bebop-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md)_

---

**Description:** In `_distributeMakerRefundAndEmit` the maker refund is split across makers by their last-leg amount. Every maker except the highest-index refundable one gets a floor-truncated proportional share, and the highest-index refundable maker (`lastRefundableMaker`) absorbs the leftover dust as `totalMakerRefund - refundDistributed`.

https://github.com/bebop-dex/bebop-rfqa/blob/main/contracts/BebopRouter.sol#L512-L519

```solidity
uint256 refundDistributed;
for (uint256 i; i < pmm.makerAddresses.length; ++i) {
    uint256 makerRefund;
    if (totalMakerRefund > 0 && pmm.lastLegAmounts[i] > 0) {
        makerRefund = i == lastRefundableMaker
            ? totalMakerRefund - refundDistributed
            : (totalMakerRefund * pmm.lastLegAmounts[i]) / totalLastLeg;
        refundDistributed += makerRefund;
```

The event then emits the maker balance change as an unchecked subtraction.

https://github.com/bebop-dex/bebop-rfqa/blob/main/contracts/BebopRouter.sol#L532-L547

```solidity
uint256 scaledMakerAmt = (legs[j].makerAmount * calc.newFromAmount) / pmm.pmmTakerAmount;

bool isLastLeg = legs[j].makerToken == order.pmmToToken;
uint256 legRefund = isLastLeg ? makerRefund : 0;

emit BebopPmmSwap(
    ...
    scaledMakerAmt - legRefund,  // real maker balance change
    legRefund
);
```

For a single-last-leg maker, `legs[j].makerAmount` equals `lastLegAmounts[i]`, so at a full fill `scaledMakerAmt` equals `lastLegAmounts[i]`. The truncation lost by earlier makers is bounded by the maker count, and all of it lands on `lastRefundableMaker`. When that maker has a tiny `lastLegAmounts[i]`, its `legRefund` can exceed its own `scaledMakerAmt`, and `scaledMakerAmt - legRefund` underflows.

Concrete trace with `lastLegAmounts = [50, 50, 50, 50, 1]`, `totalLastLeg = 201`, `totalMakerRefund = 10`, full fill:

- makers 0 to 3 each get `floor(10 * 50 / 201) = 2`, so `refundDistributed = 8`
- maker 4 gets `10 - 8 = 2`, but its `scaledMakerAmt = 1`
- `1 - 2` reverts

**Impact:** DoS of the affected order only. The transaction reverts atomically, the router nonce rolls back, and the user can re-quote. There is no fund loss and no theft.

Reachability is narrow. The underflow needs the highest-index refundable maker's last-leg amount, in raw token units, to be smaller than the accumulated truncation loss, which is bounded by the maker count. For normal 18 decimal or 6 decimal tokens this is sub-dust and will not appear in a real aggregate quote. It is realistic only for pathological dust orders or very low decimal tokens, and a maker cannot place itself at the highest index, so it is a robustness gap rather than an attacker-controlled path. Severity is Low.

**Recommended Mitigation:** Clamp the event subtraction so it cannot underflow.

```diff
+ uint256 emitMakerAmt = legRefund > scaledMakerAmt ? 0 : scaledMakerAmt - legRefund;
  emit BebopPmmSwap(
      ...
-     scaledMakerAmt - legRefund,
+     emitMakerAmt,
      legRefund
  );
```

This removes the only failure point. The token transfers in `_distributeMakerRefundAndEmit` already succeed because the distributed refunds always sum to `totalMakerRefund`, which is bounded by the fee pool.

**Bebop:** Fixed in commit [9db95bc](https://github.com/bebop-dex/bebop-rfqa/commit/9db95bc2b423d9317c149e90a70ae51565e26367).

**Cyfrin:**
Verified.

\clearpage
