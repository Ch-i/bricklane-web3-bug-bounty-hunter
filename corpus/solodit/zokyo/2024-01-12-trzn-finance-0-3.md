---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-12-trzn-finance-0-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md
tags:
- firm:zokyo
- report:2024-01-12-trzn-finance
title: Function `RM_UpdateReward` in `VaultETH_V2` has no access control
vuln_class: []
---

# Function `RM_UpdateReward` in `VaultETH_V2` has no access control

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2024-01-12-TRZN Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md)_

---

**Severity**: High

**Status**: Resolved 

**Description**

Function `RM_UpdateReward` has no access control and therefore  can be called by any user even though the function seems to have to be called by risk managers.

**Recommendations**:

Mitigate these issues by performing checks to ensure that function is not called by unexpected addresses
