---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-2-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: '`MarketOrder` minimum lifetime can be easily bypassed'
vuln_class: []
---

# `MarketOrder` minimum lifetime can be easily bypassed

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** `OrderBranch::createMarketOrder` validates the `marketOrderMinLifetime` of the previous pending market order before canceling it and opening a new market order:
```solidity
File: OrderBranch.sol
                // @audit `createMarketOrder` enforces minimum market order lifetime
210:         marketOrder.checkPendingOrder();
211:         marketOrder.update({ marketId: params.marketId, sizeDelta: params.sizeDelta });

File: MarketOrder.sol
55:     function checkPendingOrder(Data storage self) internal view {
56:         GlobalConfiguration.Data storage globalConfiguration = GlobalConfiguration.load();
57:         uint128 marketOrderMinLifetime = globalConfiguration.marketOrderMinLifetime;
58:
59:         if (self.timestamp != 0 && block.timestamp - self.timestamp <= marketOrderMinLifetime) {
60:             revert Errors.MarketOrderStillPending(self.timestamp);
61:         }
62:     }
```

But in `OrderBranch::cancelMarketOrder` users can cancel the pending market order without any validation:
```solidity
File: OrderBranch.sol
219:     function cancelMarketOrder(uint128 tradingAccountId) external {
220:         MarketOrder.Data storage marketOrder = MarketOrder.loadExisting(tradingAccountId);
221:         // @audit doesn't enforce minimum market order lifetime
222:         marketOrder.clear();
223:
224:         emit LogCancelMarketOrder(msg.sender, tradingAccountId);
225:     }
```

Hence users can cancel their previous market order and open a new order anytime by calling `cancelMarketOrder` first.

**Impact:** The `marketOrderMinLifetime` requirement can be bypassed by calling `cancelMarketOrder` first.

**Recommended Mitigation:** `cancelMarketOrder` should check the `marketOrderMinLifetime` requirement.

```diff
    function cancelMarketOrder(uint128 tradingAccountId) external {
        MarketOrder.Data storage marketOrder = MarketOrder.loadExisting(tradingAccountId);

+       marketOrder.checkPendingOrder();

        marketOrder.clear();

        emit LogCancelMarketOrder(msg.sender, tradingAccountId);
    }
```

**Zaros:** Fixed in commit [41eae0e](https://github.com/zaros-labs/zaros-core/commit/41eae0ea8f04ffd877484bd7b430d7d85893f421#diff-1329f2388c20edbc7edf3e949fdb903992444d015a681e83fc62a6a02ef51b76R236).

**Cyfrin:** Verified.
