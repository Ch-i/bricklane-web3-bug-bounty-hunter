---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-4-5
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-04-06T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md
tags:
- firm:cyfrin
- report:2024-04-06-cyfrin-beefy-finance
title: In `StrategyPassiveManagerUniswap` public functions should cache common inputs
  then pass them as parameters to private functions
vuln_class: []
---

# In `StrategyPassiveManagerUniswap` public functions should cache common inputs then pass them as parameters to private functions

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-06-cyfrin-beefy-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md)_

---

**Description:** `StrategyPassiveManagerUniswap` has many private functions which read the same values from storage multiple times without changing them. Since reading from storage is gas expensive, these values could be read from storage once then passed into private functions as inputs.

Example 1 - `StrategyPassiveManagerUniswap::_setMainTick` and `_setAltTick` use many of the same inputs; instead of reading them from storage multiple times, read them once inside `_setTicks` then pass them in as input parameters to `_setMainTick, _setAltTick`:

```solidity
function _setTicks() private {
    // @audit reading inputs only once
    int24 currTick = currentTick();
    int24 distance = _tickDistance();
    int24 width    = positionWidth * distance;

    // @audit passing inputs as parameters to avoid
    // multiple identical storage reads
    _setMainTick(currTick, distance, width);
    _setAltTick(currTick, distance, width);
}
```

Example 2 - `beforeAction` calls `_claimEarnings` and `_removeLiquidity`. Both of these private functions read `pool`, `positionMain` and `positionAlt` from storage but don't modify these storage locations. Hence `beforeAction` could read these values from storage once then pass them in as inputs to `_claimEarnings` and `_removeLiquidity` in order to save many useless but expensive storage reads.

**Beefy:**
Fixed in commit [ce5f798](https://github.com/beefyfinance/experiments/commit/ce5f7986372cd2e32e58b1a03e0693d42b4b1ce0).

**Cyfrin:** Verified.
