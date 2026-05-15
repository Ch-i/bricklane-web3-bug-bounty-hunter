---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-3-24
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: LimitOrders interface variable is named `nftRewards` in several contracts
vuln_class: []
---

# LimitOrders interface variable is named `nftRewards` in several contracts

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**


In NarwhatTrading contract and NarwhatTradingCallbacks contract, the LimitOrdersInterface variable is named `nftRewards` which has nothing to do with NFTs. 

**Recommendation**: 

Rename those variables to more meaningful name.

**Fixed**: Issue fixed in commit a72e06b
