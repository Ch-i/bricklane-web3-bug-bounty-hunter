---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-19-lyra-finance-0-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-01-19T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md
tags:
- firm:trust-security
- report:2023-01-19-lyra-finance
title: TRST-H-1 canHedge may return wrong result when there is a pending position
  request
vuln_class: []
---

# TRST-H-1 canHedge may return wrong result when there is a pending position request

_Section severity (from Solodit section header): High_  
_Audit firm: Trust Security_  
_Source report: [2023-01-19-Lyra Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md)_

---

**Description:**
Lyra’s security model relies on being able to hedge and achieve delta-neutrality when opening 
a user position. The check is done in `canHedge()` in GMXFuturesPoolHedger. The current 
hedge is calculated using `_getCurrentHedgedNetDeltaWithSpot()`. However, this function only 
takes the current position and ignores the pending increase/decrease position request. 
Therefore, `canHedge` result can be wrong - users may be rejected from interacting with the 
market, while attackers or innocent users may put the protocol in an unchangeable position.

**Recommended Mitigation:**
Including the pending position in the current hedge calculation.

**Team response:**
While this is a valid issue, `canHedge` is an added safety rail rather than a critical component 
of the system. Unwanted option positions being opened to expose LPs to unwanted delta risk 
will cost attackers the fees to open option positions and all they achieve is exposing LPs to 
some limited directional/delta risk. Adding additional complexity to an already complex 
system feels unnecessary at this stage so this will not be implemented.
