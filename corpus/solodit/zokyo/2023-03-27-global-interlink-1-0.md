---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-03-27-global-interlink-1-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-03-27T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-03-27-Global%20Interlink.md
tags:
- firm:zokyo
- report:2023-03-27-global-interlink
title: Insufficient sanity checks for treasury creation
vuln_class: []
---

# Insufficient sanity checks for treasury creation

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2023-03-27-Global Interlink.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-03-27-Global%20Interlink.md)_

---

**Severity**: Medium

**Status**: Resolved

**Description**

In contract token_vesting.move, in function `create_treasury` there are no sanity checks for the `total_lock_in_days`, `vesting_period_in_days` and `initial_lock_in_days` variables. It would be ideal to add checks to prevent these values from being zero or being invalid combinations. Also, the `vesting_period_in_days` and `initial_lock_in_days` parameters are not checked to make sure they are not greater than the variable `total_lock_in_days` which could lead to unexpected behavior if the vesting period 	is longer than the total lock period. Even if these values are set in a function that’s protected by admin rights, there is a chance that a mistake is made and not noticed before it leads to a possible issue.

**Recommendation**: 

Add sanity checks to make sure that these parameters are set to the correct values.
