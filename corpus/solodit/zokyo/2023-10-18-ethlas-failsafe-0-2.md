---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-10-18-ethlas-failsafe-0-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-10-18T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-10-18-Ethlas%20Failsafe.md
tags:
- firm:zokyo
- report:2023-10-18-ethlas-failsafe
title: The application supports the concurrent sessions
vuln_class: []
---

# The application supports the concurrent sessions

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-10-18-Ethlas Failsafe.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-10-18-Ethlas%20Failsafe.md)_

---

**Severity** : Low

**Status** : Resolved  


**Description**: 

Failsafe  application currently permits authentication of a single account multiple times, leading to the possibility of multiple sessions. This also means users cannot invalidate potential attackers’ sessions when user’s credentials leaks. Moreover, the application does not display a list of active sessions, leaving users unaware if unauthorized access occurs using their credentials. 

**Recommendation**:

 The application should deactivate previously authenticated sessions when new ones are established.
