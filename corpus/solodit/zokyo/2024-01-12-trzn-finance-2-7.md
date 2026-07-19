---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-12-trzn-finance-2-7
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md
tags:
- firm:zokyo
- report:2024-01-12-trzn-finance
title: Transfer ownership to zero address in `RiskManagerEscrow_V2`
vuln_class: []
---

# Transfer ownership to zero address in `RiskManagerEscrow_V2`

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-01-12-TRZN Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

 The `transferOwnership` function can be used to accidentally transfer ownership of the contract to a zero address and revoke the role of the current owner. This would lead to  `onlyRole(DEFAULT_ADMIN_ROLE)` function uncallable. 

**Recommendation**: 

To avoid this it is advised to add a zero address check for the newOwner parameter of the function.
