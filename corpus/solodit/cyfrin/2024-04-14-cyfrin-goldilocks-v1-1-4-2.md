---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-14-cyfrin-goldilocks-v1-1-4-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-04-14T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md
tags:
- firm:cyfrin
- report:2024-04-14-cyfrin-goldilocks-v1-1
title: Use `uint256(1)/uint256(2)` instead of `true/false` to save gas for changes.
vuln_class: []
---

# Use `uint256(1)/uint256(2)` instead of `true/false` to save gas for changes.

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-14-cyfrin-goldilocks-v1.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md)_

---

Avoids 20000 gas when changing from `false` to `true`, after having been true in the past.

```solidity
File: Goldilend.sol
107:   bool public borrowingActive;

File: Goldivault.sol
91:   bool public concluded;
```
