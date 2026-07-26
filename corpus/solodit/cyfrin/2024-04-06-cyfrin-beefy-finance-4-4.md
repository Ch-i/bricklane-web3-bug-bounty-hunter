---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-4-4
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-04-06T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md
tags:
- firm:cyfrin
- report:2024-04-06-cyfrin-beefy-finance
title: Don't call `_tickDistance` twice in `StrategyPassiveManagerUniswap::_setMainTick`
vuln_class: []
---

# Don't call `_tickDistance` twice in `StrategyPassiveManagerUniswap::_setMainTick`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-06-cyfrin-beefy-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md)_

---

**Description:** `StrategyPassiveManagerUniswap::_setMainTick` calls `_tickDistance` twice even though there is no need since the exact same value will be returned; replace the second call with the `distance` variable which caches the result of the first call like so:
```solidity
    function _setMainTick() private {
        int24 tick = currentTick();
        int24 distance = _tickDistance();
        int24 width = positionWidth * distance;
        (positionMain.tickLower, positionMain.tickUpper) = TickUtils.baseTicks(
            tick,
            width,
            // @audit use cached result from first call
            distance                 // _tickDistance()
        );
    }
```

**Beefy:**
Fixed in commit [e7723da](https://github.com/beefyfinance/experiments/commit/e7723daf27d39ae013507191aa67e111f3af05e4).

**Cyfrin:** Verified.
