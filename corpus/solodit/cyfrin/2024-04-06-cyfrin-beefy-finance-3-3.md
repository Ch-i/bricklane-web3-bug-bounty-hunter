---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-3-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-04-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md
tags:
- firm:cyfrin
- report:2024-04-06-cyfrin-beefy-finance
title: Use existing `price` function in `StrategyPassiveManagerUniswap::_setAltTick`
vuln_class: []
---

# Use existing `price` function in `StrategyPassiveManagerUniswap::_setAltTick`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-06-cyfrin-beefy-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md)_

---

**Description:** `StrategyPassiveManagerUniswap` has a `price` function that [converts](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/uniswap/StrategyPassiveManagerUniswap.sol#L534-L537) `sqrtPriceX96` returned by uniswap `pool.slot0`.

Refactor `_setAltTick` [L601-604](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/uniswap/StrategyPassiveManagerUniswap.sol#L601-L604) to use the existing `price` function to reduce code duplication and the possibility for errors creeping in when implementing the same functionality in multiple places:

```solidity
if (bal0 > 0) {
    amount0 = bal0 * price() / PRECISION;
}
```

This also allows for the removal of the `price1` variable declaration inside `_setAltTick`.

**Beefy:**
Fixed in commit [b5b609e](https://github.com/beefyfinance/experiments/commit/b5b609ec38938b15dc20a5ac187111019b82ebc5).

**Cyfrin:** Verified.
