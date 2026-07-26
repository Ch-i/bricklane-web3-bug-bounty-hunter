---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-12-trzn-finance-1-6
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md
tags:
- firm:zokyo
- report:2024-01-12-trzn-finance
title: Missing reentrancy guard in EmergencyWithdraw / WithdrawEscrow
vuln_class: []
---

# Missing reentrancy guard in EmergencyWithdraw / WithdrawEscrow

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-01-12-TRZN Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md)_

---

**Severity**: Medium

**Status**: Resolved

**Description**

By adding the nonreentrant modifier, you can help ensure that the function is not vulnerable to reentrancy attacks, especially when interacting with external contracts.
