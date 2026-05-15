---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-3-8
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Unnecessarily default safe math computation
vuln_class: []
---

# Unnecessarily default safe math computation

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

In TradingVaultV2.sol - By default arithmetic operations in soldity v0.8 are safe which incurs more computation. It is a good practice to avoid that extra computation if we are assured that a given arithmetic operation would be valid without the extra safe validations.
In TradingVaultV2.claimUSDT()
```solidity
require(currentBalanceUSDT > amount, "BALANCE_TOO_LOW");
currentBalanceUSDT -= amount;
```
Since currentBalanceUSDT is already greater than amount then subtraction shall not underflow.

**Recommendation** 

wrap arithmetic operations within unchecked.

**Fixed**: Issue fixed in commit a72e06b
