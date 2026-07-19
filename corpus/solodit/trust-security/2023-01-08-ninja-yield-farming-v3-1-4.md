---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-08-ninja-yield-farming-v3-1-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-01-08T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-08-Ninja%20Yield%20Farming%20v3.md
tags:
- firm:trust-security
- report:2023-01-08-ninja-yield-farming-v3
title: TRST-M-5 potential overflow in reward accumulator may freeze functionality
vuln_class: []
---

# TRST-M-5 potential overflow in reward accumulator may freeze functionality

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-01-08-Ninja Yield Farming v3.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-08-Ninja%20Yield%20Farming%20v3.md)_

---

**Description:** 
Note the above description of `updatePool()` functionality. We can see that **accRewardPerShare** is only allocated 128 bits in **PoolInfo:**
```solidity
      struct PoolInfo {
          uint128 accRewardPerShare;
            uint64 lastRewardTime;
               uint64 allocPoint;
```
Therefore, even if truncation issues do not occur, it is likely that continuous incrementation 
of the counter would cause **accRewardPerShare** to overflow, which would freeze vault 
functionalities such as withdrawal.
 
**Recommended Mitigation:**
Steal 32 bits from lastRewardTime and 32 bits from allocPoint to make the accumulator have 
192 bits, which should be enough for safe calculations.


**Team response:**
Accepted. We updated PoolInfo.accRewardPerShare to uint256.
