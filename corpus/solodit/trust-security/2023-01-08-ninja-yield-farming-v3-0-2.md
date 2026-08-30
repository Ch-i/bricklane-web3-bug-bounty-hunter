---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-08-ninja-yield-farming-v3-0-2
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
title: TRST-H-3 Wrong accounting of user's holdings allows theft of reward
vuln_class: []
---

# TRST-H-3 Wrong accounting of user's holdings allows theft of reward

_Section severity (from Solodit section header): High_  
_Audit firm: Trust Security_  
_Source report: [2023-01-08-Ninja Yield Farming v3.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-08-Ninja%20Yield%20Farming%20v3.md)_

---

**Description:**
In `deposit()`, `withdraw()` and `withdrawProfit()`, `rewarder.onReward()` is called for reward 
bookkeeping. It will transfer previous eligible rewards and update the current amount user 
has:

```solidity
      user.amount = _amt;
      user.rewardDebt = (_amt * pool.accRewardPerShare) / ACC_TOKEN_PRECISION;
      user.rewardsOwed = rewardsOwed;
```

In `withdraw()`, there is a critical issue where `onReward()` is called too early:

```solidity
      // Update rewarder for this user
          if (address(rewarder) != address(0)) {
      rewarder.onReward(0, msg.sender, msg.sender, pending, user.amount);
      }
      // Burn baby burn
            _burn(msg.sender, _shares);
      // User accounting
                uint256 userAmount = balanceOf(msg.sender);
      // - Underlying (Frontend ONLY)
            if (userAmount == 0) {
               user.amount = 0;
         } else {
            user.amount -= r;
         }
```
The new **_amt** which will be stored in reward contract's **user.amount** is vault's **user.amount**, 
before decrementing the withdrawn amount. Therefore, the withdrawn amount is still 
gaining rewards even though it's no longer in the contract. Effectively it is stealing the 
rewards of others, leading to reward insolvency.
In order to exploit this flaw, attacker will deposit a larger amount and immediately withdraw 
it, except for one wei. When they would like to receive the rewards accrued for others, they 
will withdraw the remaining wei, which will trigger `onReward()`, which will calculate and 
send pending awards for the previously withdrawn amount. 


**Recommended Mitigation:**
Move the `onReward()` call to after user.amount is updated.

**Team response:**
Accepted and updated.
