---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-05-24-struct-finance-0-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-05-24T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md
tags:
- firm:zokyo
- report:2023-05-24-struct-finance
title: Centralization of Pausable and possible Denial of Service
vuln_class: []
---

# Centralization of Pausable and possible Denial of Service

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2023-05-24-Struct Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md)_

---

**Severity**: Medium

**Status**: Resolved

**Description**

In contract FEYTraderJoeProduct, The global and local pausable functionality can be exploited by a malicious admin to deny users from withdrawing their funds for a very long time. This would also be equivalent to a Denial of Service attack if carried out.


**Recommendation**: 

It is advised to add more decentralization to the contract and roles, such as using a governance mechanism or a multisig.
 
**Comments**: The client assured that they would be using a multisig initially before moving on to a Governance model.
