---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-3-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-03-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-12-cyfrin-paladin-valkyrie-v2-0
title: Value mistakenly sent to `PoolCreator` can be permanently locked
vuln_class: []
---

# Value mistakenly sent to `PoolCreator` can be permanently locked

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-12-cyfrin-paladin-valkyrie-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md)_

---

**Description:** The `PoolCreator` is a simple contract designed to create Uniswap v4 pools. The `createPool()` function is currently marked `payable`, however this is not necessary as no value is passed to `PoolManager`:

```solidity
function createPool(PoolKey calldata key, uint160 sqrtPriceX96) external payable returns (PoolId poolId, int24 tick) {
    poolId = key.toId();
    tick = poolManager.initialize(key, sqrtPriceX96);
}
```

Due to the absence of any refunds or functions to sweep native tokens, any value mistakenly sent with calls to this function will be permanently locked.

**Recommended Mitigation:** Remove the `payable` keyword to prevent value from being sent to the contract.

**Paladin:** Fixed by commit [`b271724`](https://github.com/PaladinFinance/Valkyrie/pull/5/commits/b271724295605d571ea9f44231547d195ce600a0).

**Cyfrin:** Verified. The function is no longer payable.
