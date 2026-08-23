---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-ethcf-swapboard-v2-0-0-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-03-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-ethcf-swapboard-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-04-cyfrin-ethcf-swapboard-v2-0
title: No order expiration — stale orders become free options for takers
vuln_class: []
---

# No order expiration — stale orders become free options for takers

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-ethcf-swapboard-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-ethcf-swapboard-v2.0.md)_

---

**Description:** [`Swapboard::createOrder`](https://github.com/ETHCF/swapboard/blob/c43406f/contracts/src/Swapboard.sol#L55) and [`Swapboard::createOrderWithEth`](https://github.com/ETHCF/swapboard/blob/c43406f/contracts/src/Swapboard.sol#L140) create orders with no expiration timestamp. Once created, an order remains fillable indefinitely until explicitly cancelled. This creates a free option problem.

- The `Order` struct has no `deadline` field
- [`Swapboard::fillOrder`](https://github.com/ETHCF/swapboard/blob/c43406f/contracts/src/Swapboard.sol#L102), [`Swapboard::fillOrderWithEth`](https://github.com/ETHCF/swapboard/blob/c43406f/contracts/src/Swapboard.sol#L170), and [`Swapboard::fillOrderUnwrap`](https://github.com/ETHCF/swapboard/blob/c43406f/contracts/src/Swapboard.sol#L212) enforce no time-based check
- The subgraph tracks `createdAt` but the contract enforces no deadline
- The frontend shows when an order was created but cannot warn about stale orders

Scenario:
1. Maker creates an order selling 1 WETH for 2,000 USDC when ETH is at $2,000
2. ETH price rises to $4,000 over the next month
3. The order is still active — any taker can buy 1 WETH for 2,000 USDC (50% below market)
4. The maker must actively monitor and cancel, but if they lose wallet access, go offline, or miss the price movement, the order is a sitting target

From the taker's perspective, every open order is a **free call option**: they can wait and only execute when the market moves in their favor, at no cost. In traditional OTC and DeFi limit-order systems (e.g., 0x, CoW Protocol, 1inch Limit Orders), orders include a `deadline` or `expiry` parameter to mitigate this.

**Impact:** Makers suffer economic loss from stale orders being filled at outdated prices. The risk scales with market volatility and the duration orders remain open.

**Proof of Concept:**
- Any active order can be filled at any time regardless of how old it is
- No on-chain mechanism to auto-expire orders
- Maker's only option is to manually cancel, which requires wallet access and gas

**Recommended Mitigation:** Add an optional `deadline` parameter to `createOrder` and `createOrderWithEth`:

```solidity
struct Order {
    address maker;
    address tokenA;
    uint256 amountA;
    address tokenB;
    uint256 amountB;
    uint256 deadline;   // 0 = no expiry
    bool active;
}
```

Then in [`Swapboard::fillOrder`] (and all fill variants):

```solidity
if (order.deadline != 0 && block.timestamp > order.deadline) revert OrderExpired(orderId);
```

This gives makers opt-in time-bounding while preserving backwards compatibility (deadline=0 means no expiry).

**Ethcf:**
Acknowledged; this is a design choice.
