---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-14-ondo-finance-3-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-06-14T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-14-Ondo%20Finance.md
tags:
- firm:zokyo
- report:2023-06-14-ondo-finance
title: Unused function parameter
vuln_class: []
---

# Unused function parameter

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-06-14-Ondo Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-14-Ondo%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

In the contract ommf.sol on the line 588 there is declared a variable which is not used in the code.

**Recommendation**: 

use "_" instead of the named argument
