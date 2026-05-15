---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-19-cedro-finance-2-9
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-03-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md
tags:
- firm:zokyo
- report:2024-03-19-cedro-finance
title: Insufficient Validation of Token Addresses in Pool Initialization
vuln_class: []
---

# Insufficient Validation of Token Addresses in Pool Initialization

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-03-19-Cedro Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md)_

---

**Severity**: Low

**Status** : Acknowledged 

**Description** : 

The `Core.initPool` function in the given smart contract lacks necessary validations to ensure the distinctiveness of `_ceToken` and `_debtToken` (debt token) addresses. This absence of validation could lead to critical issues in the contract's lending and borrowing functionalities.

**Recommendation** : 

**Implement Address Validation**: Modify the initPool function to include checks ensuring that `_ceToken` and `_debtToken` are not only non-zero but also distinct from each other
Note#2 : admin will take care of it while initialization
