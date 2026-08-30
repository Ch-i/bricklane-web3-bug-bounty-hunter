---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-14-ondo-finance-3-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-06-14T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-14-Ondo%20Finance.md
tags:
- firm:zokyo
- report:2023-06-14-ondo-finance
title: '`rwaOracle` should be immutable'
vuln_class: []
---

# `rwaOracle` should be immutable

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-06-14-Ondo Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-14-Ondo%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

In the contract Pricer.sol on the line 45 there is a state variable which value is assigned during in the constructor and not defined elsewhere in the code.

**Recommendation**: 

add the `immutable` attribute to state variables that never change or are set only in the constructor
