---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2022-12-23-rysk-uniswapv3rangeorderreactor-2-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2022-12-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-23-rysk%20UniswapV3RangeOrderReactor.md
tags:
- firm:trust-security
- report:2022-12-23-rysk-uniswapv3rangeorderreactor
title: TRST-L-5 Governor has unlimited access to contract's funds
vuln_class: []
---

# TRST-L-5 Governor has unlimited access to contract's funds

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2022-12-23-rysk UniswapV3RangeOrderReactor.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-23-rysk%20UniswapV3RangeOrderReactor.md)_

---

**Description:** 
Governor is able to call `recoverETH()`, `recoverERC20()` and `exitActiveRangeOrder()`. It 
introduces significant risks in the event of a private key compromise or a rug pull. The 
recommendation is to delegate complete access to the parent pool and that Governor is 
only able to get delayed access to the funds.

**Mitgation review:**
Fixed applied.

 ### TRST-L-6 Changes to onlyAuthorizedFulfill take effect immediately
 **Description:** 
Owner can lock access to `fulfillActiveRangeOrder()` without prior warning. Such an ability 
may catch users off guard, so it is best to implement a delay.

**Mitgation review:**
Fixed applied.
