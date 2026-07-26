---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-10-18-ethlas-failsafe-1-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-10-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-10-18-Ethlas%20Failsafe.md
tags:
- firm:zokyo
- report:2023-10-18-ethlas-failsafe
title: Unsecured WebSocket Reconnection Logic
vuln_class: []
---

# Unsecured WebSocket Reconnection Logic

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-10-18-Ethlas Failsafe.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-10-18-Ethlas%20Failsafe.md)_

---

**Severity** : Informational 

**Status** : Acknowledged 

**Description**:

In Interceptor the Writer.js the logic to reconnect the WebSocket can potentially be exploited by forcing socket closure, leading to a Denial-of-Service (DoS) scenario.
An attacker may exploit this by repeatedly causing the WebSocket to close or error (could be through a network attack or by exploiting another vulnerability that can crash the socket), knowing that the system will keep trying to reconnect without backoff or limit. This could lead to resource exhaustion or Denial-of-Service (DoS) as the system is constantly trying to reconnect.

**Recommendation**:

Implement a secure reconnection strategy, including a back-off strategy and limiting reconnection attempts to mitigate the risk of DoS attacks
