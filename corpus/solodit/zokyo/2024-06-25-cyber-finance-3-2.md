---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-06-25-cyber-finance-3-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-06-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-25-Cyber%20Finance.md
tags:
- firm:zokyo
- report:2024-06-25-cyber-finance
title: Public Functions Could Be Declared External
vuln_class: []
---

# Public Functions Could Be Declared External

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-06-25-Cyber Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-25-Cyber%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

In Solidity, functions can be declared as public or external. While both visibility specifiers allow functions to be called from outside the contract, external functions are generally more gas-efficient when called externally. This is because external functions use a lower amount of gas due to optimized calldata handling.
In the CyberFinance contract, several functions that are intended to be called only from outside the contract are declared as public. These functions could be declared as external to optimize gas usage.

**Recommendation**: 

Review the contract to identify functions that are intended to be called only externally and declare them as external instead of public.
