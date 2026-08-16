---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-3-20
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Method removeTradingContract(...) needs to check if the trading contract is
  added or not
vuln_class: []
---

# Method removeTradingContract(...) needs to check if the trading contract is added or not

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

In TradingStorage contract, `removeTradingContract(address _trading)` does not check if _trading contract is added or not before flagging it false. 

**Recommendation**: 

Update the method to add the following require statement.

`require(isTradingContract[_trading], “No contract to remove”)`

**Fixed**: Issue fixed in commit a72e06b
