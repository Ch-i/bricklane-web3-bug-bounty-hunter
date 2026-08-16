---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-22-wombat-exchange-2-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-03-22T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-22-Wombat%20Exchange.md
tags:
- firm:zokyo
- report:2024-03-22-wombat-exchange
title: Unsafe cast
vuln_class: []
---

# Unsafe cast

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-03-22-Wombat Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-22-Wombat%20Exchange.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

In Contract VolatilePool.sol, the method `_getHaircutRate()` has the following logic:
```solidity

return
           poolData.haircutRate +
           DynamicFeeHelper.getVolatilityHaircutRate(dynamicFeeConfig, volatility.toInt256()) +
           DynamicFeeHelper.getImbalanceHaircutRate(dynamicFeeConfig, int256(rFromAsset), int256(rToAsset));
```
Here, `rFromAsset` and `rToAsset` are cast to int256 unsafely. 

**Recommendation**: Use `.toInt256()` for casting `rFromAsset` and `rToAsset`.
