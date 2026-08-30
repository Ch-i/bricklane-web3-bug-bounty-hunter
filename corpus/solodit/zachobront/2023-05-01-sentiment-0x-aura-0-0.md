---
affected_contracts: []
derives_from: []
id: solodit-zachobront-2023-05-01-sentiment-0x-aura-0-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-05-01T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-05-01-Sentiment-0x-Aura.md
tags:
- firm:zachobront
- report:2023-05-01-sentiment-0x-aura
title: '[H-01] AURA token will not be accounted for in `tokensIn`'
vuln_class: []
---

# [H-01] AURA token will not be accounted for in `tokensIn`

_Section severity (from Solodit section header): High_  
_Audit firm: ZachObront_  
_Source report: [2023-05-01-Sentiment-0x-Aura.md](https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-05-01-Sentiment-0x-Aura.md)_

---

When the controller sees a call to Aura's `getReward()` function, it uses the following logic to set `tokensOut` and `tokensIn`:
```solidity
function canCallGetReward(address target) internal view returns (bool, address[] memory, address[] memory) {
    uint256 rewardLength = IRewards(target).extraRewardsLength();
    address[] memory tokensIn = new address[](rewardLength + 1);
    for (uint256 i = 0; i < rewardLength; i++) {
        tokensIn[i] = IRewards(IRewards(target).extraRewards(i)).rewardToken();
    }
    tokensIn[rewardLength] = IRewards(target).rewardToken();
    return (true, tokensIn, new address[](0));
}
```
This sets the `tokensIn` to equal an array with all the `extraRewards` tokens, as well as the target contract's `rewardToken`.

However, if we examine the code itself, we will see that `getReward()` sends out all the tokens we accounted for (the `rewardToken` as well as all the `extraRewards`) and also makes the following call:
```solidity
IDeposit(operator).rewardClaimed(pid, _account, reward);
```
https://github.com/convex-eth/platform/blob/b93b7b77169777f3d508feffc646042709e40ef7/contracts/contracts/BaseRewardPool.sol#L263-L279

Following that logic, we find the following function in the `Booster.sol` contract:
```solidity
function rewardClaimed(uint256 _pid, address _address, uint256 _amount) external returns(bool){
    address rewardContract = poolInfo[_pid].crvRewards;
    require(msg.sender == rewardContract || msg.sender == lockRewards, "!auth");

    //mint reward tokens
    ITokenMinter(minter).mint(_address,_amount);

    return true;
}
```
https://github.com/convex-eth/platform/blob/b93b7b77169777f3d508feffc646042709e40ef7/contracts/contracts/Booster.sol#L458C12-L466

As we can see, this additional call mints the `AURA` token to the `receiver`.

This token is not accounted for in `tokensIn`, which means it will not contribute to an account's balance in Sentiment. As a result, the account could be unfairly liquidated due to the missing balance.

**Recommendation**

Add the `AURA` token to the `tokensIn` array. If the deployment on Arbitrum matches Mainnet, it can be accessed as follows:
```solidity
IBooster(IRewards(target).operator()).minter();
```

**Review**

Fixed in [commit 49db04366e255568f0cab1e6e083b9fff808b384](https://github.com/sentimentxyz/controller/pull/64/commits/49db04366e255568f0cab1e6e083b9fff808b384) as recommended.
