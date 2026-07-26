---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-12-trzn-finance-3-9
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md
tags:
- firm:zokyo
- report:2024-01-12-trzn-finance
title: CEI not followed in `WithdrawEscrow()`
vuln_class: []
---

# CEI not followed in `WithdrawEscrow()`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-01-12-TRZN Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md)_

---

**Severity**: Informational

**Status**:  Resolved

**Description**

Checks effects interactions pattern has not been followed in the withdrawEscrow() function of the RiskManagerEscrow contract. As a result a compromised admin may be able carry out a reentrancy attack on the contract.

**Recommendation**: 

It is advised to follow checks-effects interactions pattern as a best practice for the same.
