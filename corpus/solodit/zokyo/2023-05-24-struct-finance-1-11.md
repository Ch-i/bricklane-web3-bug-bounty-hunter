---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-05-24-struct-finance-1-11
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-05-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md
tags:
- firm:zokyo
- report:2023-05-24-struct-finance
title: No check for zero amount
vuln_class: []
---

# No check for zero amount

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-05-24-Struct Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md)_

---

**Severity**: Low

**Status**: Acknowledged

**Description**

In contract DistributionManager.sol, the function  setRewardsPerSecond, there is no zero amount check.

**Recommendation**: 

Add the zero amount check

**Comment**: It can be zero initially to avoid distributing rewards
