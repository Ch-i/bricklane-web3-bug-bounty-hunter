---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-2-9
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Methods `firstEmptyTradeIndex(...)` and `firstEmptyOpenLimitIndex` will always
  return 0 if no empty index available
vuln_class: []
---

# Methods `firstEmptyTradeIndex(...)` and `firstEmptyOpenLimitIndex` will always return 0 if no empty index available

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

In TradingStorage contract, methods firstEmptyTradeIndex(...) and firstEmptyOpenLimitIndex(...) uses for loop for finding the next empty index. 
These methods will always return 0 if the loop does not break and no empty index is found. 


**Recommendation**: 

Always use these methods with the following check
```solidity
require(
           storageT.openTradesCount(t.trader, t.pairIndex) +
               storageT.pendingMarketOpenCount(t.trader, t.pairIndex) +
               storageT.openLimitOrdersCount(t.trader, t.pairIndex) <
               storageT.maxTradesPerPair(),
           "MAX_TRADES_PER_PAIR"
       );
```

This will ensure not check for empty index if one doesn’t exist anymore.
**Fixed**: Issue fixed in commit a72e06b
