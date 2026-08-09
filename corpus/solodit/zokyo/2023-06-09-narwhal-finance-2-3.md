---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-2-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Redundant if branching in deposit
vuln_class: []
---

# Redundant if branching in deposit

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

In TradingVaultV2.sol - Method deposit(uint,address): Unnecessary if branching
```solidity
if (allowed[msg.sender]) {
    console.log("Allowed");
    IERC20(USDT).safeTransferFrom(msg.sender, address(this), _amount);
    harvest(user);
} else {
    console.log("Not allowed");
    IERC20(USDT).safeTransferFrom(user, address(this), _amount);
    harvest(msg.sender);
}
```
Since user already takes the value of msg.sender in the else branch and that is given by the if-statement  before it (i.e. which checks the same condition).

**Recommendation** 

Remove if statement and replace by
```solidity
require(storageT.USDT().transferFrom(msg.sender, address(this), _amount));
harvest(user);
```
**Fixed**: Issue fixed in commit a72e06b
