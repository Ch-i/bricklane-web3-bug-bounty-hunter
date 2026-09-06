---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-2-8
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Trade index has been set twice while registering the trade
vuln_class: []
---

# Trade index has been set twice while registering the trade

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

In NarwhatTradingCallbacks contract, registerTrade method called the trading storage contract to find the first empty trade index and sets it as `trade.index`.
In the same method, NarwhatTradingCallbacks makes a call to store the trade in trading storage contract which also sets the `trade.index` using the same method as above.

**Recommendation**: 

Instead of assigning the trade.index again in `storeTrade` method in TradingStorage, it will be better to check if the assigned index is correct or not.

**Fixed**: 

Issue fixed in commit a72e06b
