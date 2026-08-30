---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-10-29-liberty-finance-1-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-10-29T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-29-Liberty%20Finance.md
tags:
- firm:zokyo
- report:2024-10-29-liberty-finance
title: Disable initializer
vuln_class: []
---

# Disable initializer

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-10-29-Liberty Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-29-Liberty%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

Contract AmanaVaultV1 and Contract Rewards do not disable initializer as recommended by OpenZeppelin  by adding the code as  follows:
```solidity
constructor() {
       _disableInitializers();
   }
```
**Recommendation**: 

Disable intializers by adding the above code.
