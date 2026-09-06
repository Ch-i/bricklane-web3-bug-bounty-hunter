---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-2-4
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
title: Redundant updateReward invocation
vuln_class: []
---

# Redundant updateReward invocation

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

In TradingVaultV2.sol - deposit(uint,address)/withdraw(uint) invokes updateReward(), also in the body of the method the harvest(address) invokes that method. This updates the storage twice and might lead to confusing results. It is better to follow best practices on how to implement that logic.

**Recommendation** 

Remove the invocation in deposit() since it is already invoked in harvest().
**Fixed**: Issue fixed in commit a72e06b
