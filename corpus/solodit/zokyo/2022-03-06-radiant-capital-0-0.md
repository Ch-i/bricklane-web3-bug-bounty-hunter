---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-0-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: Wrong comparison condition.
vuln_class: []
---

# Wrong comparison condition.

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

MultiFee Distribution.sol: _withdraw Expired LocksFor(), line 1147. 
The "if " statement validates that in case relock is not disabled by the user during the relock action transaction, withdrawn funds should be restaked. However, the contract compares variable 'isRelockAction' to "false" instead of "true", which doesn't correspond to the logic of the contract. For example, if_withdrawExpired LocksFor() is called within function withdrawExpiredLocks For(), it will have parameter 'isRelockAction' set to "false" which means that funds should be transferred to the user, not restaked. However, due to the wrong condition, funds will be restaked. The issue is marked as critical since it is currently impossible for users to withdraw expired locks to their balances. 

**Recommendation**: 

Verify the comparison logic OR compare 'isRelockAction' to true instead. 

**Post-audit**. 
Comparison condition wasn't changed. Thus, function withdraw ExpiredLocksFor() still performs a relock action, however another function was added to perform withdrawing without relock.
