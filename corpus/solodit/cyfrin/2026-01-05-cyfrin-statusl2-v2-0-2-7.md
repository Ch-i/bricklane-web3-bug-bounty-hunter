---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-2-7
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-01-05T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-05-cyfrin-statusl2-v2-0
title: Slashing doesn't work if any reward distributor is paused
vuln_class: []
---

# Slashing doesn't work if any reward distributor is paused

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-05-cyfrin-statusl2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md)_

---

**Description:** `Karma::_slash` iterates over all reward distributors and claims rewards by calling `IRewardDistributor::redeemRewards`:
```solidity
    function _slash(address account, address rewardRecipient) internal virtual returns (uint256) {
        ...

        for (uint256 i = 0; i < rewardDistributors.length(); i++) {
            address distributor = rewardDistributors.at(i);
            uint256 currentDistributorAccountBalance = IRewardDistributor(distributor).rewardsBalanceOfAccount(account);

            // then, calculate the amount to slash from each reward distributor
            totalAmountToSlash += _calculateSlashAmount(currentDistributorAccountBalance);

            // turn virtual Karma into real Karma for slashing
@>          IRewardDistributor(distributor).redeemRewards(account);
        }

        ...
    }
```

Problem is that `StakeManager::redeemRewards` is pausable:
```solidity
    function redeemRewards(address account) external onlyNotEmergencyMode whenNotPaused returns (uint256) {
```

So users can't be slashed if any reward distributor is paused.

**Impact:** Slashing doesn't work if any reward distributor is paused

**Recommended Mitigation:** Consider adding function `isPaused() returns (bool)` to `interface IRewardDistributor` and skip paused during slashing.

**StatusL2:** Fixed in [99b73b0](https://github.com/status-im/status-network-monorepo/commit/99b73b0d6060d2c9eee916006b57ad3f5d3913c1).

**Cyfrin:** Verified.

\clearpage
