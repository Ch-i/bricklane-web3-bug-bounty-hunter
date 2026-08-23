---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-19-cedro-finance-2-4
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-03-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md
tags:
- firm:zokyo
- report:2024-03-19-cedro-finance
title: Incorrect Price validation
vuln_class: []
---

# Incorrect Price validation

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-03-19-Cedro Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

In Contract Oracle.sol, the following check is done on the prices fetched from chainlink:
```solidity
function priceCheck(
       bytes32 _symbol,
       uint256 _price
   ) public view returns (bool status) {
       if (
           _price == 0 ||
           _price == minValue[_symbol] || 
           _price == maxValue[_symbol]
       ) {
           return true;
       }
   }
```
Here a price is a valid price even if price is less than `minValue` or price is more the `maxValue`.

**Recommendation**: 

update the above check to ensure that the fetched price is not 0 and within the price range.

```solidity
function priceCheck(
       bytes32 _symbol,
       uint256 _price
   ) public view returns (bool status) {
       if (
           _price == 0 ||
           _price <= minValue[_symbol] || 
           _price >= maxValue[_symbol]
       ) {
           return true;
       }
   }
```
