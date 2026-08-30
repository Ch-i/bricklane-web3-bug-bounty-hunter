---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-1-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: Tokens are not approved to a new pool helper.
vuln_class: []
---

# Tokens are not approved to a new pool helper.

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

LockZap.sol: setPoolHelper(). 
After the LockZap.sol initialization, it requires granting an unlimited allowance to_poolHelper in WETH and RDNT tokens. However, when a new pool is set with the function setPoolHelper(), allowance is not granted to a new pool helper. Thus the protocol couldn't operate with any new pool helper due to the lack of allowance. 

**Recommendation**: 

Consider granting allowance before each transfer OR grant unlimited allowance in the setter as well. 

**Post-audit**: 
Approval is performed before each transfer now.
