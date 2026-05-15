---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-1-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: ETH might get stuck on the contract's balance.
vuln_class: []
---

# ETH might get stuck on the contract's balance.

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

1) LiquidityZap.sol: standardAdd(). 
BalancerPoolHelper.sol: zapTokens(). 
Function is marked as payable, allowing users to send Ether when calling it. However this function never interacts with msg.value, thus sending Ether to it has no effect. Thus any Ether, sent with this function, will be stuck on the contract. 
2) LockZap.sol: zapFromVesting(), line 118. 
In case parameter_borrow' is true, any sent Ether will get stuck on the contract's balance. 
Thus, in case_borrow is true, it should be validated that no Ether is sent with the function. 

**Recommendation**: 

1. Remove payable modifier OR add interaction with Ether in the function. 
2. Add a validation that in case '_borrow' is true, msg.value is equal to 0.
