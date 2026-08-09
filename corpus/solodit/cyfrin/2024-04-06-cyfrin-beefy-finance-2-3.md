---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-2-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-04-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md
tags:
- firm:cyfrin
- report:2024-04-06-cyfrin-beefy-finance
title: '`_onlyCalmPeriods` does not consider MIN/MAX ticks, which can DOS deposit,
  withdraw and harvest in edge cases'
vuln_class: []
---

# `_onlyCalmPeriods` does not consider MIN/MAX ticks, which can DOS deposit, withdraw and harvest in edge cases

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-06-cyfrin-beefy-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md)_

---

**Description:** In Uniswap V3 liquidity providers can only provide liquidity between price ranges `[1.0001^{MIN_ TICK};1.0001^{MAX_TICK})`. Therefore these are the min and max prices.

```solidity
    function _onlyCalmPeriods() private view {
        int24 tick = currentTick();
        int56 twapTick = twap();

        if(
            twapTick - maxTickDeviationNegative > tick  ||
            twapTick + maxTickDeviationPositive < tick) revert NotCalm();
    }
```

If `twapTick - maxTickDeviationNegative < MIN_TICK`, this function would revert even if `tick` has been the same for years. This can DOS deposits, withdrawals and harvests when they should be allowed for as long as the state holds.

**Recommended Mitigation:** Consider changing the current implementation to:

```diff
+   const int56 MIN_TICK = -887272;
+   const int56 MAX_TICK = 887272;
    function _onlyCalmPeriods() private view {
        int24 tick = currentTick();
        int56 twapTick = twap();

+       int56 minCalmTick = max(twapTick - maxTickDeviationNegative, MIN_TICK);
+       int56 maxCalmTick = min(twapTick - maxTickDeviationPositive, MAX_TICK);

        if(
-           twapTick - maxTickDeviationNegative > tick  ||
-           twapTick + maxTickDeviationPositive < tick) revert NotCalm();
+           minCalmTick > tick  ||
+           maxCalmTick < tick) revert NotCalm();
    }
```

**Beefy:**
Fixed in commit [b5432d2](https://github.com/beefyfinance/experiments/commit/b5432d2c73f071f08ab34efcc570605f64808d38).

**Cyfrin:** Verified.
