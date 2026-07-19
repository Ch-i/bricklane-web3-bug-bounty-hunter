---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-05-24-struct-finance-1-7
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-05-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md
tags:
- firm:zokyo
- report:2023-05-24-struct-finance
title: Iterating allProducts array can cause the gas limit to exceed
vuln_class: []
---

# Iterating allProducts array can cause the gas limit to exceed

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-05-24-Struct Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md)_

---

**Severity**: Low

**Status**: Unresolved

**Description**

The variable allProducts maintains an array of created products. If an external smart contract attempts to iterate over the array to validate if an address is a valid product or not, the transaction can exceed the gas limit and fail due to the large size of the array.


**Recommendation**: 

User enumerable sets instead of the array. Using enumerable sets provides additional features for validating whether an address is a valid product or not in constant time O(1). Link: https://docs.openzeppelin.com/contracts/3.x/api/utils#EnumerableSet
