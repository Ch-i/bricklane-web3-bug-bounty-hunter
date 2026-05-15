---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-2-17
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Missing Check for Price returned from tokenPriceUSDT
vuln_class: []
---

# Missing Check for Price returned from tokenPriceUSDT

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity** : Low

**Status**: Resolved

**Descritption** :

The tokenPriceUSDT function should have a check in place to ensure that the price returned from the queryPriceFeed function is not zero, as this could lead to a vulnerability. Without this check, users could potentially exploit the system by using a feed with a zero price to manipulate the values returned by the function.

**Recommendation** : 

Add Check For Non-zero Price after the Querying price from PythOracle 
```solidity
require(priceFeed.price.price != 0, “PRICE_FEED_ERROR”); // add check for non-zero price
```
**Fixed**: Issue fixed in commit a72e06b
