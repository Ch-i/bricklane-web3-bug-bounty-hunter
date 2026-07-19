---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-08-07-boba-network-1-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-08-07T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-08-07-Boba%20Network.md
tags:
- firm:zokyo
- report:2023-08-07-boba-network
title: Method could return 0 based on oracles returned decimals feeds
vuln_class: []
---

# Method could return 0 based on oracles returned decimals feeds

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-08-07-Boba Network.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-08-07-Boba%20Network.md)_

---

**Description**

In contract Boba Deposit Paymaster, function "getTokenValueOfEth" is translating a given value amount of ethereum into the underlying token amount, for that the business logic is using oracles to query for values and different token decimals, oracles will be chosen by the admin of the contract, based on the function comments there is no check over the variable requiredAmount to ensure it's not 0 as priceRatio shouldn't normally exceed ethBought value, that statement is not always true and it is dependent of the values returned by the oracles, as the oracles are chosen by the owner, there is the possibility that one oracles will returned a price feed on 8 decimals and another one on 18 decimals and so on, and that will ruin the assumption that required Amount can not be 0.

**Recommendation**

Add a sanity check to ensure that the function can not return the value at the end.

**Re-audit comment**

Resolved
