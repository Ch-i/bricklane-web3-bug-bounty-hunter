---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-2-7
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Lack of validation in constructor
vuln_class: []
---

# Lack of validation in constructor

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

VestingSchedule.sol - In constructor _cliffs and _vestingDurations are not validated to be the same length while it is necessary that they be so.

**Recommendation** 

require statement to be added in order to ensure that condition.

**Fix** -  As of  commit a72e06b ,  issue fixed by dev team by adding the needed require statement which asserts both lengths are the same.
