---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-3-9
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Forced Oldest-Order Eviction Enables Griefing
vuln_class: []
---

# Forced Oldest-Order Eviction Enables Griefing

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** **This issue is theoretically possible, but the exploitation conditions are quite strict, so I marked it as INFO.**

When a side of the spot order book exceeds `MAX_ORDERS`, the matching engine unconditionally cancels the globally oldest order on that side. Because `MAX_ORDERS` is shared by all traders, a malicious participant can deliberately fill the book with tiny orders, repeatedly trigger the eviction path, and force legitimate users’ resting/large orders to be cancelled.

`add_order` grows the order book and, after inserting the new order, checks whether the per-side total exceeds MAX_ORDERS. If so, it removes the oldest order, without regard to ownership and the order size.

```rust
        } else if self.orders_count(side) > MAX_ORDERS {
            let oldest_node = self.find_oldest_order_node(side);
            let oldest_order = self.get_order_ptr(oldest_node.link(), side);
            self.erase_client_order(oldest_order, oldest_node, true, side)?;
            ...
```

`MAX_ORDERS` is a global limit (≈14,334) shared by all users of the instrument.

```rust
pub mod spot {
    pub const MAX_LINES: usize = 2048;
    pub const MAX_ORDERS: u32 = (4 * 64 * 64 - MAX_LINES) as u32 - 2;
```

An attacker can create many minimum-quantity orders (funds are returned when their orders are eventually evicted), drive `orders_count(side)` above `MAX_ORDERS`, and delete the oldest resting order. The cost is limited to transaction fees plus temporarily locking collateral for the attacker’s own active orders.

**Impact:** Other traders’ limit orders can be griefed off the book at will regardless of the order size, degrading market integrity, denying service, and allowing the attacker to control displayed liquidity.

**Recommended Mitigation:** Prevent a single participant from consuming the entire order quota. Options include:
- Enforce a per-client cap on orders numbers.

**Deriverse:** Fixed in commit [ed3b97ec](https://github.com/deriverse/protocol-v1/commit/ed3b97ec0e4157a55df4c5a8e56dda6786ec2195).

**Cyfrin:** Verified.
