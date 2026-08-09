---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2022-12-14-vagabond-token-transmuter-1-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2022-12-14T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-14-Vagabond%20Token%20Transmuter.md
tags:
- firm:trust-security
- report:2022-12-14-vagabond-token-transmuter
title: TRST-M-1 Vesting end time is not enforced
vuln_class: []
---

# TRST-M-1 Vesting end time is not enforced

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2022-12-14-Vagabond Token Transmuter.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-14-Vagabond%20Token%20Transmuter.md)_

---

**Description:**
vestingEntryCloseTime is defined to be the time when vesting ends. However, there is a lack 
of check in **transmuteInstant()** and **transmuteLinear()**, that current time is lower than close 
time. Therefore, users may initiate new transmutations when desired period is over.

**Recommended Mitigation:**
Add a timestamp check in **transmuteInstant()** and **transmuteLinear()**

**Team Response:**
Issue was fixed.

**Mitigation review:**
Timestamp checks implemented successfully.
