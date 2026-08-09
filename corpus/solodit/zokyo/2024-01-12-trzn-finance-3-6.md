---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-12-trzn-finance-3-6
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md
tags:
- firm:zokyo
- report:2024-01-12-trzn-finance
title: Repetitive condition check
vuln_class: []
---

# Repetitive condition check

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-01-12-TRZN Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

In Contract VaultETH_V2, the method Redeem_BuyETH(...) first asserts the following:
```solidity
 userWithdrawRequest.requestWithdrawAmt <= address(this).balance
```
Later on, check the same in an `if` condition which is not needed as it is already asserted to be true and no ETH transfers happened between those lines.

**Recommendation**: 

Remove this check from the `if` condition.
