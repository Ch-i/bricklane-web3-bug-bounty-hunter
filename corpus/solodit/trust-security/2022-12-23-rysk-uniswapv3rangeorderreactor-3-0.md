---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2022-12-23-rysk-uniswapv3rangeorderreactor-3-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2022-12-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-23-rysk%20UniswapV3RangeOrderReactor.md
tags:
- firm:trust-security
- report:2022-12-23-rysk-uniswapv3rangeorderreactor
title: More comprehensive testing
vuln_class: []
---

# More comprehensive testing

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2022-12-23-rysk UniswapV3RangeOrderReactor.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-23-rysk%20UniswapV3RangeOrderReactor.md)_

---

The current test suite does not stress the contract in many important ways. It needs to 
create a variety of pools, with different tokens, token decimals and inversion. Consider fuzz 
testing the fulfillment and `hedgeDelta()` functions.
