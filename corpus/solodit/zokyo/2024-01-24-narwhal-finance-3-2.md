---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-24-narwhal-finance-3-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-01-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-24-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2024-01-24-narwhal-finance
title: Import `MILLAGE_DENOMINATOR`
vuln_class: []
---

# Import `MILLAGE_DENOMINATOR`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-01-24-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-24-Narwhal%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

In Contract FeeHelper, variable `MILLAGE_DENOMINATOR`  can be imported from ./libs/VarCanstant.sol file like in other contracts to maintain uniformity.

**Recommendation**: 

Import the variable as suggested.
