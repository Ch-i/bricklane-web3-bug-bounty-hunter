---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-08-ninja-yield-farming-v3-1-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-01-08T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-08-Ninja%20Yield%20Farming%20v3.md
tags:
- firm:trust-security
- report:2023-01-08-ninja-yield-farming-v3
title: TRST-M-4 truncation in reward calculation could cause leakage of rewards
vuln_class: []
---

# TRST-M-4 truncation in reward calculation could cause leakage of rewards

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-01-08-Ninja Yield Farming v3.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-08-Ninja%20Yield%20Farming%20v3.md)_

---

**Description:**
In ComplexRewarder.sol, `updatePool()` call updates values in the specified pool.
```solidity
      uint lpSupply = IVault(VAULT).balance();
          if (lpSupply > 0) {
      uint time = block.timestamp - pool.lastRewardTime;
                uint reward = totalAllocPoint == 0 ? 0 : ((time * rewardPerSecond * 
                  pool.allocPoint) / totalAllocPoint);
               pool.accRewardPerShare = pool.accRewardPerShare + uint128((reward * 
          ACC_TOKEN_PRECISION) / lpSupply);
      }
```
**reward** could be a fairly large number. The decimals of **reward * ACC_TOKEN_PRECISION** is 
10**30, because of how ACC_TOKEN_PRECISION is defined:

```solidity
         ACC_TOKEN_PRECISION = 10 ** (30 - decimalsRewardToken);
```

**lpSupply** is given in LP's decimals, but could be as small as 1. If **lpSupply** is 1, **reward** of 
2**28 = 268435456 will be enough to cause uint128 overflow of the product (10 * * 30 is 100 
bits). Therefore, it is shown that this calculation is not safe under 128-bit math. The impact
would be **pool.accRewardPerShare** increasing by a tiny amount in relation to the correct 
amount.

**Recommendation:**
Use a larger int type to handle the above calculation. 

**Team response**
Accepted. We updated to uint192 and can move to uint256 if you prefer
