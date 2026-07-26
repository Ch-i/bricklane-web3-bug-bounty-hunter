---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-05-24-struct-finance-1-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-05-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md
tags:
- firm:zokyo
- report:2023-05-24-struct-finance
title: Bypassing require checks possible
vuln_class: []
---

# Bypassing require checks possible

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-05-24-Struct Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md)_

---

**Severity**: Low

**Status**: Acknowledged

**Description**


In contract FEYTraderJoeProduct, It is possible to deploy Product contract without the factory contract. If someone accidentally deploys the Product contract without the factory, then all the critical requirement checks used in the _validateProductConfig() can be bypassed. 

**Recommendation**: 

It is advised to make the FEYTraderJoeProduct contract abstract in order to avoid this issue.

**Comments**: 

The client stated that If the product contract is deployed by someone(without the factory), then the frontend would need to be exploited to trick the users to deposit funds into the malicious contract. And that Direct interaction with the malicious contract is very unlikely, as the users could easily read the params from the explorer if verified.
