---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-07-cyfrin-uniswap-v3-limit-orders-2-5
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-06-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md
tags:
- firm:cyfrin
- report:2023-06-07-cyfrin-uniswap-v3-limit-orders
title: Move shared logic to internal functions called within a modifier
vuln_class: []
---

# Move shared logic to internal functions called within a modifier

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-07-cyfrin-uniswap-v3-limit-orders.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md)_

---

```solidity
...
if (direction) data.token0.safeApprove(address(POSITION_MANAGER), amount0);
else data.token1.safeApprove(address(POSITION_MANAGER), amount1);

    // 0.9999e18 accounts for rounding errors in the Uniswap V3 protocol.
    uint128 amount0Min = amount0 == 0 ? 0 : (amount0 * 0.9999e18) / 1e18;
    uint128 amount1Min = amount1 == 0 ? 0 : (amount1 * 0.9999e18) / 1e18;
...
// If position manager still has allowance, zero it out.
    if (direction && data.token0.allowance(address(this), address(POSITION_MANAGER)) > 0)
        data.token0.safeApprove(address(POSITION_MANAGER), 0);
    if (!direction && data.token1.allowance(address(this), address(POSITION_MANAGER)) > 0)
        data.token1.safeApprove(address(POSITION_MANAGER), 0);
```

The above logic in [`_mintPosition`](https://github.com/crispymangoes/uniswap-v3-limit-orders/tree/83f5db9cb90926c11ee6ce872dc165b7f600f3d8/src/LimitOrderRegistry.sol#L1029) and [`_addToPosition`](https://github.com/crispymangoes/uniswap-v3-limit-orders/tree/83f5db9cb90926c11ee6ce872dc165b7f600f3d8/src/LimitOrderRegistry.sol#L1078) is shared and repeated across both functions. Consider moving this code to internal functions which are called within a modifier like so:
```solidity
modifier approvePositionManager() {
    _approveBefore();
    _;
    _approveAfter();
}
```

**GFX Labs:** Acknowledged. This is a valid concern, but in an effort to reduce contract size and minimize code changes, this will not be implemented.

**Cyfrin:** Acknowledged.
