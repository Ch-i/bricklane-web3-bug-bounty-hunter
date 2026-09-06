---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2022-12-14-vagabond-token-transmuter-2-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2022-12-14T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-14-Vagabond%20Token%20Transmuter.md
tags:
- firm:trust-security
- report:2022-12-14-vagabond-token-transmuter
title: TRST-L-1 Zero duration time causes divide-by-zero exception
vuln_class: []
---

# TRST-L-1 Zero duration time causes divide-by-zero exception

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2022-12-14-Vagabond Token Transmuter.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-14-Vagabond%20Token%20Transmuter.md)_

---

**Description:**
linearVestingDuration is used as the total period from start to end of vesting in linear 
transmutation. It is set in the constructor and is fixed. There is no validation in construction 
that the variable is not set to zero. When users call `releaseTransmutedLinear()` to claim 
released tokens, `_vestingSchedule()` is called which divides by linearVestingDuration in one 
flow. 
  ```solidity
     } else {
        return (totalAllocation * (timestamp - start(_vester))) / 
         duration();
        }
 ```
This flow has no chance of completing as the function will revert with divide-by-zero 
exception. 
**Recommended Mitigation:**
Require linearVestingDuration to not be zero in the constructor.

**Team Response:**
Specific issue as well as addition safety checks implemented in the constructor.

**Mitigation review:**
Correct safety checks are included in the constructor.
