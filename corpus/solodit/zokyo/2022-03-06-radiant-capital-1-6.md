---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-1-6
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: Non-withdrawable locks can be withdrawn.
vuln_class: []
---

# Non-withdrawable locks can be withdrawn.

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

LockZap.sol: setPoolHelper(). 
After the LockZap.sol initialization, the contract grants an unlimited allowance to _poolHelper in WETH and RDNT tokens. However, when a new pool is set with the function setPoolHelper(), allowance is not granted to a new pool helper. Thus the protocol couldn't operate with any new pool helper due to the lack of allowance. 

**Recommendation**: 

Check the last element of the array with index locks.length - 1' in "if". 

**Post-audit**: 
Last element of locks is not checked now. User has to call function several times to withdraw a large amount of locks.
