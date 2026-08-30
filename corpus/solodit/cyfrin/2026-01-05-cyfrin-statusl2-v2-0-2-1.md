---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-2-1
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
title: Users can be overslashed in `Karma.sol`
vuln_class: []
---

# Users can be overslashed in `Karma.sol`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-05-cyfrin-statusl2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md)_

---

**Description:** `Karma::_calculateSlashAmount` increases slashed amount to `MIN_SLASH_AMOUNT = 1e18` or even full balance:
```solidity
    function _calculateSlashAmount(uint256 balance) internal view returns (uint256) {
        uint256 amountToSlash = Math.mulDiv(balance, slashPercentage, MAX_SLASH_PERCENTAGE);
        if (amountToSlash < MIN_SLASH_AMOUNT) {
            if (balance < MIN_SLASH_AMOUNT) {
                // Not enough balance for minimum slash, slash entire balance
                amountToSlash = balance;
            } else {
                amountToSlash = MIN_SLASH_AMOUNT;
            }
        }
        return amountToSlash;
    }
```

Problem is that such rounding is applied multiple times in the same action
```solidity
    function _slash(address account, address rewardRecipient) internal virtual returns (uint256) {
        ...

        // first, calculate the total amount to slash from the actual reward tokens
@>      uint256 totalAmountToSlash = _calculateSlashAmount(super.balanceOf(account));

        for (uint256 i = 0; i < rewardDistributors.length(); i++) {
            address distributor = rewardDistributors.at(i);
            uint256 currentDistributorAccountBalance = IRewardDistributor(distributor).rewardsBalanceOfAccount(account);

            // then, calculate the amount to slash from each reward distributor
@>          totalAmountToSlash += _calculateSlashAmount(currentDistributorAccountBalance);

            // turn virtual Karma into real Karma for slashing
            IRewardDistributor(distributor).redeemRewards(account);
        }

        ...

        // Burn the entire slashed amount from the account
        _burn(account, totalAmountToSlash);

        ...
    }
```

Suppose following scenario:
1) Current balance is `0.9e18`
2) Virtual balances in RewardDistributors are `0.8e18` and `0.7e18`
3) Finally it will slash full `2.4e18` because every amount is rounded up. Actually it should slash only 50%, i.e. `1.2e18`

**Impact:** Users are overslashed on low balance

**Recommended Mitigation:** Apply min amount calculation only once on final amount in `Karma::_slash`.

**StatusL2:** Fixed in [cc00600](https://github.com/status-im/status-network-monorepo/commit/cc00600de5f0b67552a370d198cf6675d0d6fffb).

**Cyfrin:** Verified.
