---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-21-cyfrin-illuvium-stakingv3-v2-0-1-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-10-21T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-21-cyfrin-illuvium-stakingv3-v2-0
title: Redundant recomputation of accrued rewards in `StakingVault::_updateRewards`
vuln_class: []
---

# Redundant recomputation of accrued rewards in `StakingVault::_updateRewards`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md)_

---

**Description:** In [`StakingVault::_updateRewards`](https://github.com/0xKaizenLabs/staking-contracts-v3/blob/c78653ed5f2e5a6d5ace13c303a8765fe30679b0/src/StakingVault.sol#L291-L295), `accrued` is calculated and then the exact same expression is recomputed for `totalRewardDebt`. The second calculation is unnecessary.

```solidity
uint256 accrued = (staked * _acc) / _scale;
if (accrued > userInfo.totalRewardDebt) {
    userInfo.storedPendingRewards += accrued - userInfo.totalRewardDebt;
}
// @audit Recomputed unnecessarily
userInfo.totalRewardDebt = (staked * _acc) / _scale;
```

Consider reusing the already computed value:

```solidity
uint256 accrued = (staked * _acc) / _scale;
if (accrued > userInfo.totalRewardDebt) {
    userInfo.storedPendingRewards += accrued - userInfo.totalRewardDebt;
}
userInfo.totalRewardDebt = accrued;
```

**Illuvium:** Fixed in commit [5f273bc](https://github.com/0xKaizenLabs/staking-contracts-v3/commit/5f273bc8a196170162400c33a43efe2fb84f0013).

**Cyfrin:** Verified.
