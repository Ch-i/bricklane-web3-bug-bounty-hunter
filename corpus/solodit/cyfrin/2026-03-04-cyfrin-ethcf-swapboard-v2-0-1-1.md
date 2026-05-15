---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-ethcf-swapboard-v2-0-1-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-03-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-ethcf-swapboard-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-04-cyfrin-ethcf-swapboard-v2-0
title: Use named mappings parameters to explicitly indicate the purpose of keys and
  values
vuln_class: []
---

# Use named mappings parameters to explicitly indicate the purpose of keys and values

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-ethcf-swapboard-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-ethcf-swapboard-v2.0.md)_

---

**Description:** Use named mappings parameters to explicitly indicate the purpose of keys and values:
```solidity
Swapboard.sol
39:    mapping(uint256 => Order) public orders;
```

**ETHCF:** Fixed in commit [572f3c5](https://github.com/ETHCF/swapboard/commit/572f3c5d724b78fc3a2f304557a23c018f9fc31d).

**Cyfrin:** Verified.
