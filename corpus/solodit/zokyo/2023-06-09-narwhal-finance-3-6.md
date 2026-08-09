---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-3-6
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Inefficient storage usage
vuln_class: []
---

# Inefficient storage usage

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Informational

**Status**: Acknowledged

**Description**

In TradingVaultV2.sol - method notifyRewardAmount(), we have lastUpdateTime can be set twice to 2 different values which consumes more unnecessary gas cost.

**Recommendation** 

Implement a new version of method updateReward to be called by notifyRewardAmount() without having lastUpdateTime mutated in its implementation.

**Fix** -  As of  commit a72e06b , the informational note is acknowledged and no change by dev team.
