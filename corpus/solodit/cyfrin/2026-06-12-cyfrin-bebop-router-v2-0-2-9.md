---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-12-cyfrin-bebop-router-v2-0-2-9
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-06-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-12-cyfrin-bebop-router-v2-0
title: '`BebopRouter::_distributeFees` derives `feePool` from the absolute `pmmToToken`
  balance rather than a per-swap delta, sweeping prior or donated balance to treasury
  as positive slippage'
vuln_class: []
---

# `BebopRouter::_distributeFees` derives `feePool` from the absolute `pmmToToken` balance rather than a per-swap delta, sweeping prior or donated balance to treasury as positive slippage

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-12-cyfrin-bebop-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md)_

---

**Description:** `_distributeFees` reads the router's absolute `pmmToToken` balance and computes the fee pool from that full balance:

```solidity
// contracts/BebopRouter.sol:450-489
uint256 pmmToBalance = IERC20(order.pmmToToken).balanceOf(address(this));

uint256 feePool = pmmToBalance > calc.toAmountAfterFeeSlippage
    ? pmmToBalance - calc.toAmountAfterFeeSlippage
    : 0;
...
uint256 positiveSlippage = feePool > theoreticalTotal ? feePool - theoreticalTotal : 0;
...
uint256 toTreasury = protocolFeeShare + protocolSlippageShare + positiveSlippage;
...
if (toTreasury > 0) {
    IERC20(order.pmmToToken).safeTransfer(protocolTreasury, toTreasury);
}
```

Because no pre-swap balance snapshot is taken, any `pmmToToken` already held by the router is included in `feePool`. If that incidental balance pushes `feePool` above `theoreticalTotal`, it is classified as positive slippage and transferred to `protocolTreasury`, even though it was not delivered by the current swap's makers.

**Files:**

- `contracts/BebopRouter.sol` - `BebopRouter::_distributeFees`

**Impact:** Pre-existing `pmmToToken` in the router can be classified as positive slippage and transferred to `protocolTreasury`, misattributing value that did not arise from the current swap's maker delivery. The magnitude depends on the incidental balance present at the time of the swap.

**Recommended Mitigation:** Snapshot `IERC20(order.pmmToToken).balanceOf(address(this))` immediately before the PMM call and use `balanceAfter - balanceBefore` as the delivered amount for computing `feePool`. This ensures only the tokens actually delivered by this swap's makers enter the fee distribution.

**Bebop:** Acknowledged.
