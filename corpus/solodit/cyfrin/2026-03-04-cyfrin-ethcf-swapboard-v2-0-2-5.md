---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-ethcf-swapboard-v2-0-2-5
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-03-04T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-ethcf-swapboard-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-04-cyfrin-ethcf-swapboard-v2-0
title: Better storage packing in `struct Order` reduces gas cost of all `create, fill,
  cancel` operations
vuln_class: []
---

# Better storage packing in `struct Order` reduces gas cost of all `create, fill, cancel` operations

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-ethcf-swapboard-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-ethcf-swapboard-v2.0.md)_

---

**Description:** Since `Order::maker, active` are frequently written and read together,  in struct `Order` it is more efficient to pack them into the same slot:
```diff
    struct Order {
        address maker;
+       bool active;
        address tokenA;
        uint256 amountA;
        address tokenB;
        uint256 amountB;
-       bool active;
    }
```

Then in `Swapboard::fillOrder, cancelOrder, fillOrderWithEth, cancelOrderUnwrap, fillOrderUnwrap` use this format to read them both in one SLOAD:
```diff
-       address maker = order.maker;
+       (address maker, bool active) = (order.maker, order.active);
        if (maker == address(0)) revert OrderNotFound(orderId);
-       if (!order.active) revert OrderNotActive(orderId);
+       if (!active) revert OrderNotActive(orderId);
```

This also reduces the gas costs of creating orders since it removes one storage write with no required code changes to those functions.

**ETHCF:** Fixed in commit [82f9b49](https://github.com/ETHCF/swapboard/commit/82f9b4902ae53e439a5b34c08e651abdd9bd5ca8).

**Cyfrin:** Verified.

\clearpage
