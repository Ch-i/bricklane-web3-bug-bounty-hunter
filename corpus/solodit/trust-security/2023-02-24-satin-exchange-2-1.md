---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-24-satin-exchange-2-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-02-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md
tags:
- firm:trust-security
- report:2023-02-24-satin-exchange
title: TRST-L-2 The logic in _calculateClaim() can leave some tokens locked and waste
  gas
vuln_class: []
---

# TRST-L-2 The logic in _calculateClaim() can leave some tokens locked and waste gas

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-02-24-Satin.Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md)_

---

**Description:**
The function `_calculateClaim()` is responsible for the calculations of the amount of emissions a 
specific veSatin is entitled to claim. To do so, this code is executed in a loop for each week from 
the current timestamp to the last claim (code with mitigation from TRST-H-1):
```solidity
    if ((lockEndTime - weekCursor) > (minLockDurationForReward)) {
             toDistribute +=
         (balanceOf * tokensPerWeek[weekCursor]) / veSupply[weekCursor];
      weekCursor += WEEK;
    }
```
When the if condition is not met two things happen:
- An amount of emissions that was supposed to be distributed ((balanceOf * 
tokensPerWeek[weekCursor]) / veSupply[weekCursor])) is skipped, meaning it will stay 
locked in the contract.
- The function `_calculateClaim()` will loop for the maximum number of times (50), because 
**weekCursor** is not increased, wasting users' gas.

**Recommended Mitigation:**
When the if condition is not met burn the tokens that were supposed to be distributed and 
exit the loop. Since the non-distributed tokens would stay locked it’s not strictly necessary to 
burn them.

**Team Response:**
Fixed

**Mitigation Review:**
The issue has been resolved as suggested, the function `_calculateClaim()` exits the loop as soon 
as necessary. The non-distributed tokens stay locked in the contract
