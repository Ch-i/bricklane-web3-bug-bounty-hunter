---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-20-cyfrin-myriad-realitio-oracle-v2-0-0-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-03-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-20-cyfrin-myriad-realitio-oracle-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-20-cyfrin-myriad-realitio-oracle-v2-0
title: Consider using named mappings
vuln_class: []
---

# Consider using named mappings

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-20-cyfrin-myriad-realitio-oracle-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-20-cyfrin-myriad-realitio-oracle-v2.0.md)_

---

**Description:** The `questions` mapping uses an unnamed key type:

```solidity
mapping(uint256 => bytes32) public questions;
```

Solidity 0.8.18 introduced named mapping parameters, which improve readability and tooling support.

**Recommended Mitigation:**
```solidity
mapping(uint256 marketId => bytes32 questionId) public questions;
```


**Myriad:** Fixed in commit [`e3e2876`](https://github.com/Polkamarkets/polkamarkets-js/commit/e3e28763a0c807f673032aae678cd63378ebf80f)

**Cyfrin:** Verified.
