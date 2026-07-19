---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-12-trzn-finance-3-8
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md
tags:
- firm:zokyo
- report:2024-01-12-trzn-finance
title: No validation when setting parameters
vuln_class: []
---

# No validation when setting parameters

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-01-12-TRZN Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

In Contract VaultETH_V2, methods `setParam(...)` and `setParams2(...)` set a lot of different values but they are not validated.

**Recommendation**: 

Add validation for setup parameters to ensure proper configuration values.
