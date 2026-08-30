---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2022-12-23-rysk-uniswapv3rangeorderreactor-2-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2022-12-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-23-rysk%20UniswapV3RangeOrderReactor.md
tags:
- firm:trust-security
- report:2022-12-23-rysk-uniswapv3rangeorderreactor
title: TRST-L-1 createUniswapRangeOrder() does not validate direction for hedge
vuln_class: []
---

# TRST-L-1 createUniswapRangeOrder() does not validate direction for hedge

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2022-12-23-rysk UniswapV3RangeOrderReactor.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-23-rysk%20UniswapV3RangeOrderReactor.md)_

---

**Description:**
`_createUniswapRangeOrder()` is an internal function that receives parameters for hedge 
action, including lower/upper tick and direction. It can be called from `hedgeDelta()`, in that 
case parameters are ensured to be correct by the in-contract creation. However, when 
called from `createUniswapRangeOrder()`, manager is responsible for passing these params. 
They can easily get wrong the RangeOrderDirection parameter, which will make the hedge 
only fulfillable from the wrong side. It is also not checked that lower tick < upper tick, but 
UniswapV3 logic ensures that property.

**Recommended Mitigation:**
Insert validity checks for `createUniswapRangeOrder()` parameters.

**Team Response:**
Manager may need to place an order that is outside the scope of a normal order according 
to hedgeDelta this includes orders that maybe in range or the on the opposite side of what 
the delta would dictate. Manager can also withdraw range liquidity at any time using
exitActiveRangeOrder

**Mitigation review:**
As long as described behavior is intended and documented, it is not an issue.
