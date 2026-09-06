---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-2-5
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
title: Nft order retrieved is unchecked
vuln_class: []
---

# Nft order retrieved is unchecked

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**:  Low

**Status**: Resolved

**Description**

In TradingCallbacks.sol - Method executeOpenOrderCallback, nft order n retrieved from an external call to TradingStorage is not validated.

**Recommendation** 

Require statement to ensure n.trader is not equal to zero or return the method without side effects if it is equal to zero.
 **Fixed**: Issue fixed in commit a72e06b
