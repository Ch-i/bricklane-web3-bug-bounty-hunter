---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-24-satin-exchange-0-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-02-24T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md
tags:
- firm:trust-security
- report:2023-02-24-satin-exchange
title: TRST-H-2 Users will be unable to claim emissions from veSatin tokens if they
  withdraw it or merge it
vuln_class: []
---

# TRST-H-2 Users will be unable to claim emissions from veSatin tokens if they withdraw it or merge it

_Section severity (from Solodit section header): High_  
_Audit firm: Trust Security_  
_Source report: [2023-02-24-Satin.Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md)_

---

**Description:**
The function `_calculateClaim()` uses the variable **lockEndTime** when checking if a veSatin is 
entitled to emissions for a particular week (code with mitigation from TRST-H-1):
```solidity
           if ((lockEndTime - weekCursor) > (minLockDurationForReward)) {
            toDistribute +=
        (balanceOf * tokensPerWeek[weekCursor]) / veSupply[weekCursor];
        weekCursor += WEEK;
       }
```
However **lockEndTime** is set to 0 whenever a user withdraws a veSatin by calling `withdraw()` or 
merges one by calling `merge()`. When this is the case the operation **lockEndTime - weekCursor** 
underflows, thus reverting. This results in users being unable to claim veSatin emissions if they 
withdraw or merge it first

**Recommended Mitigation:**
In the `withdraw()` and merge() functions, call `claim()` in VeDist.sol to claim emissions before 
setting the lock end timestamp to 0. In `merge()` this is only necessary for the veSatin passed 
as **_from**

**Team Response:**
Fixed

**Mitigation Review:**
The issue has been resolved as suggested, both `merge()` and `withdraw()` now call `claim()` in 
VeDist.sol before **lockEndTime** is set to 0.
