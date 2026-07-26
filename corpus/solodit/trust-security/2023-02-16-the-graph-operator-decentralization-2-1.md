---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-16-the-graph-operator-decentralization-2-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-02-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-16-The%20Graph%20Operator%20Decentralization.md
tags:
- firm:trust-security
- report:2023-02-16-the-graph-operator-decentralization
title: Redundant event emission
vuln_class: []
---

# Redundant event emission

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-02-16-The Graph Operator Decentralization.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-16-The%20Graph%20Operator%20Decentralization.md)_

---

In `collect()`, the event AllocationCollected is emitted outside the main if block. It is 
recommended that it shall be placed inside the if block, as when queryFees is zero, the 
function doesn't change state and therefore shouldn’t emit an event.
