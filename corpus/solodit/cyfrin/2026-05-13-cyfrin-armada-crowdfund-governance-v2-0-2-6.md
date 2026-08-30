---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-2-6
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: '`ArmadaTreasuryGov::removeStewardBudgetToken` can revert with OOG error'
vuln_class: []
---

# `ArmadaTreasuryGov::removeStewardBudgetToken` can revert with OOG error

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** As you can see, it removes `_stewardSpendHistory`:
```solidity
    function removeStewardBudgetToken(address token) external onlyOwner {
        require(stewardBudgets[token].authorized, "ArmadaTreasuryGov: token not authorized");

        delete stewardBudgets[token];
@>      delete _stewardSpendHistory[token];
    }
```

Actually `_stewardSpendHistory` is append-only array, it contains every spending:
```solidity
    function stewardSpend(address token, address recipient, uint256 amount) external onlyOwner {
        ...

        // Record this spend for rolling window tracking.
        // NOTE: Same append-only pattern as _outflowHistory — see design note on _checkAndRecordOutflow.
@>      _stewardSpendHistory[token].push(OutflowRecord({
            amount: amount,
            timestamp: block.timestamp
        }));

        _checkAndRecordOutflow(token, amount);
        IERC20(token).safeTransfer(recipient, amount);

        uint256 remaining = budget.limit - (recentSpend + amount);
        emit StewardSpent(token, recipient, amount, remaining);
    }
```

It won't be possible to call `removeStewardBudgetToken` when array is big enough to delete.

**Impact:** Function `removeStewardBudgetToken` can't be called, it means budget config can't be removed completely. Still there is workaround to use `updateStewardBudgetToken` setting limit to 1 wei.

**Recommended Mitigation:** Consider not deleting history:
```diff
    function removeStewardBudgetToken(address token) external onlyOwner {
        require(stewardBudgets[token].authorized, "ArmadaTreasuryGov: token not authorized");

        delete stewardBudgets[token];
-       delete _stewardSpendHistory[token];
    }
```

**Armada:** Fixed in commit [447e6cb](https://github.com/ship-armada/armada-poc/commit/447e6cbb8833f92dffa517ea24423e9945f3ee4d).

**Cyfrin:** Verified.
