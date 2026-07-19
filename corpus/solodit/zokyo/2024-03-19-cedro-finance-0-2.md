---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-19-cedro-finance-0-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-03-19T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md
tags:
- firm:zokyo
- report:2024-03-19-cedro-finance
title: Minted `ceTokens` not added to users list if minted using `Repay()`
vuln_class: []
---

# Minted `ceTokens` not added to users list if minted using `Repay()`

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2024-03-19-Cedro Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md)_

---

**Severity**: High

**Status**: Resolved

**Description**

In Contract Core.sol, the method `repay(...)` allows a user to deposit any extra amount more than the repay amount. This deposit mints `ceTokens` for the user but the same is not added using `_addToken(...)` method to keep a record of all the `ceTokens` held by the user.

This impacts the `borrow(...)` for the user or risk liquidation of users collateral because the earlier minted ceTokens will not be counted towards the health factor calculation because of the following logic:
```solidity
function healthFactor(
       address user
   ) public view returns (Data.HealthData memory health) {
       bytes32[] memory ids = users[user];
       if (ids.length > 0) {
           uint256[] memory prices = oracle.getPrices(ids);
           for (uint256 i; i < ids.length; i++) { … }
     … }
 … }
```
Here only ids in the `users[user]` list are used for calculating the health factor. 

**Recommendation**: 

Add the `ceToken` using `_addToken(...)` for users using `repay(...)` to mint ceTokens.
