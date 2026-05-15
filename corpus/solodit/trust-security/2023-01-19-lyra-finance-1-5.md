---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-19-lyra-finance-1-5
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-01-19T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md
tags:
- firm:trust-security
- report:2023-01-19-lyra-finance
title: TRST-M-6 option board will be settled with incorrect prices when settled after
  a delay
vuln_class: []
---

# TRST-M-6 option board will be settled with incorrect prices when settled after a delay

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-01-19-Lyra Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md)_

---

**Description:** 
`settleExpiredBoard()` runs after a board expires to perform accounting. It uses 
`getSettlementPriceForMarket()` to get the settlement price, which simply returns the current 
price. It does not account for the possibility that the function was called after some delay, and 
that the current price does not reflect the option’s expiry value. This situation could arise from 
many different reasons. For example, keepers may have been offline, or the network was 
halted for some time.

**Recommended Mitigation:**
Only accept the spot price if the time elapsed since expiry is smaller than some parameter. 
Otherwise, update the settlement value using a gov-only function.

**Team response:**
This is more a design choice. The first seen spot price after a large outage feels like a better 
alternative than to rely on a centralized source for the settlement price.
