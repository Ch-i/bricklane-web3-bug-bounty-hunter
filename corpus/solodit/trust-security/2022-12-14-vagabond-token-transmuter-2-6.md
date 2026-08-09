---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2022-12-14-vagabond-token-transmuter-2-6
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2022-12-14T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-14-Vagabond%20Token%20Transmuter.md
tags:
- firm:trust-security
- report:2022-12-14-vagabond-token-transmuter
title: TRST-L-7 Owner can pause withdrawals of vested amount
vuln_class: []
---

# TRST-L-7 Owner can pause withdrawals of vested amount

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2022-12-14-Vagabond Token Transmuter.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-14-Vagabond%20Token%20Transmuter.md)_

---

Owner can use **setEmergencyPause()** to set the isPaused flag. The flag is checked in both 
transmute functions and **releaseTransmuteLinear()**. As a result, owner can immediately 
suspend withdrawals of vested amount. It is advisable that the pause flag would only be 
applied to transmute functions as it is severe for users to not be able to withdraw an already 
vested amount.

**Mitigation review:**
Centralization issue fixed
