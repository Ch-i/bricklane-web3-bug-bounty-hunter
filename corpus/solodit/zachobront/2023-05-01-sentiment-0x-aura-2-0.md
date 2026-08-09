---
affected_contracts: []
derives_from: []
id: solodit-zachobront-2023-05-01-sentiment-0x-aura-2-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-05-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-05-01-Sentiment-0x-Aura.md
tags:
- firm:zachobront
- report:2023-05-01-sentiment-0x-aura
title: '[L-01] Aura''s `withdraw()` and `redeem()` functions do not send any reward
  tokens'
vuln_class: []
---

# [L-01] Aura's `withdraw()` and `redeem()` functions do not send any reward tokens

_Section severity (from Solodit section header): Low_  
_Audit firm: ZachObront_  
_Source report: [2023-05-01-Sentiment-0x-Aura.md](https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-05-01-Sentiment-0x-Aura.md)_

---

When the controller sees a call to Aura's `withdraw()` or `redeem()` function, it sets `tokensIn` to an array of the `asset` along with all reward tokens:
```solidity
function canCallWithdrawAndRedeem(address target)
    internal
    view
    returns (bool, address[] memory, address[] memory)
{
    uint256 rewardLength = IRewards(target).extraRewardsLength();
    address[] memory tokensIn = new address[](rewardLength + 2);
    for (uint256 i = 0; i < rewardLength; i++) {
        tokensIn[i] = IRewards(IRewards(target).extraRewards(i)).rewardToken();
    }
    tokensIn[rewardLength] = IERC4626(target).asset();
    tokensIn[rewardLength + 1] = IRewards(target).rewardToken();

    address[] memory tokensOut = new address[](1);
    tokensOut[0] = target;
    return (true, tokensIn, tokensOut);
}
```
However, if we examing the code, we will see that no rewards are sent, so the `tokensIn` array could simply be set to `[asset]`.
```solidity
function _withdrawAndUnwrapTo(uint256 amount, address from, address receiver) internal updateReward(from) returns(bool){
    //also withdraw from linked rewards
    for(uint i=0; i < extraRewards.length; i++){
        IRewards(extraRewards[i]).withdraw(from, amount);
    }

    _totalSupply = _totalSupply.sub(amount);
    _balances[from] = _balances[from].sub(amount);

    //tell operator to withdraw from here directly to user
    IDeposit(operator).withdrawTo(pid,amount,receiver);
    emit Withdrawn(from, amount);

    emit Transfer(from, address(0), amount);

    return true;
}
```
https://github.com/aurafinance/convex-platform/blob/3cd1ce3657bae8abb975b9dd06f28247c22880d3/contracts/contracts/BaseRewardPool.sol#LL269C1-L285C6

We can see that there is no call to withdraw the `rewardToken` of the main pool.

While it seems that there are withdrawals of the `extraRewards`, the `withdraw()` function on those does not actually claim those rewards, it simply uses the `updateReward()` modifier to update the stored rewards waiting to be claimed:
```solidity
function withdraw(address _account, uint256 amount)
    public
    updateReward(_account)
{
    require(msg.sender == address(deposits), "!authorized");
    //require(amount > 0, 'VirtualDepositRewardPool : Cannot withdraw 0');

    emit Withdrawn(_account, amount);
}
```
https://github.com/aurafinance/convex-platform/blob/3cd1ce3657bae8abb975b9dd06f28247c22880d3/contracts/contracts/VirtualBalanceRewardPool.sol#L179-L187

**Recommendation**

The `canCallWithdrawAndRedeem()` function can be simplified to only include the `IERC4626(target).asset()` token in the `tokensIn` array.

**Review**

Fixed in [commit 49db04366e255568f0cab1e6e083b9fff808b384](https://github.com/sentimentxyz/controller/pull/64/commits/49db04366e255568f0cab1e6e083b9fff808b384) as recommended.
