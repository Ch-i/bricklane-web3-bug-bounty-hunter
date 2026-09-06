---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-05-24-struct-finance-1-8
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-05-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md
tags:
- firm:zokyo
- report:2023-05-24-struct-finance
title: trancheDurationMax can be less than trancheDurationMin
vuln_class: []
---

# trancheDurationMax can be less than trancheDurationMin

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-05-24-Struct Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved


**Description**: 

Although the functions to set the maximum and minimum tranche duration have onlyRole(GOVERNANCE) function modifier, decreasing the possibility of having trancheDurationMax < trancheDurationMin in the state of the contract, the contract can still have trancheDurationMax < trancheDurationMin. 

**Recommendation**: 

Add checks in the function setMinimumTrancheDuration() and setMaximumTrancheDuration() to avoid this state in the contract.
