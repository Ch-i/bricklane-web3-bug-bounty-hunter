---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-24-satin-exchange-0-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-02-24T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md
tags:
- firm:trust-security
- report:2023-02-24-satin-exchange
title: TRST-H-1 _calculateClaim() does not distribute boost emissions correctly
vuln_class: []
---

# TRST-H-1 _calculateClaim() does not distribute boost emissions correctly

_Section severity (from Solodit section header): High_  
_Audit firm: Trust Security_  
_Source report: [2023-02-24-Satin.Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md)_

---

**Description:**
The function `_calculateClaim()` is responsible for the calculations of the amount of emissions a 
specific veSatin is entitled to claim. The idea is to distribute emissions only to veSatin tokens 
locked for more than **minLockDurationForReward** and only for the extra time the veSatin is 
locked for on top of **minLockDurationForReward**. As an example, if **minLockDurationForReward**
is set to 6 months a veSatin locked for 7 months would receive emissions for 1 month and a 
veSatin locked for 5 months would receive no emissions at all.
To do so the following code is executed in a loop, where every loop calculates the amount of 
emissions the veSatin accumulated during a specific week, in chronological order:
```solidity
      if ((lockEndTime - oldUserPoint.ts) > (minLockDurationForReward)) {
        toDistribute +=
          (balanceOf * tokensPerWeek[weekCursor]) / veSupply[weekCursor];
      weekCursor += WEEK;
      }
```
The code distributes the rewards if the elapsed time between **lockEndTime** (the locking end 
timestamp) and **oldUserPoint.ts** is bigger than **minLockDurationForReward**. However, 
**oldUserPoint.ts** is the timestamp of the last user action on a veSatin, for example depositing LP 
by calling `increaseAmount()`. As an example, a user that locks his veSatin and does nothing 
else will receive rewards for the whole locking duration. In contrast, a user that performs 
one action a week would only receive rewards for the locking duration minus 
**minLockDurationForReward**

**Recommended Mitigation:**
The variable **weekCursor** should be used instead of **oldUserPoint.ts** in the if condition:
```solidity
      if ((lockEndTime - weekCursor) > (minLockDurationForReward)) {
```   
**Team response:**
Fixed

**Mitigation Review:**
The issue has been resolved as suggested, the function `_calculateClaim()` now correctly 
handles emissions for the last minLockDurationForReward seconds of locking time
