---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-12-trzn-finance-0-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md
tags:
- firm:zokyo
- report:2024-01-12-trzn-finance
title: Reentrancy attack is possible on `SellETH` function
vuln_class: []
---

# Reentrancy attack is possible on `SellETH` function

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2024-01-12-TRZN Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md)_

---

**Severity**: High

**Status**: Resolved

**Description**

The `SellETH` function sends Ether to risk managers, if these risk managers are contracts that have malicious code, there is a possibility of reentrancy attack. Even though this contract inherits ReentrancyGaurd, the guard will only apply to functions that have nonreentrant modifier.


**Recommendations**:

To mitigate this risk, it's generally a good practice to mark the function with nonreentrant modifiers from openzeppelin.

Also place Ether transfer operation at the end of function. By doing this, the transfer operation occurs after all state changes are completed, reducing the risk of reentrancy attacks.
