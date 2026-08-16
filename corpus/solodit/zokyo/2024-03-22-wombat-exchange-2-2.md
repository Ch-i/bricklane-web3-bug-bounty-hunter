---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-22-wombat-exchange-2-2
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
title: Use existing values to save gas
vuln_class: []
---

# Use existing values to save gas

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-03-22-Wombat Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-22-Wombat%20Exchange.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

In Contract VolatilePool.sol, the method `_getHaircutRate()` has the following logic:

```solidity

       uint256 fromLiability = fromAsset.liability();
       uint256 toLiability = toAsset.liability();
       uint256 rFromAsset = fromLiability > 0 ? uint256(fromAsset.cash()).wdiv(fromAsset.liability()) : WAD;
       uint256 rToAsset = toLiability > 0 ? uint256(toAsset.cash()).wdiv(toAsset.liability()) : WAD;

```

Here `fromLiability` and `toLiability` are initialized but later on `fromAsset.liability()` and `toAsset.liability()`  is used as well.

**Recommendation**: 

Use already initialized variables.
