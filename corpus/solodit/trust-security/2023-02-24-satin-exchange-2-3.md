---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-24-satin-exchange-2-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-02-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md
tags:
- firm:trust-security
- report:2023-02-24-satin-exchange
title: TRST-L-4 It’s possible to artificially increase the supply variable in Ve.sol
vuln_class: []
---

# TRST-L-4 It’s possible to artificially increase the supply variable in Ve.sol

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-02-24-Satin.Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md)_

---

**Description:**
The function `merge()`, which is used to merge two different veSatin into one, internally calls 
`_depositFor()` which as part of its execution increases the variable **supply**, responsible for 
tracking the amount of Satin/$CASH LP locked. Since when merging two veSatin there is 
never an increase in locked tokens in the system, the function `merge()` should adjust **supply**
back, but this never happens. This bug can be used to artificially increase the variable **supply** 
by merging veSatin over and over again.

**Recommended mitigation:**
In `merge()` remove **value0**, the amount of Satin/$CASH LP locked in the first veSatin, from 
**supply**:
```solidity
      supply -= value0;
``` 
**Team response:**
Fixed

**Mitigation Review:**
The issue has been resolved as suggested, supply is now correctly adjusted.
