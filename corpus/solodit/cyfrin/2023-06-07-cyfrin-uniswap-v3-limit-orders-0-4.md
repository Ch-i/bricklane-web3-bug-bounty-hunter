---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-07-cyfrin-uniswap-v3-limit-orders-0-4
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-06-07T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md
tags:
- firm:cyfrin
- report:2023-06-07-cyfrin-uniswap-v3-limit-orders
title: Malicious validators can prevent orders from being created or cancelled
vuln_class: []
---

# Malicious validators can prevent orders from being created or cancelled

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-07-cyfrin-uniswap-v3-limit-orders.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md)_

---

**Description:** Use of `block.timestamp` as the deadline for [`MintParams`](https://github.com/crispymangoes/uniswap-v3-limit-orders/blob/83f5db9cb90926c11ee6ce872dc165b7f600f3d8/src/LimitOrderRegistry.sol#L1056), [`IncreaseLiquidityParams`](https://github.com/crispymangoes/uniswap-v3-limit-orders/blob/83f5db9cb90926c11ee6ce872dc165b7f600f3d8/src/LimitOrderRegistry.sol#L1099) and [`DecreaseLiquidityParams`](https://github.com/crispymangoes/uniswap-v3-limit-orders/blob/83f5db9cb90926c11ee6ce872dc165b7f600f3d8/src/LimitOrderRegistry.sol#L1207) means that a given transaction interfacing with Uniswap v3 will be valid whenever the validator decides to include it. This could result in orders prevented from being created or cancelled if a malicious validator holds these transactions until after the tick price for the given pool has moved such that the deadline is valid but order status is no longer valid.

**Impact:** Whenever the validator decides to include the transaction in a block, it will be valid at that time, since `block.timestamp` will be the current timestamp. This could result in forcing an order to be fulfilled when it was the sender's intention to have it cancelled, by holding until price exceeds the target tick as ITM orders can't be cancelled, or never creating the order at all, by similar reasoning as it is not allowed to create orders that are immediately ITM.

**Recommended Mitigation:** Add deadline arguments to all functions that interact with Uniswap v3 via the `NonFungiblePositionManager`, and pass it along to the associated calls.

**GFX Labs:** Fixed by adding deadline arguments to all Position Manager calls in commit [f05cdfc](https://github.com/crispymangoes/uniswap-v3-limit-orders/commit/f05cdfce4762d980235fe4d726800d2b0a112d2d).

**Cyfrin:** Acknowledged.
