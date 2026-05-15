---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-05-24-struct-finance-2-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-05-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md
tags:
- firm:zokyo
- report:2023-05-24-struct-finance
title: initialize() can be called by anyone
vuln_class: []
---

# initialize() can be called by anyone

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-05-24-Struct Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md)_

---

**Severity**: Informational

**Status**: Acknowledged

**Description**

In contract FEYTraderJoeProduct, function initialize() can be called by anyone to initialize the product contract. This can result in incorrect values being used for initialization.

**Recommendation**: 

Although the factory contract immediately initializes the product contract after deployment, it  is advised to add appropriate modifiers for the initialize() function as a best practice.


**Comments**: The client stated that this would happen when the product contract is deployed separately without the factory contract and stated that their comment on issue 8 would be applicable here.
