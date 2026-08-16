---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-3-31
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
title: Unsafe casting from uint256 to int256
vuln_class: []
---

# Unsafe casting from uint256 to int256

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Informational

**Status**: Acknowledged

**Description**

In contract TradingStorage.sol, the method getNetOI(...) is converting openInterestUSDT[_pairIndex][0] and openInterestUSDT[_pairIndex][1] of type uint256 to type int256 unsafely. We understand that it will not cause any issue unless openInterestUSDT[_pairIndex][X] is greater than type(int256).max which is highly unlikely but this conversion is considered anti-pattern.

**Recommendation**: 

Use openzeppelin SafeCast Library to cast.
