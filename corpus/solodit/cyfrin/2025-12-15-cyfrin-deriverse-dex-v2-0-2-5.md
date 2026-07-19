---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-2-5
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: 'Griefing Attack: Malicious Takers Can Force Order Cancellation by Partial
  Filling Below Minimum Quantity'
vuln_class: []
---

# Griefing Attack: Malicious Takers Can Force Order Cancellation by Partial Filling Below Minimum Quantity

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** A malicious taker can exploit the automatic order cancellation mechanism to force makers' orders to be cancelled by intentionally partially filling orders such that the remaining quantity falls below the `min_qty` threshold.

When this occurs, the system automatically cancels the order and refunds the remaining locked funds to the maker. However, since the refunded amount is below `min_qty`, the maker cannot place a new order with these funds, effectively creating a griefing attack that disrupts normal trading operations.

The vulnerability exists in the `fill` function of the spot trading engine . When an order is partially filled (last = true), the system will automatically cancels the order via `erase_client_order(order, node, true, side)`.


```rust
// src/program/spot/engine.rs:1265-1279
if last {
    order.decr_qty(traded_qty).map_err(|err| drv_err!(err))?;
    order.decr_sum(traded_crncy).map_err(|err| drv_err!(err))?;
    order.set_time(self.time);
    if order.qty() < min_qty {  // ⚠️ check
        let node = self.get_node_ptr(order.link(), fill_static_args.side);
        self.erase_client_order(order, node, true, fill_static_args.side)?;
        // ... order is cancelled and funds refunded
    }
}
```

Attack Scenario:
- Maker places an order with quantity 100 tokens, where `min_qty = 2`
- Malicious taker intentionally matches 99 tokens, leaving `1` token remaining
- Since `1 < min_qty (2)`, the system automatically cancels the order
- The remaining `1` token is refunded to the maker via `erase_client_order`
- The maker cannot place a new order with the refunded 1 token because it's below `min_qty`


**Impact:**
- Griefing Attack: Attackers can systematically target orders and force their cancellation by leaving dust amounts below `min_qty`.
- **Refunded amounts below `min_qty` cannot be used to place new orders, effectively locking small amounts of funds**. I think this is not restricted to the order cancellation process, but is throughout the whole repo as it's uncertain how to deal with the dust amount

**Recommended Mitigation:** For this, I have two possible suggestions:
- Prevent Automatic Cancellation on Partial Fill
- Add a way for the user to sell dust amount directly on AMM

**Deriverse:** Fixed in commit [134db8b](https://github.com/deriverse/protocol-v1/commit/134db8b1dac9e48641dac1a6b95bcf34637f695f).

**Cyfrin:** Verified. User's can use market order to deal with tiny amounts
