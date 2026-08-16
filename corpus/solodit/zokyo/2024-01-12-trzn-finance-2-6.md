---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-12-trzn-finance-2-6
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md
tags:
- firm:zokyo
- report:2024-01-12-trzn-finance
title: Typing error in the `RemoveContract_toStableToken()` function
vuln_class: []
---

# Typing error in the `RemoveContract_toStableToken()` function

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-01-12-TRZN Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**


In the MultiSig_V2 contract, the line: 145 in the RemoveContract_toStableToken() function is as follows:
```solidity
        IStalbeToken(StableToken).RemoveVaultManager(_target);(_target);
```
The code “(_target);” has been repeated twice in the function as an error and is not necessary. This could render confusion and render the contract undeployable.
     
**Recommendation**: 

It is advised to remove the duplication of (_target);
