---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-05-24-struct-finance-0-5
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-05-24T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md
tags:
- firm:zokyo
- report:2023-05-24-struct-finance
title: Exposure to revert due to wrong operation.
vuln_class: []
---

# Exposure to revert due to wrong operation.

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2023-05-24-Struct Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md)_

---

**Severity**: Medium

**Status**: Resolved

**Description**

In contract DistributionManager.sol, the function  distributeRewards


is exposed to a panic revert (leads to Denial of service) in some valid cases if the one of totalAllocationPoints and totalAllocationFee  is zero.

**Recommendation**: 

Add zero amount check.
