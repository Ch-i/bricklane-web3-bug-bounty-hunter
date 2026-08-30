---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-19-cedro-finance-2-5
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
title: Missing validation in the method `swapRequest()`
vuln_class: []
---

# Missing validation in the method `swapRequest()`

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-03-19-Cedro Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

In Contract Branch.sol, the method `swapRequest(...)` allows to swap funds between different chains. It also allows ETH but does not check if `msg.value > qty` or not. The transaction will fail if `msg.value < qty`.

Even if it’s equal to qty, it will still fail as there is no `msg.value` left for the starGate router fee.

**Recommendation**: Add the following check:
```solidity
       if (msg.value == 0 && msg.value > qty) revert InsufficientValue(TAG, msg.value, 0);
```
