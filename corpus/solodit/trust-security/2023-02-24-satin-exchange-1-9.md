---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-24-satin-exchange-1-9
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-02-24T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md
tags:
- firm:trust-security
- report:2023-02-24-satin-exchange
title: TRST-M-10 updatePeriod() distributes the same amount of emissions regardless
  of the time passed from the last distribution
vuln_class: []
---

# TRST-M-10 updatePeriod() distributes the same amount of emissions regardless of the time passed from the last distribution

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-02-24-Satin.Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md)_

---

**Description:**
The function `updatePeriod()` distributes new rewards when it’s called more than one week 
after the last distribution. However, if a distribution only happens after two weeks or more, 
the distributed amount is the same as if only one week passed. This can lead to users 
earning fewer rewards than they would expect.

**Recommended mitigation:**
Adjust the amount of emissions to the amount of full weeks passed since the last 
distribution.

**Team response:**
Fixed

**Mitigation Review:**
The proposed fix multiplies the current amount of **WEEKLY_EMISSION** by the number of 
whole weeks (periods) passed since the last **activePeriod**, but the number of emissions 
should decrease by a percentage for every period passed. 
As an example, if 3 periods passed from the last call to `updatePeriod()` and 
**WEEKLY_EMISSION** is set to 1000 SATIN, then the amount of emissions would be calculated 
as 1000 * 3 = 3000 SATIN:
```solidity
        _period = (block.timestamp / _WEEK) * _WEEK;
           uint sinceLast = _period - activePeriod;
         uint emissionsMultiplier = sinceLast / _WEEK;
      uint _weekly = WEEKLY_EMISSION * emissionsMultiplier;
```
However because every period the emissions should decrease by 2% the total amount 
should be 1000 + 1000 * (98/100) + 1000 * (98/100)^2 = 2940 SATIN

**Mitigation Review 2:**
The issue introduced by the fix has been resolved as suggested.
