---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-22-wombat-exchange-1-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-03-22T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-22-Wombat%20Exchange.md
tags:
- firm:zokyo
- report:2024-03-22-wombat-exchange
title: Method `_getHaircutRate` should check if the price anchor is set or not
vuln_class: []
---

# Method `_getHaircutRate` should check if the price anchor is set or not

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-03-22-Wombat Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-22-Wombat%20Exchange.md)_

---

**Severity**: Low

**Status**: Acknowledged

**Description**

In Contract VolatilePool.sol, the method `_getHaircutrate(...)` calculates the volatility of `fromAsset` and `toAsset` if they are not price anchor.

Since `priceAnchor` is not set in the `initialize()` method, there is a possibility of it not being assigned and this will lead to volatility calculation even for `priceAnchor` asset if it is either `fromAsset` or `toAsset` which will lead to wrong haircut rate.

**Recommendation**: 

Ensure that the price anchor is set before `getHaircutrate` can be calculated.
