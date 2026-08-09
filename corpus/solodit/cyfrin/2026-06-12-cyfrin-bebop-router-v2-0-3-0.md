---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-12-cyfrin-bebop-router-v2-0-3-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-06-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-12-cyfrin-bebop-router-v2-0
title: '`BebopPmmHelper::_decodeSinglePmm, _decodeAggregatePmm` discard the PMM `receiver`
  and `taker_address` and never assert `receiver == address(this)`'
vuln_class: []
---

# `BebopPmmHelper::_decodeSinglePmm, _decodeAggregatePmm` discard the PMM `receiver` and `taker_address` and never assert `receiver == address(this)`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-12-cyfrin-bebop-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md)_

---

**Description:** Both `_decodeSinglePmm` and `_decodeAggregatePmm` decode - and then immediately discard - the PMM order's `receiver` and `taker_address` fields (marked with `, // receiver` and `, // taker_address` comments at `contracts/base/BebopPmmHelper.sol:71` and `contracts/base/BebopPmmHelper.sol:131`). The router's entire fee-distribution and receiver-payout logic assumes the PMM settlement sends its output to the router: `_distributeFees` reads `IERC20(order.pmmToToken).balanceOf(address(this))` (`contracts/BebopRouter.sol:450`) and the receiver payout reads `IERC20(order.toToken).balanceOf(address(this))` (`contracts/BebopRouter.sol:305`). This invariant - that PMM output lands in the router - is currently enforced only by the out-of-scope `BebopSettlement` contract, which binds `receiver` into the maker signature and enforces `msg.sender == order.taker_address`. The router itself has no local `require(pmmReceiver == address(this))` guard. If a maker ever signs a PMM order naming a `receiver` other than the router (through misconfiguration, collusion, or a future settlement upgrade), the maker output is silently routed elsewhere; the router then distributes fees and pays `order.receiver` from whatever residual balance it holds, corrupting accounting. The `taker_address` mismatch results in a clean revert from the settlement rather than silent misaccounting, but is equally unvalidated locally.

**Recommended Mitigation:** In both `_decodeSinglePmm` and `_decodeAggregatePmm`, decode the PMM `receiver` field and add `require(receiver == address(this))`. Similarly decode `taker_address` and add `require(taker_address == address(this))`. This makes the load-bearing custody invariant locally enforced rather than delegated to an out-of-scope contract.

**Bebop:** Fixed in commit [9db95bc](https://github.com/bebop-dex/bebop-rfqa/commit/9db95bc2b423d9317c149e90a70ae51565e26367).

**Cyfrin:**
Verified.
