---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-07-05-made-for-gamers-2-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2022-07-05T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-07-05-Made%20for%20gamers.md
tags:
- firm:zokyo
- report:2022-07-05-made-for-gamers
title: Use Solidity literal.
vuln_class: []
---

# Use Solidity literal.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-07-05-Made for gamers.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-07-05-Made%20for%20gamers.md)_

---

**Description**

EXPO.sol and EXPOVO.sol: function initialize(), line 31. Currently, "maxSupply" is assigned to a value 2700000000000000000000000000000. Such notation is difficult to be read and may lead to accuracy mistakes, when some zeros might be missed.

**Recommendation**

Since both contracts inherit OZ ERC777 standard token, which has 18 decimals, ether literal can be used to increase code readability. For example: 2_700_000_000_000 ether.

**Re-audit comment**

Resolved
