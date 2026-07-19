---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-08-25-cyfrin-stake-link-2-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-08-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-08-25-cyfrin-stake-link.md
tags:
- firm:cyfrin
- report:2023-08-25-cyfrin-stake-link
title: Missing checks for `address(0)` when assigning values to address state variables
vuln_class: []
---

# Missing checks for `address(0)` when assigning values to address state variables

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-08-25-cyfrin-stake-link.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-08-25-cyfrin-stake-link.md)_

---

```solidity
File: PriorityPool.sol

399:         distributionOracle = _distributionOracle;

```

**Client:**
Acknowledged.

**Cyfrin:** Acknowledged.
