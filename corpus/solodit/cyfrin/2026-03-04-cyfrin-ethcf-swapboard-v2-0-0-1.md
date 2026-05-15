---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-ethcf-swapboard-v2-0-0-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-03-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-ethcf-swapboard-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-04-cyfrin-ethcf-swapboard-v2-0
title: No fill deadline parameter exposes takers to stale transaction execution
vuln_class: []
---

# No fill deadline parameter exposes takers to stale transaction execution

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-ethcf-swapboard-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-ethcf-swapboard-v2.0.md)_

---

**Description:** [`Swapboard::fillOrder`](https://github.com/ETHCF/swapboard/blob/c43406f/contracts/src/Swapboard.sol#L102), [`Swapboard::fillOrderWithEth`](https://github.com/ETHCF/swapboard/blob/c43406f/contracts/src/Swapboard.sol#L170), and [`Swapboard::fillOrderUnwrap`](https://github.com/ETHCF/swapboard/blob/c43406f/contracts/src/Swapboard.sol#L212) accept no deadline parameter. In a congested network, a taker's fill transaction could sit in the mempool for extended periods and execute when conditions have changed (e.g., the token price has moved significantly).

This is distinct from M-01 (maker-side order expiry) — this is **taker-side** protection. Even if the order itself has no expiry, the taker should be able to specify "execute my fill only if it happens within N seconds."

This is standard practice in DeFi swap protocols. For example, [Uniswap V2 Router02](https://docs.uniswap.org/contracts/v2/reference/smart-contracts/router-02) includes a `deadline` parameter on all swap functions:

```solidity
// Uniswap V2 Router02
function swapExactTokensForTokens(
    uint amountIn,
    uint amountOutMin,
    address[] calldata path,
    address to,
    uint deadline    // UNIX timestamp
) external returns (uint[] memory amounts);
```

The `deadline` prevents miners/block builders from holding a transaction and executing it later at a more favorable price. Uniswap V2, V3, and V4 all include it.

**Impact:** Takers may have their fill transactions execute at an outdated and unfavorable rate after sitting in the mempool during network congestion.

**Proof of Concept:**
- Taker submits `fillOrder(orderId)` during congestion
- Transaction sits in mempool for hours
- Token price moves significantly
- Transaction finally executes at the now-unfavorable rate
- Taker had no way to set a deadline to prevent this

**Recommended Mitigation:** Add a `deadline` parameter to fill functions:

```solidity
function fillOrder(uint256 orderId, uint256 deadline) external nonReentrant {
    if (deadline != 0 && block.timestamp > deadline) revert DeadlineExpired();
    // ...
}
```

**Ethcf:**

Fixed in commit [572f3c5](https://github.com/ETHCF/swapboard/commit/572f3c5d724b78fc3a2f304557a23c018f9fc31d). Added `uint256 deadline` parameter to `fillOrder, fillOrderWithEth, and fillOrderUnwrap`. When `deadline == 0`, no expiry is enforced. When `deadline != 0 && block.timestamp > deadline`, the call reverts with `DeadlineExpired`.

**Cyfrin:** Verified. Deadline check is correct — early revert before storage reads, `deadline == 0` allows takers to opt out of deadline enforcement.

\clearpage
