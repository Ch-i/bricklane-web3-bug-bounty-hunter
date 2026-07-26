---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-10-13-thestandard-io-2-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2022-10-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-10-13-TheStandard.io.md
tags:
- firm:zokyo
- report:2022-10-13-thestandard-io
title: Gas optimization opportunity in TokenManager `deleteToken` function.
vuln_class: []
---

# Gas optimization opportunity in TokenManager `deleteToken` function.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-10-13-TheStandard.io.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-10-13-TheStandard.io.md)_

---

**Description**

TokenManager.sol
Possible Gas optimization in the deleteToken function.
Current code:
for (uint256 $i=$ index; i < tokenSymbols.length $-1$; i++)
Suggestion:
uint256 len = tokenSymbols.length;
for (uint256 $i=$ index; i < len;) {
unchecked {
++i;
}
}

**Recommendation**

Storing array length in 'len' saves gas rather than reading the length every time. Also, `++i` saves gas rather than 'i++`. The unchecked keyword can be used while incrementing if the number of tokens to be added is intended to exceed the maximum value of uint256 type.

**Re-audit comment**

Unresolved
