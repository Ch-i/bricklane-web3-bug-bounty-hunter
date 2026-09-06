---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-3-28
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
title: Missing initialization of Reentrancy Guard Upgradeable Contract
vuln_class: []
---

# Missing initialization of Reentrancy Guard Upgradeable Contract

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

In the contract Narwhal Referrals and contract Narwhal Trading, these contracts inherits ReentrancyGuardUpgradeable which has an init method `__ReentrancyGuard_init` that needs to be called in the `initialize()`  to set the _status to NOT_ENTERED state.

**Recommendation**: 

Call the `__ReentrancyGuard_init` method in the `initialize()` method.

**Fixed**: Issue fixed in commit 3998b5b
