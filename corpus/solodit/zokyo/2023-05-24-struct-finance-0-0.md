---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-05-24-struct-finance-0-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-05-24T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md
tags:
- firm:zokyo
- report:2023-05-24-struct-finance
title: Centralization of emergencyRemoveLiquidity()
vuln_class: []
---

# Centralization of emergencyRemoveLiquidity()

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2023-05-24-Struct Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md)_

---

**Severity**: Medium

**Status**: Resolved


**Description**

In contract FEYTraderJoeProduct, the emergencyRemoveLiquidity() function can be used by a malicious admin to withdraw all the liquidity from the contracts at any point of time or state. 


**Recommendation**: 

It is advised to add more decentralization to the contract and roles, such as using a governance mechanism or a multisig.
 
**Comments**: The client assured that they would be using a multisig initially before moving on to a Governance model.
