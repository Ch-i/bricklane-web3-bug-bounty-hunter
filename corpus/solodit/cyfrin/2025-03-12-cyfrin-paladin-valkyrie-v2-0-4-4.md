---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-4-4
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-03-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-12-cyfrin-paladin-valkyrie-v2-0
title: Unnecessary `BoostedIncentiveLogic` functions can be removed
vuln_class: []
---

# Unnecessary `BoostedIncentiveLogic` functions can be removed

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-12-cyfrin-paladin-valkyrie-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md)_

---

**Description:** * `BoostedIncentiveLogic::_updateRewardState` overrides the `BaseIncentiveLogic` implementation; however, both functions have exactly the same implementation, so there is no need to override it.

* `BoostedIncentiveLogic::updateUserBoostedBalance` is completely unnecessary because `updateUserState` performs the exact same state changes:

```solidity
function updateUserState(IncentivizedPoolId id, address account) external override nonReentrant {
    _updateAllUserState(id, account);
    _updateUserBoostedBalance(id, account);
}

function updateUserBoostedBalance(IncentivizedPoolId id, address account) external nonReentrant {
    _updateAllUserState(id, account);
    _updateUserBoostedBalance(id, account);
}
```

**Recommended Mitigation:**
1. Remove the overridden `_updateRewardState()` implementation.
2. Remove the `updateUserBoostedBalance()` function and use the overridden `updateUserState()` in its place.

**Paladin:** Fixed by commit [`df40bd5`](https://github.com/PaladinFinance/Valkyrie/pull/5/commits/df40bd508cc1efd9dfe04a572d0d7db8178fb6a0).

**Cyfrin:** Verified. The overridden `_updateRewardState()` implementation and the `updateUserBoostedBalance()` function have been removed.
