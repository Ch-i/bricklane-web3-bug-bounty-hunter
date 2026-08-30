---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-2-6
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-01-05T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-05-cyfrin-statusl2-v2-0
title: '`DeployProtocol.s.sol` incorrectly allows transfers to `StakeManager.sol`'
vuln_class: []
---

# `DeployProtocol.s.sol` incorrectly allows transfers to `StakeManager.sol`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-05-cyfrin-statusl2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md)_

---

**Description:** `DeployProtocol.s.sol` is used to automatically deploy and configure protocol. Contracts `StakeManager.sol` and `SimpleKarmaDistributor.sol` should be allowed to transfer Karma token. However it provides `stakeManager` both times:
```solidity
        // whitelist reward distributors for transferring Karma tokens
        karma.setAllowedToTransfer(address(stakeManager), true);
        console.log("Whitelisted reward distributor (StakeManager)", address(stakeManager), "for transfer");
@>      karma.setAllowedToTransfer(address(stakeManager), true);
        console.log(
            "Whitelisted reward distributor (SimpleKarmaDistributor)", address(simpleKarmaDistributor), "for transfer"
        );
```

**Impact:** `SimpleKarmaDistributor::redeemRewards` will revert. It means that slashing won't work because `Karma::_slash` iterates over all reward distributors:
```solidity
    function _slash(address account, address rewardRecipient) internal virtual returns (uint256) {
        uint256 currentBalance = _balanceOf(account);
        if (currentBalance == 0) {
            revert Karma__CannotSlashZeroBalance();
        }

        // first, calculate the total amount to slash from the actual reward tokens
        uint256 totalAmountToSlash = _calculateSlashAmount(super.balanceOf(account));

        for (uint256 i = 0; i < rewardDistributors.length(); i++) {
            address distributor = rewardDistributors.at(i);
            uint256 currentDistributorAccountBalance = IRewardDistributor(distributor).rewardsBalanceOfAccount(account);

            // then, calculate the amount to slash from each reward distributor
            totalAmountToSlash += _calculateSlashAmount(currentDistributorAccountBalance);

            // turn virtual Karma into real Karma for slashing
@>          IRewardDistributor(distributor).redeemRewards(account);
        }
```

**Recommended Mitigation:**
```diff
        // whitelist reward distributors for transferring Karma tokens
        karma.setAllowedToTransfer(address(stakeManager), true);
        console.log("Whitelisted reward distributor (StakeManager)", address(stakeManager), "for transfer");
-       karma.setAllowedToTransfer(address(stakeManager), true);
+       karma.setAllowedToTransfer(address(simpleKarmaDistributor), true);
        console.log(
            "Whitelisted reward distributor (SimpleKarmaDistributor)", address(simpleKarmaDistributor), "for transfer"
        );
```

**StatusL2:** Fixed in [025f790](https://github.com/status-im/status-network-monorepo/commit/025f790f92f9fa0f40bb905b9db3a7a5473134e6).

**Cyfrin:** Verified.
