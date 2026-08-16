---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-07-cyfrin-uniswap-v3-limit-orders-3-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-06-07T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md
tags:
- firm:cyfrin
- report:2023-06-07-cyfrin-uniswap-v3-limit-orders
title: Perform post-increment in a single line
vuln_class: []
---

# Perform post-increment in a single line

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-07-cyfrin-uniswap-v3-limit-orders.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md)_

---

The post-increment of `batchCount` variable in `LimitOrderRegistry::_setupOrder` can be performed in a single line when it is assigned to `order.batchId`:
```diff
  function _setupOrder(bool direction, uint256 position) internal {
     BatchOrder storage order = orderBook[position];
-    order.batchId = batchCount;
+    order.batchId = batchCount++;
     order.direction = direction;
-    batchCount++;
  }
```

**GFX Labs:** Fixed in commit [4cff05a](https://github.com/crispymangoes/uniswap-v3-limit-orders/commit/4cff05a1e6acd5f03bac527f0121eb3d3385fc2b).

**Cyfrin:** Acknowledged.

\clearpage
