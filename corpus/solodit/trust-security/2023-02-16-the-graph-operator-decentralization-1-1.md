---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-16-the-graph-operator-decentralization-1-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-02-16T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-16-The%20Graph%20Operator%20Decentralization.md
tags:
- firm:trust-security
- report:2023-02-16-the-graph-operator-decentralization
title: TRST-L-2 Operator – Indexer trust assumptions
vuln_class: []
---

# TRST-L-2 Operator – Indexer trust assumptions

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-02-16-The Graph Operator Decentralization.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-16-The%20Graph%20Operator%20Decentralization.md)_

---

**Description:**
The fee collection mechanism in Graph Staking is still somewhat trusted. For example, if 
operator does not maintain sufficient GRT balance, the indexer would not be able to trigger 
collection from the operator. This could be seen as outside the scope of the Staking 
protocol; however it is Graph's responsibility to create an incentive structure that enables 
establishment of relations across the different Graph roles
