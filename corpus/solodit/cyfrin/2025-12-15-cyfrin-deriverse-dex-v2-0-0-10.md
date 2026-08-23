---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-0-10
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Attacker can cause losses to others by partially closing their position at
  an unfavorable price
vuln_class: []
---

# Attacker can cause losses to others by partially closing their position at an unfavorable price

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** In our new perp order flow, we verify whether the leverage is valid using `check_client_leverage_from`. However, this check is only executed if any of the following conditions are true:
```rust
current_perps.signum() != old_perps.signum()
current_leverage > old_leverage
old_leverage == i64::MAX as f64
```
A user can exploit this behavior to sell their position at an artificially unfavorable price(a very low price when long, or a very high price when short). This can result in socialized losses being imposed on other users.

Example: A user is able to create a new order only a few lamports away from their liquidation point. For example, when the user is long, they may create an ask order extremely close to liquidation and potentially exploit the mechanism.

Specifically, if there are no bid orders—or only negligible ones—the user can place an ask order at a very low price. Immediately afterward, using another address, they can purchase their own ask order by creating a bid order at the same low price. This causes loss, which are then socialized to other participants.

This exploit relies on the condition that no meaningful bid liquidity is present.

Scenerio: A user has a 1 BTC long position with 10× leverage. Their funds are –90k, and the edge price is 90k, with a zero-liquidation threshold.

Now, suppose there are no bid orders, and both the mark price and index price is $90,100.
The user then creates an ASK order for 0.5 BTC at $80,000.
In the portfolio(perp), the position becomes 0.5 BTC.
In the order, the perp becomes 0.5 BTC.

At this point:
The old leverage is 90k / 100 = 900, and the old total perp is 1 BTC.
The new leverage is also unchanged (still 90k / 100 = 900).
old_leverage is not i64::MAX as f64.
And importantly, both the current and old perp values have the same signum.

`check_client_leverage_from` will not run because the sign remains the same, and the current leverage is equal to the previous leverage — which itself was not at the maximum.

After this, a user can create a bid order from a different address and purchase the ask order at 80k, enabling them to exploit the mechanism.

Later, when the user’s original position of 0.5 BTC is liquidated, it will generate a loss that becomes socialized across other users.

**Impact:** The impact is high, as it results in losses for other users.


**Recommended Mitigation:**
1. Add a check to ensure that if `margin_call` is false and loss is greater than zero, the transaction should revert.
```rust
     if loss > 0 && !args.margin_call {
           return Err;
     }
```
2. When a user is in a long position and creates an ask order, the order price should be greater than the critical price. Conversely, when the user is in a short position, the bid order price should be lower than the critical price.

**Deriverse:** Fixed in commit [26d87c](https://github.com/deriverse/protocol-v1/commit/26d87c791fd7edf5971dfbcd41b702ee1a1218b8), [319890](https://github.com/deriverse/protocol-v1/commit/3198908f063537fc8b9ff6c9e1b6bcd8933e0847).

**Cyfrin:** Verified.
