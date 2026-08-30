---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-3-4
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: Comments don't correspond to the code.
vuln_class: []
---

# Comments don't correspond to the code.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

1. MultiFee Distribution.sol: initialize(). 
The commentary section stated that the first token in the array of rewards must be a staking token. As a function has a parameter '_stakingToken', one may assume this token must be the first one in the rewards array (based on comments). However, another token, '_rdntToken', is pushed to the array instead. Thus, this doesn't correspond to the comments and should be verified by the team. 
Eligibility DataProvider.sol: lastEligibleTime(). 
The commentary section stated that the function returns locked RDNT and LP token values in ETH. However, the function's name and the return variable's name imply that the function returns the last eligible timestamp. 

**Recommendation**: 

1. Verify that _rdntToken' should be the first one in the rewards array and update comments OR verify that '_rdntToken' and '_stakingToken' are the same token OR update the code and push_staking Token' to the rewards array. 
2. Verify the correctness of the return value in function.
