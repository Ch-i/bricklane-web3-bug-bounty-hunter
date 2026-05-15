---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-19-cedro-finance-1-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-03-19T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md
tags:
- firm:zokyo
- report:2024-03-19-cedro-finance
title: '`initPool(...)` can reset any existing pools'' `ceScaled` and `dtScaled` values
  to default values'
vuln_class: []
---

# `initPool(...)` can reset any existing pools' `ceScaled` and `dtScaled` values to default values

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-03-19-Cedro Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md)_

---

**Severity**: Medium

**Status**: Resolved

**Description**

In Contract Core.sol, the method `initPool(...)` allows an account with the role `INIT_POOL` to add a new pool. However, the same method can be used to set the configuration for any existing pool which will result in `ceScaled` and `dtScaled` to 1e18 i.e. default value which will lead to loss of funds for users as these values are used to calculate the LP tokens and withdrawal amount.

**Recommendation**: 

Update the `initPool` logic to not update `ceScaled/dtScaled` for any existing pool if not needed.
