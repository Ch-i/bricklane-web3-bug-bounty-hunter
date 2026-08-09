---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-22-wombat-exchange-2-9
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-03-22T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-22-Wombat%20Exchange.md
tags:
- firm:zokyo
- report:2024-03-22-wombat-exchange
title: Use specific Solidity compiler version
vuln_class: []
---

# Use specific Solidity compiler version

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-03-22-Wombat Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-22-Wombat%20Exchange.md)_

---

**Severity**: Informational

**Status**: Acknowledged

**Description**

Audited contracts use the following floating pragma:
```solidity
pragma solidity ^0.8.5;
```
It allows to compile contracts with various versions of the compiler and introduces the risk of using a 
different version when deploying than during testing.

**Recommendation**: 

Use a specific version of the Solidity compiler.
