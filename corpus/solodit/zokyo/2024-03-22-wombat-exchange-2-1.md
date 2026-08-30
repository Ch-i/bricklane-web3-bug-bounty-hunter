---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-22-wombat-exchange-2-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-03-22T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-22-Wombat%20Exchange.md
tags:
- firm:zokyo
- report:2024-03-22-wombat-exchange
title: Unnecessary condition check
vuln_class: []
---

# Unnecessary condition check

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-03-22-Wombat Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-22-Wombat%20Exchange.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

In Library `RepegHelper`, the method `_getProposedPriceScales` has the following check:
```solidity
       require(normalizedAdjustmentStep <= WAD);
```
Since the `normalizedAdjustmentStep` can not be more than 0.2e18 as per the logic of the method `_getNormalizedAdjustmentStep`, this check is not needed here.

**Recommendation**: 

Remove this unnecessary check.
