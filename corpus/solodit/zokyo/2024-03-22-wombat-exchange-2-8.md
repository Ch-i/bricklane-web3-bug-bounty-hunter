---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-22-wombat-exchange-2-8
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
title: Unused imports
vuln_class: []
---

# Unused imports

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-03-22-Wombat Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-22-Wombat%20Exchange.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

Following import in VolatilePool.sol is not used.
```solidity
import '../../wombat-governance/libraries/LogExpMath.sol';
```


The following imports in RepegHelper are not used.
```solidity
import '../interfaces/IRelativePriceProvider.sol';

import '../pool/PoolV4Data.sol';
```
The following import in DynamicFeeHelper is not used.
```solidity
import '../interfaces/IAsset.sol';
```


**Recommendation**: 

Removed unused imports.
