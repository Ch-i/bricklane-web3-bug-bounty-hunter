---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-01-02-onchain-trade-2-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-01-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-01-02-Onchain%20Trade.md
tags:
- firm:zokyo
- report:2023-01-02-onchain-trade
title: Shadowing inherited state variables
vuln_class: []
---

# Shadowing inherited state variables

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-01-02-Onchain Trade.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-01-02-Onchain%20Trade.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

In contract Liquidity.sol, in function lpName, the variable symbol is a shadowing variable with the same name from inherited contract ERC20.

**Recommendation**: 

Rename function parameter symbol.
