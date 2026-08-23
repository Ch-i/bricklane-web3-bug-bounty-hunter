---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2022-12-23-rysk-uniswapv3rangeorderreactor-1-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2022-12-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-23-rysk%20UniswapV3RangeOrderReactor.md
tags:
- firm:trust-security
- report:2022-12-23-rysk-uniswapv3rangeorderreactor
title: TRST-M-4 hedgeDelta(0) doesn’t behave properly
vuln_class: []
---

# TRST-M-4 hedgeDelta(0) doesn’t behave properly

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2022-12-23-rysk UniswapV3RangeOrderReactor.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-23-rysk%20UniswapV3RangeOrderReactor.md)_

---

**Description:**
`hedgeDelta()` is called again by the pool when the exposure to underlying asset needs to 
change. If it was previously non-zero and the pool wishes to reset the delta to zero, 
`hedgeDelta(0)` would be called. Unfortunately, it will never execute.

Flow will enter the sell wETH branch and call `_createUniswapRangeOrder()` with 0 delta. 
Eventually it will try minting a UniswapV3 position with 0 liquidity, which reverts at the 
Uniswap level.

As a result, the previous exposure remains as `_yankRangeOrderLiquidity()` is not called.

**Recommendation:**
Add branching logic for hedgeDelta. If delta is 0, do nothing.

**Team response**
Fixed

**Mitigation Review**
hedgeDelta() now correctly implements an early-exit in case _delta is 0.
