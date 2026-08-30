---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-08-ninja-yield-farming-v3-0-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-01-08T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-08-Ninja%20Yield%20Farming%20v3.md
tags:
- firm:trust-security
- report:2023-01-08-ninja-yield-farming-v3
title: TRST-H-2 Lack of child rewarder reserves could lead to freeze of funds
vuln_class: []
---

# TRST-H-2 Lack of child rewarder reserves could lead to freeze of funds

_Section severity (from Solodit section header): High_  
_Audit firm: Trust Security_  
_Source report: [2023-01-08-Ninja Yield Farming v3.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-08-Ninja%20Yield%20Farming%20v3.md)_

---

**Description:**
In ComplexRewarder.sol, `onReward()` is used to distribute rewards for previous time period, 
using the complex rewarder and any child rewarders. If the complex rewarder does not have 
enough tokens to hand out the reward, it correctly stores the rewards owed in storage. 
However, child rewarded will attempt to hand out the reward and may revert:

```solidity 
   function onReward(uint _pid, address _user, address _to, uint, uint _amt) external override onlyParent nonReentrant {
      PoolInfo memory pool = updatePool(_pid);
         if (pool.lastRewardTime == 0) return;
            UserInfo storage user = userInfo[_pid][_user];
            uint pending;
         if (user.amount > 0) {
              pending = ((user.amount * pool.accRewardPerShare) / ACC_TOKEN_PRECISION) - user.rewardDebt;
      rewardToken.safeTransfer(_to, pending);
         }
         user.amount = _amt;
         user.rewardDebt = (_amt * pool.accRewardPerShare) / 
            ACC_TOKEN_PRECISION;
      emit LogOnReward(_user, _pid, pending, _to);
      }
```
 Importantly, if the child rewarder fails, the parent's `onReward()` reverts too:
```solidity
      uint len = childrenRewarders.length();
         for (uint i = 0; i < len; ) {
      IRewarder(childrenRewarders.at(i)).onReward(_pid, _user, _to, 0, 
         _amt);
      unchecked {
         ++i;
         }
      }
```
In the worst-case scenario, this will lead the user's `withdraw()` call to V3 Vault, to revert.

**Recommended Mitigation:**
Introduce sufficient exception handling in the CompexRewarder.sol contract, so that 
`onReward()` would never fail.

**Team Response:**
Rejected. Child rewarders are not being used in the protocol and are out of the scope. We 
have kept the ability for them if needed, and they will be included in a future audit before 
use. We appreciate this being pointed out and will take care of the issue in future updates.
