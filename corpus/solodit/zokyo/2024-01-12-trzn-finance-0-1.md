---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-12-trzn-finance-0-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md
tags:
- firm:zokyo
- report:2024-01-12-trzn-finance
title: Missing access control check
vuln_class: []
---

# Missing access control check

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2024-01-12-TRZN Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md)_

---

**Severity**: High

**Status**: Resolved 

**Description**

In Contract VaultETH_V2, the method RM_UpdateReward(...) should only be callable by an account that has the RISK_MANAGER  role as per the comment similar to the method RM_UpdateDeposit(...).
Since this method has no access control check, malicious users can call this method which can cause DoS for other users to mint ZeUSD tokens as this method internally calls the `SellETH()` method which can mint max amount of ZeUSD as the `SellETH()` method allows this contract to mint as many tokens as possible with no upper limit. 

**Recommendation**: 

Add the following check in the method RM_UpdateReward().

```solidity
       assert(hasRole(RISK_MANAGER, msg.sender));
```
