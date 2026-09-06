---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-12-cyfrin-bebop-router-v2-0-3-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-06-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-12-cyfrin-bebop-router-v2-0
title: '`BebopRouter::_getFeeAndSlippage` consumes a spot-price example oracle with
  no TWAP, letting a taker sandwich the referenced pool to zero the slippage charge'
vuln_class: []
---

# `BebopRouter::_getFeeAndSlippage` consumes a spot-price example oracle with no TWAP, letting a taker sandwich the referenced pool to zero the slippage charge

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-12-cyfrin-bebop-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md)_

---

**Description:** `_getFeeAndSlippage` (`contracts/BebopRouter.sol:385-390`) calls `IOracle(order.oracle).getSlippage(...)` at execution time and consumes the returned rate without any manipulation-resistance check or protocol-level deviation bound. The example PoolsBasedOracle referenced in the codebase derives its slippage rate from Uniswap V2 `getReserves` and V3 `slot0` - single-block spot prices with no TWAP and no observation window. `getSlippage` returns `0` whenever `currentPrice <= offchainMidPrice`. A taker who controls `order.receiver` can move the oracle's source pool in the same transaction (or via a sandwich bundle) to push currentPrice at or below offchainMidPrice, causing the oracle to return a zero slippage rate. Zeroing slippage raises `toAmountAfterFeeSlippage` (the receiver's share computed in `_calculateAmounts`) and correspondingly shrinks `feePool` in `_distributeFees`, so the slippage amount that would otherwise be refunded to makers or routed to the treasury is instead retained by the receiver. Conversely, a third party can inflate the pool price to maximize the slippage rate and over-charge the receiver's share (griefing direction). The offchainMidPrice reference and the pool list are bound into the signed `extraInfo` hash, so the taker cannot alter the reference - but the live pool state the oracle reads at call time is freely movable.

This is a property of the example oracle provided in the codebase. Any production oracle chosen by the `routerSigner` that similarly relies on spot pool prices would expose the same manipulation surface; the router applies the oracle-returned rate verbatim with no TWAP requirement, staleness guard, or deviation cap of its own.


**Recommended Mitigation:** At the router boundary, enforce a maximum combined rate (`require(fee + slippage < UNIT_BASE)`) to bound worst-case manipulation, and document that accepted oracles must use TWAP-based pricing rather than single-block spot reads. The example PoolsBasedOracle should be updated to use a TWAP observation window (e.g., Uniswap V3's `observe` API) instead of `slot0` / `getReserves` to resist within-transaction manipulation.

**Bebop:** Acknowledged.
