---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-3-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Uncalled public functions
vuln_class: []
---

# Uncalled public functions

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

Public functions that are never called from within the contract should be marked as external.
NarwhalPool.setTokenWhitelisted
NarwhalPool.setWithdrawTimelockEnabled
NarwhalPool.getUserTokenBalance
NarwhalPool.getReservedAmount
NarwhalPool.getUserNARInfo
NarwhalPool._lockNAR
NarwhalPool._unLockNAR
NarwhalPool.stake
NarwhalPool.unstake
Vester.setNarwhalPool
VesterNLP.setTradingVault
VestingSchedule.start
VestingSchedule.changeClaimerStatus
VestingSchedule.transferAnyERC20

**Recommendation**: 

Make those functions external to optimize gas costs.

**Fixed**: Issue fixed in commit a72e06b
