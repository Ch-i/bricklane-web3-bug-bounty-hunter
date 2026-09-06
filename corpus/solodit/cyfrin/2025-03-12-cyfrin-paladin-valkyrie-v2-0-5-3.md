---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-5-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-03-12T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-12-cyfrin-paladin-valkyrie-v2-0
title: Cache `amount` variable should be used within loop to save gas
vuln_class: []
---

# Cache `amount` variable should be used within loop to save gas

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-12-cyfrin-paladin-valkyrie-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md)_

---

**Description:** The `amount` variable is assigned within `IncentiveManager::notifyRemoveLiquidty` to avoid repeated typecasting; however, it is not currently used within the loop.

**Recommended Mitigation:**
```diff
    function notifyRemoveLiquidty(PoolId id, address lpToken, address account, int256 liquidityDelta)
        external
        onlyAllowedHooks
    {
        ...
        uint256 amount = toUint256(-liquidityDelta);
        ...
        if (length > 0) {
            for (uint256 i; i < length;) {
                // Notify the Incentive Logic of the balance change
                IIncentiveLogic(incentiveSystems[_systems[i]].system).notifyBalanceChange(
--                  _id, account, toUint256(-liquidityDelta), false
++                  _id, account, amount, false
                );
                unchecked {
                    ++i;
                }
            }
        }

        poolTotalLiquidity[_id] -= amount;
        poolUserLiquidity[_id][account] -= amount;

        emit LiquidityChange(_id, account, address(0), amount);
    }
```

**Paladin:** Fixed by commit [`075c846`](https://github.com/PaladinFinance/Valkyrie/pull/5/commits/075c84618e1f94b17ad10afeb6d77ea101195871).

**Cyfrin:** Verified. The cast amount in now cached.
