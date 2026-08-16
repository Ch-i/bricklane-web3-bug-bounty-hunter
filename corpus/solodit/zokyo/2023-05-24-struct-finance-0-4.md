---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-05-24-struct-finance-0-4
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-05-24T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md
tags:
- firm:zokyo
- report:2023-05-24-struct-finance
title: Centralization of setFEYProductImplementation()
vuln_class: []
---

# Centralization of setFEYProductImplementation()

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2023-05-24-Struct Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md)_

---

**Severity**: Medium

**Status**: Resolved

**Description**

In contract FEYProductFactory, the implementation address of the Product contract can be changed anytime by a malicious admin. This can result in users losing their funds to the attacker via a malicious implementation contract, if new products are deployed using this implementation address.


**Recommendation**: 

It is advised to disallow changing of the implementation contract. It is also advised to add more decentralization to the contract and roles, such as using a governance mechanism or a multisig.
