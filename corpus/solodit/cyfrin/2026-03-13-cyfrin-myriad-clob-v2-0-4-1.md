---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-4-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-myriad-clob-v2-0
title: Cache repeated storage reads
vuln_class: []
---

# Cache repeated storage reads

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-myriad-clob-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md)_

---

**Description:** Across the matching functions these variables are accessed far more times than necessary:

| Variable | Function | Reads |
|---|---|---|
| `conditionalTokens` | `_settleMintMatch` | 6 |
| `conditionalTokens` | `_settleMergeMatch` | 5 |
| `conditionalTokens` | `matchCrossMarketOrders` | 2×N (distribution loop) |
| `conditionalTokens` | `_settleDirectMatch` | 2 |
| `manager` | `matchCrossMarketOrders` | 2×N+2 (validation loop + outside) |
| `feeModule` | `matchCrossMarketOrders` | N+2 (fee loop + accrue) |
| `feeModule` | `matchOrdersWithFees` | 3 |
| `negRiskAdapter` | `matchCrossMarketOrders` | 4 |

**Recommended Mitigation:** Cache each variable into a local at the top of every function where it is read more than once:

```solidity
// matchCrossMarketOrders — saves (2N+1) + (N+1) + (2N−1) + 3 SLOADs
IMyriadMarketManager _manager   = manager;
IFeeModule           _feeModule = IFeeModule(feeModule);
ConditionalTokens    _ct        = conditionalTokens;
address              _adapter   = negRiskAdapter;

bytes32 eventId = _manager.getEventId(orders[0].marketId);
// ... use _manager, _feeModule, _ct, _adapter throughout

// _settleMintMatch — saves 5 SLOADs
ConditionalTokens _ct = conditionalTokens;
collateral.forceApprove(address(_ct), fillAmount);
_ct.splitPosition(maker.marketId, fillAmount);
_ct.safeTransferFrom(address(this), outcome0Order.trader, _ct.getTokenId(maker.marketId, 0), fillAmount, "");
_ct.safeTransferFrom(address(this), outcome1Order.trader, _ct.getTokenId(maker.marketId, 1), fillAmount, "");

// _settleMergeMatch — saves 4 SLOADs
ConditionalTokens _ct = conditionalTokens;
uint256 outcome0TokenId = _ct.getTokenId(maker.marketId, 0);
uint256 outcome1TokenId = _ct.getTokenId(maker.marketId, 1);
_ct.safeTransferFrom(...);
_ct.safeTransferFrom(...);
_ct.mergePositions(...);
```

**Myriad:** Fixed in commit [`5870aa4`](https://github.com/Polkamarkets/polkamarkets-js/commit/5870aa42a6177978d566785a474715195abac763)

**Cyfrin:** Verified.
