---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-05-24-struct-finance-1-6
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-05-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md
tags:
- firm:zokyo
- report:2023-05-24-struct-finance
title: Pause/Unpause functions should emit event to notify users
vuln_class: []
---

# Pause/Unpause functions should emit event to notify users

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-05-24-Struct Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md)_

---

**Severity** : Low

**Status**: Acknowledged

**Description**

In contract GACManaged, the two functions are used to pause and unpause the contract. They should emit an event so that the user would be notified when this is happening.

**Recommandation**:  

Consider emitting events to notify 

**Comment**: GACManaged inherits OpenZeppelin.Pausable contract. _pause() is being triggered and the event is already being emitted from the Pausable contract
