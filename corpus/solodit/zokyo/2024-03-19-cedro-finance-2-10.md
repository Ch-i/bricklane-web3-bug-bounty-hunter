---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-19-cedro-finance-2-10
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-03-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md
tags:
- firm:zokyo
- report:2024-03-19-cedro-finance
title: Isolated assignments of Critical variables addresses
vuln_class: []
---

# Isolated assignments of Critical variables addresses

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-03-19-Cedro Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md)_

---

**Severity**: Low

**Status**: Acknowledged

**Description**

There are isolated and separate assignment of critical variable addresses for each contract although they are expected to be the same across the codebase.
But it is not advised to set the addresses of roleManager, core, etc. separately in each contract. This is because this can introduce errors as it could result in 
different addresses being assigned for each of the variables. For example it is possible that `Address_V1` is assigned to `roleManager` of DebtToken.sol whereas Address_V2 
is assigned to roleManager of Pool.sol, whereas in fact it should have been Address_V2 being assigned to both the variables of the two contracts.


**Recommendation**: 

It is advised to assign the address variables in only one contract, and let the rest of the contracts read, fetch and assign values from there during initialization/deployment of the contracts.
