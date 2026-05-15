---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-1-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Missing bound check on rewardsDuration function
vuln_class: []
---

# Missing bound check on rewardsDuration function

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Medium

**Status**: Resolved

**Description**

In contracts NarwhalPool.sol and TradingVaultV2, at line 110 inside the setRewardDuration function allows the governance to to set the duration of rewards. This value is then used by the notifyRewardAmount function to calculate the reward rate (line 116). However, if the rewardsDuration parameter is set to zero, it will cause a divide-by-zero error when trying to calculate the reward rate, resulting in a contract malfunction. Additionally, if this value is very big, function may cease to produce meaningful results.

**Recommendation**: 

Add a minimum and maximum range check in the setRewardDuration function.

**Fixed**: 

Added range check.
