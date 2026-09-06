---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-05-24-struct-finance-2-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-05-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md
tags:
- firm:zokyo
- report:2023-05-24-struct-finance
title: Inverted naming of variables
vuln_class: []
---

# Inverted naming of variables

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-05-24-Struct Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md)_

---

**Severity**: Informational

**Status**: Acknowledged

**Description**


In contract FEYTraderJoeProduct, the naming of leverageThresholdMax and leverageThresholdMin variables is inverted with respect to their execution logic. Inverted naming can lead to confusion during code review. 

**Recommendation**: 

It is advised to avoid naming of variables that are the exact opposite of how they behave.
 
**Comments**:  The client acknowledged this issue, stating that this is due to the financial terms used in traditional finance, which led them to use the following naming conventions.
