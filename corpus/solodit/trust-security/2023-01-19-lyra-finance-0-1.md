---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-19-lyra-finance-0-1
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
title: TRST-H-2 canHedge will return true when hedging requirement would be above
  the defined hedgeCap
vuln_class: []
---

# TRST-H-2 canHedge will return true when hedging requirement would be above the defined hedgeCap

_Section severity (from Solodit section header): High_  
_Audit firm: Trust Security_  
_Source report: [2023-01-19-Lyra Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md)_

---

**Description:**
Lyra’s security model relies on being able to hedge and achieve delta-neutrality when opening 
a user position. The check is done in `canHedge()` in GMXFuturesPoolHedger. The expected 
hedge is fetched using `_getCappedExpectedHedge()`. However, it is never checked that the 
hedge has reached capacity, which should disqualify the hedge from taking place. Any hedge 
above the cap will never be hedged, so whenever `canHedge()` wrongly approves a hedge that 
is beyond the cap, the protocol will be guaranteed not to be delta-neutral.

**Recommended Mitigation:**
If **expectedHedge** is, in absolute value, equal to the **hedgeCap**, return false

**Team Response:**
This is more a design choice than an issue. To account for all cases (as in the flagged issue) an 
additional parameter would need to be added to allow opening above the cap which is the 
current intended design.
