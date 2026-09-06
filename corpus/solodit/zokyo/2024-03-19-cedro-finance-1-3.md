---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-19-cedro-finance-1-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-03-19T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md
tags:
- firm:zokyo
- report:2024-03-19-cedro-finance
title: Centralization issues
vuln_class: []
---

# Centralization issues

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-03-19-Cedro Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md)_

---

**Severity**: Medium

**Status**: Acknowledged

**Description**

In `CEToken.sol`, the `setCore()` allows to reset the core and `PoolId` and overwrite them. 
`setTransferBlockRelease()` can be used to freeze the assets of any user by a malicious admin indefinitely. Also, the `setTransferBlockWait()` can be set to a very large value. 

The function `setRoleManager()` on line: 82 can be used to change the address of the `roleManager` at any time. Same goes for the `setRewardController()` function on line: 105. 
The same goes for `setRoleManager()` function, `setFeeProvider()` and `setCore()` function in Pool.sol. 
It also exists in `setRoleManager()` and `setDexFactory()` functions in Oracle.sol. The same goes for `setCore()` and `setRoleManager()` of LiquidationManager.sol 
The `setCore()` and `setRoleManager()` functions of `FeeProvider.sol` and the `setRoleManager()` function of `Core.sol`. And also `setRoleManager()` function of `AdapterPool.sol`. 

The same is applicable for `setRoleManager()`, `setAdapter()` and `setStargateRouterAndVault()` of `Branch.sol`. 

**Recommendation**: 

It is advised to follow the following recommendations in order to fix this issue:

- Use a multisig wallet for the contract and the roles, in order to increase decentralization and minimize the risk of malicious admin or loss of private keys. 
- It is advised to introduce a sufficient MAX cap for the num parameter of setTransferBlockWait() function, otherwise it can also lead to a Denial of Service attack in case it is set to a very large value by a malicious or compromised admin.
**Comments**: The client said that they accept that there is centralization and will inform the user about it.
