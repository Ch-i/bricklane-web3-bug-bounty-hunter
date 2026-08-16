---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-3-29
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Missing initialization of PausableUpgradeable Contract
vuln_class: []
---

# Missing initialization of PausableUpgradeable Contract

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

In the contract Narwhal Trading Callbacks, the contracts inherits PausableUpgradeable
which has an init method __Pausable_init that needs to be called in the `initialize()`  to set the _paused to `false` state.

**Recommendation**: 

Call the __Pausable_init method in the `initialize()` method.

**Fixed**: Issue fixed in commit 3998b5b
