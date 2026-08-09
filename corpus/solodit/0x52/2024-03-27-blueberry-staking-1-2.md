---
affected_contracts: []
derives_from: []
id: solodit-0x52-2024-03-27-blueberry-staking-1-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-03-27T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-03-27-Blueberry-Staking.md
tags:
- firm:0x52
- report:2024-03-27-blueberry-staking
title: '[M-03] Rewards will be permanently lost for ibToken with no deposits'
vuln_class: []
---

# [M-03] Rewards will be permanently lost for ibToken with no deposits

_Section severity (from Solodit section header): Medium_  
_Audit firm: 0x52_  
_Source report: [2024-03-27-Blueberry-Staking.md](https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-03-27-Blueberry-Staking.md)_

---

**Details**

[BlueberryStaking.sol#L482-L485](https://github.com/Blueberryfi/blueberry-staking/blob/efaf7fc690e38914ba475d5ac61a4d0bd3f45c0d/src/BlueberryStaking.sol#L482-L485)

    function rewardPerToken(address _ibToken) public view returns (uint256) {
        if (totalSupply[_ibToken] == 0) {
            return rewardPerTokenStored[_ibToken];
        }

[BlueberryStaking.sol#L782-L790](https://github.com/Blueberryfi/blueberry-staking/blob/efaf7fc690e38914ba475d5ac61a4d0bd3f45c0d/src/BlueberryStaking.sol#L782-L790)

    rewardPerTokenStored[_ibToken] = rewardPerToken(_ibToken);
    lastUpdateTime[_ibToken] = lastTimeRewardApplicable(_ibToken);

    if (_user != address(0)) {
        rewards[_user][_ibToken] = _earned(_user, _ibToken);
        userRewardPerTokenPaid[_user][_ibToken] = rewardPerTokenStored[
            _ibToken
        ];
    }

When distributing rewards, the reward rate and elapsed time are used to determine the number of tokens to distribute. If no ibTokens are deposited, rewards cannot be distributed, however the timestamp in this scenario is still updated. This leads all rewards during this period to be lost.

Additionally rewards are added at the same time that ibTokens are registered and allowed to be deposited. This causes a guaranteed loss of some rewards for every ibToken. The longer it goes before the first deposit the more tokens that are lost.

**Lines of Code**

[BlueberryStaking.sol#L777-L791](https://github.com/Blueberryfi/blueberry-staking/blob/efaf7fc690e38914ba475d5ac61a4d0bd3f45c0d/src/BlueberryStaking.sol#L777-L791)

**Recommendation**

The timestamp should not be updated for an ibToken if there is none of that token deposited.

**Remediation**

Fixed in [PR#29](https://github.com/Blueberryfi/blueberry-staking/pull/29) as recommended.
