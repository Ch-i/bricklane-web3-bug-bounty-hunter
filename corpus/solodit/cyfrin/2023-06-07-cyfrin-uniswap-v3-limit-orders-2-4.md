---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-07-cyfrin-uniswap-v3-limit-orders-2-4
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
title: Improvements to use of ternary operator
vuln_class: []
---

# Improvements to use of ternary operator

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-07-cyfrin-uniswap-v3-limit-orders.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md)_

---

There is currently one [instance](https://github.com/crispymangoes/uniswap-v3-limit-orders/blob/83f5db9cb90926c11ee6ce872dc165b7f600f3d8/src/LimitOrderRegistry.sol#L903) of ternary operator usage that can be simplified, with the boolean expression being evaluated directly:
```solidity
bool direction = targetTick > node.tickUpper ? true : false;
```
should be changed to:
```solidity
bool direction = targetTick > node.tickUpper;
```

Additionally, there is [another conditional statement](https://github.com/crispymangoes/uniswap-v3-limit-orders/blob/83f5db9cb90926c11ee6ce872dc165b7f600f3d8/src/LimitOrderRegistry.sol#L524-L525) where use of the ternary operator would be recommended:
```solidity
if (direction)
    assetIn = poolToData[pool].token0;
else assetIn = poolToData[pool].token1;
```
This conditional statement could be replaced with
```solidity
assetIn = direction ? poolToData[pool].token0 : poolToData[pool].token1;
```

**GFX Labs:** Fixed in commit [4cff05a](https://github.com/crispymangoes/uniswap-v3-limit-orders/commit/4cff05a1e6acd5f03bac527f0121eb3d3385fc2b).

**Cyfrin:** Acknowledged.
