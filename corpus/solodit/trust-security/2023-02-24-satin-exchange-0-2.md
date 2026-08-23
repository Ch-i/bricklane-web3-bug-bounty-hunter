---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-24-satin-exchange-0-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-02-24T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md
tags:
- firm:trust-security
- report:2023-02-24-satin-exchange
title: TRST-H-3 Additional Satin/$CASH LP locked in an owner-created veSatin can’t
  be withdrawn
vuln_class: []
---

# TRST-H-3 Additional Satin/$CASH LP locked in an owner-created veSatin can’t be withdrawn

_Section severity (from Solodit section header): High_  
_Audit firm: Trust Security_  
_Source report: [2023-02-24-Satin.Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md)_

---

**Description:**
_The protocol allows the owners to create a special veSatin for the owners and partners via 
`createLockForOwner()`, which does not require to lock LP. On such veSatin, the protocol 
reverts when calling `withdraw()`, `merge()`, and `increaseUnlockTime()`. However the function 
`increaseAmount()`, which is used to lock extra Satin/$CASH LP, does not.
This could lead to partners adding Satin/$CASH LP to their position, but then being unable 
wot withdraw it, since `withdraw()` would revert.

**Recommended Mitigation:**
Revert on calls to `increaseAmount()` for veSatin tokens created via `createLockForOwner()`, 
like in the other functions.

**Team response:**
Fixed

**Mitigation Review:**
The issue has been resolved as suggested, `increaseAmount()` can’t be called anymore on a 
veSatin created via `createLockForOwner()`.
