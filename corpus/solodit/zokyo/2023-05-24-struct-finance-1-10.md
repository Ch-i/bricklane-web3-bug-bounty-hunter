---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-05-24-struct-finance-1-10
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-05-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md
tags:
- firm:zokyo
- report:2023-05-24-struct-finance
title: Gas Optimization
vuln_class: []
---

# Gas Optimization

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-05-24-Struct Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md)_

---

**Severity**: Low

**Status**: Unresolved

**Description**

In contract DistributionManager.sol,  In the function  queueFees
`if`  check condition is used for zero amount check.
In this case, if the given amount is zero, queuedNative isn’t changed, but the transaction will be successful. So it can cause unnecessary gas consumption.

**Recommendation**: 

Add the require check condition
