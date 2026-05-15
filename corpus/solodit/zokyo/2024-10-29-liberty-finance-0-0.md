---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-10-29-liberty-finance-0-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-10-29T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-29-Liberty%20Finance.md
tags:
- firm:zokyo
- report:2024-10-29-liberty-finance
title: _decimalOffset can be set to 6
vuln_class: []
---

# _decimalOffset can be set to 6

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-10-29-Liberty Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-29-Liberty%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

Contract AmanaVaultV1 inherits ERC4626 from OpenZeppelin library which uses virtual shares to mitigate inflation attack by setting decimalOffset as 0 but mentions the following as well:

While not fully preventing the attack, analysis shows that the default offset
(0) makes it non-profitable, as a result of the value being captured by the virtual shares (out of the attacker's
donation) matching the attacker's expected gains.

This means although the attacker will not make a profit, it still cannot be in the magnitude to prevent the attack completely.

Openzeppelin doc further mentions:
With a larger offset, the attack becomes orders of magnitude more
expensive than it is profitable. More details about the underlying math can be found xref:erc4626.adoc#inflation-attack[here]

Hence it is advised to set decimalOffset as 6 by overriding the method in the AmanaVaultV1 contract.

**Recommendation**: 

Set _decimalOffset as 6.
