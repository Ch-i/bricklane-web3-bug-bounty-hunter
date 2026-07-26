---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-3-16
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Checks-effects-interactions not obeyed
vuln_class: []
---

# Checks-effects-interactions not obeyed

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

Vester.sol - In _claim() this snippet:
```solidity
IERC20(claimableToken).safeTransfer(_receiver, amount);
cumulativeRewardDeductions[_account] += amount;
```
shows we have effects coming after interactions.

**Recommendation** 

Move the effect (updating the mapping cumulativeRewardDeductions) before the interaction (external call to safeTransfer).

**Fixed**: Issue fixed in commit a72e06b
