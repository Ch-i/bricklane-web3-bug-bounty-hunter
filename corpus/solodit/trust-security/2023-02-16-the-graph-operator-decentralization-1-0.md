---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-16-the-graph-operator-decentralization-1-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-02-16T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-16-The%20Graph%20Operator%20Decentralization.md
tags:
- firm:trust-security
- report:2023-02-16-the-graph-operator-decentralization
title: TRST-L-1 collected amount might be entirely burnt as protocol fees unintentionally
vuln_class: []
---

# TRST-L-1 collected amount might be entirely burnt as protocol fees unintentionally

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-02-16-The Graph Operator Decentralization.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-16-The%20Graph%20Operator%20Decentralization.md)_

---

**Description:**
When `collect()` is called after allocation closed, entire pulled amount is consumed as protocol 
tax. The transition from closed state to finalized state is instantaneous at a specific epoch. 
Therefore, it may occur that money sent for curation and indexer query fees is consumed 
entirely as tax. This happens when the time between sending of TX and its execution is 
larger than the remaining dispute window.

**Recommended Mitigation:**
Consider adding an optional parameter in the collect() API, **allowMaxTax**. If users are willing 
for the fee to be completely burned, they may set it to true.

**Team Response:**
Acknowledged. The proposed fix would require updating the interface with the existing 
**AllocationExchange**, which is not upgradable, so instead we will document this risk in the 
function's notice so that callers ensure they call the function well before the end of the 
dispute window.
