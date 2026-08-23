---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-1-11
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Missing Implementation of isPausable State Variable Leads to Inability to Prevent
  New Trades
vuln_class: []
---

# Missing Implementation of isPausable State Variable Leads to Inability to Prevent New Trades

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity** : Medium

**Status**: Resolved

**Description** : 

In NarwhalTradingCallback contract a state variable boolean 
isPaused that is intended to prevent new trades from being opened. However, the code does not include any mechanism for setting the value of this variable, meaning that it will always be initialized to false . Therefore, the intended functionality of preventing new trades from being opened will not be implemented.



**Recommendation** : 

Add function for IsPausable to make action on state variable and use openzeppelin pausable standard 
**Fixed**: Issue fixed in commit a72e06b
