---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-19-cedro-finance-1-4
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-03-19T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md
tags:
- firm:zokyo
- report:2024-03-19-cedro-finance
title: Strict equality used in `CEToken`
vuln_class: []
---

# Strict equality used in `CEToken`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-03-19-Cedro Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md)_

---

**Severity**: Medium

**Status**: Acknowledged

**Description**

Strict equality has been used in CEToken.sol. The transfer function can be frontrunned by a user to send a small amount to another user so that the following code on line: 173 of `_removeChain()` does not execute. For example, if Bob is sending his complete balance to Alice, then Eve could frontrun this transaction so that the Bob still has this small amount left. This would result in the if statement not executing at all. 
```solidity
if (balancePerChain[from][chainIds[i]] == 0)
```
The same issue exists on line: 293 in the `burnFromChain()` and line: 333 in the `burn()` function.

Similarly, strict equality has been used in Core.sol. The _removeToken can be made to not work as intended by denying the if code block to execute. This can be done by either sending a small amount of CEToken or DebtToken to the user, before call to `_removeToken()` is made. This can be done by frontrunning the `_removeToken()` with a griefing transaction to the user on whom the `_removeToken()` is being used.
This would also mean that call to `removeTokenForBorrower()` by `roleManager` will succeed is not guaranteed. Assuming otherwise could lead to flawed code logic.
For example, if `_removeToken()` is being called internally on address of Bob, then Eve can frontrun this transaction to send a small amount either `CEToken` or `DebtToken` to Bob so that the Bob still has this small amount left. This would result in the if statement on line: 671 not executing at all.

**Recommendation**: 

Although this is a griefing atttack, it would still be advised to use private mempools for these transactions such as Flashbots. And it is recommended to avoid using strict equality in code logic.

**Comments**: 

The client said that there would not be any problem to the user if they have a small amount left due to the front run attack. As only the cetoken can be transferred to other users.
