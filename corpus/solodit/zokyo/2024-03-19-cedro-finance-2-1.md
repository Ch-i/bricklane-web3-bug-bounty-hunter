---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-19-cedro-finance-2-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-03-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md
tags:
- firm:zokyo
- report:2024-03-19-cedro-finance
title: Underflow issue in `swap()` method
vuln_class: []
---

# Underflow issue in `swap()` method

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-03-19-Cedro Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

In Contract Core.sol, the `swap()` method has the following logic:

```solidity
function swap(
       bytes32 id,
       bytes32 srcChainId,
       bytes32 destChainId,
       uint256 tokenAmountInSrc,
       uint256 tokenAmountInDest
   ) external onlyRole(IRoleManager(roleManager).POOL()) {
       if (tokenAmountInDest > tokenAmountInSrc) {
           revert ExcessLiquidityInDest(TAG);
       }
       chainLiquidity[srcChainId][id] -= tokenAmountInSrc; 
…}
```
Here if `chainLiquidity[srcChainId][id] < tokenAmountInSrc`, it will lead to underflow panic error.

**Recommendation**: 

It is advised to check if `chainLiquidity[srcChainId][id] >= tokenAmountInSrc` before the operation.
