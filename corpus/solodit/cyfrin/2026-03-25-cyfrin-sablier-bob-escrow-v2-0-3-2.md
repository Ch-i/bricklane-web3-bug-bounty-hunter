---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-3-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-03-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-25-cyfrin-sablier-bob-escrow-v2-0
title: '`SablierEscrow::fillOrder` lacks deadline parameter for buyer protection,
  same with swaps in `SablierLidoAdapter::_wstETHToWeth`'
vuln_class: []
---

# `SablierEscrow::fillOrder` lacks deadline parameter for buyer protection, same with swaps in `SablierLidoAdapter::_wstETHToWeth`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md)_

---

**Description:** `SablierEscrow::fillOrder` (`SablierEscrow.sol:167-243`) has no deadline/expiry parameter for the buyer's transaction. A buyer's fill transaction can sit in the mempool indefinitely and execute at a later time when market conditions have changed unfavorably.

**Impact:** A buyer submits a fill transaction at a favorable price. The transaction gets stuck in the mempool (low gas, network congestion). By the time it executes, the market price has moved significantly such that the buyer would have never filled in the current conditions. The buyer has no protection against stale execution; this is analogous to the well-known missing deadline parameter in AMM swaps.

**Recommended Mitigation:** Add an optional `deadline` parameter to `fillOrder`:
```solidity
function fillOrder(uint256 orderId, uint128 buyAmount, uint40 deadline) external {
    if (deadline > 0 && block.timestamp > deadline) {
        revert Errors.SablierEscrow_Expired(deadline);
    }
    // ... rest of function
}
```

Similarly swaps occur inside `SablierLidoAdapter::_wstETHToWeth` but these transactions also don't have a deadline input.

**Sablier:** Acknowledged; we believe that, unlike AMMs, the setup here is different because:
(i) in case the order has a specific buyer set, they know preemptively what the minimum price they will pay for is - and we expect it to be used as `buyAmount == minBuyAmount` - and there is no change to `minBuyAmount` during the time the tx is signed and actually included in the block (i.e. the time in the mempool)
(ii) the order doesn’t have a buyer set: here we expect to have a “race” condition for who gets the tx first - whether it’s a human or an MEV bot.
