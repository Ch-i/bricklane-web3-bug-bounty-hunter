---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-2-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-01-05T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-05-cyfrin-statusl2-v2-0
title: '`ERC20VotesUpgradeable::getPastTotalSupply` overestimates the value'
vuln_class: []
---

# `ERC20VotesUpgradeable::getPastTotalSupply` overestimates the value

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-05-cyfrin-statusl2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md)_

---

**Description:** Karma token is used for voting. `ERC20VotesUpgradeable` keeps track of checkpoints: 1) balance of user at certain block, 2) `totalSupply` at certain block. Already minted but not yet distributed tokens are excluded from accounting in both `balanceOf` and `totalSupply` in `Karma.sol`:
```solidity
    function balanceOf(address account) public view override returns (uint256) {
        if (rewardDistributors.contains(account)) {
            return 0;
        }
        return _balanceOf(account);
    }

    function totalSupply() public view override returns (uint256) {
        uint256 externalSupply = 0;
        uint256 totalDistributorBalance = 0;

        for (uint256 i = 0; i < rewardDistributors.length(); i++) {
            IRewardDistributor distributor = IRewardDistributor(rewardDistributors.at(i));
            externalSupply += distributor.totalRewardsSupply();
            totalDistributorBalance += super.balanceOf(address(distributor));
        }

        if (externalSupply > totalDistributorBalance) {
            externalSupply = totalDistributorBalance;
        }

        // subtract the distributor balances to avoid double counting
        return super.totalSupply() - totalDistributorBalance + externalSupply;
    }
```

However internal checkpoint accounting in `ERC20VotesUpgradeable.sol` doesn't use updated `Karma::totalSupply`, it simply increases by amount of `mint` and `burn`:
```solidity
    function _mint(address account, uint256 amount) internal virtual override {
        super._mint(account, amount);
        require(totalSupply() <= _maxSupply(), "ERC20Votes: total supply risks overflowing votes");

        _writeCheckpoint(_totalSupplyCheckpoints, _add, amount);
    }

    /**
     * @dev Snapshots the totalSupply after it has been decreased.
     */
    function _burn(address account, uint256 amount) internal virtual override {
        super._burn(account, amount);

        _writeCheckpoint(_totalSupplyCheckpoints, _subtract, amount);
    }
```



**Impact:** Total supply is overestimated by not yet distributed tokens. Usually total supply is used for quorum during voting, in this case quorum value is incorrect

**Recommended Mitigation:** TBD. Likely, mint and burn functions should not update `totalSupply` if that's reward distributor, rather `totalSupply` should be updated when rewards are distributed.

**StatusL2:** Acknowledged, as the team are not planning to rely on 'getPastTotalSupply'.
