---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2022-12-23-rysk-uniswapv3rangeorderreactor-2-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2022-12-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-23-rysk%20UniswapV3RangeOrderReactor.md
tags:
- firm:trust-security
- report:2022-12-23-rysk-uniswapv3rangeorderreactor
title: TRST-L-7 Manager is able to create arbitrary orders
vuln_class: []
---

# TRST-L-7 Manager is able to create arbitrary orders

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2022-12-23-rysk UniswapV3RangeOrderReactor.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-23-rysk%20UniswapV3RangeOrderReactor.md)_

---

**Description:** 
Manager is able to call `createUniswapRangeOrder()` with controlled RangeOrderParams, 
meaning it can be used for a completely different use case than hedging strategy. It is 
recommended to allow only very specific parameters to be controlled by manager, such as 
tick width.

**Mitgation review:**
Fixed applied.
