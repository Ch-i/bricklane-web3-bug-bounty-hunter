---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2022-12-23-rysk-uniswapv3rangeorderreactor-3-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2022-12-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-23-rysk%20UniswapV3RangeOrderReactor.md
tags:
- firm:trust-security
- report:2022-12-23-rysk-uniswapv3rangeorderreactor
title: Hedging assumptions
vuln_class: []
---

# Hedging assumptions

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2022-12-23-rysk UniswapV3RangeOrderReactor.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-23-rysk%20UniswapV3RangeOrderReactor.md)_

---

Hedging is only activated when crossing the ticks into active territory. If price stays on the 
same side, the LMT order won't execute. This should be clearly stated as a limitation of the 
reactor.
