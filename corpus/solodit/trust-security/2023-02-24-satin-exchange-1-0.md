---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-24-satin-exchange-1-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-02-24T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md
tags:
- firm:trust-security
- report:2023-02-24-satin-exchange
title: TRST-M-1 Division by 0 can freeze emissions claims for veSatin holders
vuln_class: []
---

# TRST-M-1 Division by 0 can freeze emissions claims for veSatin holders

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-02-24-Satin.Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md)_

---

**Description:**
The function `_calculateClaim()` is responsible for the calculations of the amount of emissions a 
specific veSatin is entitled to claim. In doing so, this code is executed (code with mitigation from 
TRST-H-1):
```solidity
    if ((lockEndTime - weekCursor) > (minLockDurationForReward)) {
         toDistribute +=
            (balanceOf * tokensPerWeek[weekCursor]) / veSupply[weekCursor];
    weekCursor += WEEK;
         }
```
The variable **veSupply[weekCursor]** is used as a denominator without checking if it’s 0, 
which could make the function revert. If the protocol ever reaches a state where 
**veSupply[weekCursor]** is 0, all the claims for veSatin that were locked during that week 
would fail for both past and future claims. The same issue is present in the function 
`_calculateEmissionsClaim()`

**Recommended Mitigation:**
Ensure veSupply[weekCursor] is not 0 when performing the division.

**Team Response:**
Fixed

**Mitigation Review:**
The issue has not been resolved in the function `_calculateEmissionsClaim()` but has been 
resolved in the function `_calculateClaim()` which now correctly avoids division by 0.

**Mitigation Review 2:**
The issue has been resolved as suggested in both `_calculateEmissionsClaim()` and 
`_calculateClaim()`, which now correctly avoids division by 0.
