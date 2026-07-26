---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-1-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: Iteration though the whole storage array.
vuln_class: []
---

# Iteration though the whole storage array.

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

MultiFee Distribution.sol: _cleanWithdrawableLocks(), line 1119; withdraw(), line 754. 
After the withdrawal of locks or earnings, the contract performs an iteration through the whole storage array. For example, if a user creates a significant amount of locks, iteration might consume more gas than can fit in one transaction. Thus, the user's funds might get stuck. The issue is marked a medium-risk since it might affect certain users, not the whole protocol. However, it is still recommended not to allow users to create infinite elements in the array to mitigate this issue. 

**Recommendation**: 

Consider restricting the maximum amount of elements in storage arrays 
`userEarnings[user]` and `userLocks [onBehalfOf] OR set a minimal amount of tokens, which can be locked or minted per one time, so that a user can't create too many locks with low values. 

**Post-audit**: 

Restriction was added in function_cleanWithdrawableLocks(). User will have to call function multiple times if he has a great amount of locks.
